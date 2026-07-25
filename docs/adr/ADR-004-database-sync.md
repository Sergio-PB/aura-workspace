# ADR-004: Database & Sync Strategy

Date: 2026-07-25
Status: proposed

## Context

Aura's data model spans three domains: **Farm** (local device — recordings, attributions, telemetry), **Card** (local device — identity, claimed points, feed cache), and **Backend** (server — user registry, shared attributions, validation records, feed aggregation). The database strategy must serve all three while honoring the local-first, privacy-by-design principles.

Key requirements:
- Farm works fully offline — recordings and attributions stored locally
- Card works fully offline — identity, claimed points, cached feed
- Backend is the shared source of truth for cross-user data
- Privacy: telemetry stays on-device; only user-explicitly-shared data reaches the backend
- Eventual consistency: devices go offline, sync when connected
- Solo developer + agent — minimal operational overhead
- Start with zero cloud infrastructure (M1 Pro only)

## Options Considered

### A: SQLite Everywhere (Local-Only, No Server DB)

Farm and Card use SQLite locally. Backend also uses SQLite. No sync engine — data moves via explicit API calls (REST).

- **Pros:** Simplest possible setup. Zero infra. One database engine everywhere. Bun has native SQLite. Drizzle ORM works identically on all three.
- **Cons:** No sync primitives. Every sync edge case (conflicts, offline queue, retry) must be hand-rolled in application code. Backend SQLite hits concurrency limits under multi-user load. No read replicas, no point-in-time recovery.

### B: SQLite Local + PostgreSQL Server (Hybrid)

Farm and Card use SQLite locally. Backend uses PostgreSQL. Data syncs via REST API. No CRDT or automatic sync — explicit push/pull.

- **Pros:** Best of both worlds. SQLite is perfect for local (zero-config, embedded, fast). PostgreSQL handles multi-user concurrency, backups, and scaling on the server. Drizzle ORM abstracts the difference — same schema, same queries. Clear boundary: local is private, server is shared.
- **Cons:** Two database engines to know. Sync logic still hand-rolled (but simpler — server is authoritative). PostgreSQL requires operational care (but not until cloud deploy — SQLite is fine for local dev).

### C: Local-First with CRDT/Sync Engine (ElectricSQL, PowerSync, or Replicache)

Full local-first: SQLite on device, PostgreSQL on server, with a sync layer that handles conflict resolution automatically.

- **Pros:** True offline-first with automatic sync. Conflict resolution built-in. The "gold standard" for local-first apps.
- **Cons:** Adds a sync service dependency (ElectricSQL requires a sync service, PowerSync has its own server). Operational complexity from day one. Agent less familiar with these tools. Overkill for early stage — we don't have multi-device correlation yet (P-7). Locks us into a specific sync vendor/pattern.

### D: PostgreSQL Everywhere (Server-Only, No Local DB)

Farm and Card are thin clients. All data lives on the server. Offline = degraded.

- **Pros:** Single database. No sync. Simple mental model.
- **Cons:** Violates local-first principle. Farm can't work offline. Every recording requires a network round-trip. Privacy: telemetry must transit to server. Non-starter.

## Decision

**Option B: SQLite Local + PostgreSQL Server (Hybrid), with Drizzle ORM as the abstraction layer.**

| Domain | Database | Rationale |
|--------|----------|-----------|
| **Farm** | SQLite (via `expo-sqlite` or `op-sqlite`) | Embedded, zero-config, works offline. Stores recordings metadata, pending attributions, telemetry cache. |
| **Card** | SQLite (via `expo-sqlite` or `op-sqlite`) | Embedded, zero-config. Stores identity keypair, claimed points, cached feed. |
| **Backend (local dev)** | SQLite (via Bun native or Turso/libSQL) | Zero setup. `bun run dev` just works. Identical Drizzle schema. |
| **Backend (production)** | PostgreSQL (via Turso Cloud or Fly Postgres) | Multi-user concurrency, backups, scaling. Drizzle migration is a connection string change. |

| Concern | Approach |
|---------|----------|
| **ORM** | Drizzle ORM — type-safe, SQL-like DX, same schema for SQLite and PostgreSQL |
| **Migrations** | Drizzle Kit — generates SQL migrations, runs via CLI/CI |
| **Sync** | Explicit REST API (Hono RPC). Farm pushes attributions; Card pulls feed. No magic sync engine. |
| **Conflict resolution** | Server is authoritative. Last-write-wins for simple fields. Attribution conflicts (duplicate uploads) resolved by event correlation (P-7). |
| **Offline queue** | Farm stores pending uploads in SQLite. Retries with exponential backoff when online. |
| **Local privacy** | Telemetry (face vectors, IP, precise location) never leaves SQLite unless user explicitly shares an attribution. |

## Rationale

1. **SQLite is the right local database.** Embedded, zero-config, fast, well-supported on React Native (`expo-sqlite`, `op-sqlite`). No server process, no network, no auth — perfect for offline-first mobile.

2. **PostgreSQL is the right server database.** Mature, well-understood, great concurrency, rich ecosystem. We don't need it yet — SQLite on the backend during local dev is fine — but the migration path is trivial with Drizzle.

3. **Drizzle ORM abstracts the difference.** Same schema definition, same query API, same migration tooling. Switching from SQLite to PostgreSQL is a connection string change. No code changes in queries or models.

4. **No sync engine (yet).** CRDT-based sync (ElectricSQL, PowerSync) is powerful but adds operational complexity we don't need before P-7 (multi-device correlation). Explicit REST sync is simpler, more transparent, and sufficient for single-device-per-user flows. We can adopt a sync engine later if conflict rates become unmanageable.

5. **Privacy boundary is the network call.** Telemetry stays in local SQLite. Only user-explicitly-shared data (attribution: "I give Alice +5 aura for that speech") crosses the network. The database architecture enforces this — there's no background sync of raw telemetry.

6. **Aligns with ADR-003.** Backend stack decision already assumed SQLite → PostgreSQL with Drizzle. This ADR formalizes that assumption and extends it to Farm and Card.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| SQLite concurrency on backend (local dev) | Single-user local dev — no concurrency issue. Production uses PostgreSQL. |
| Drizzle ORM maturity | Drizzle is production-used, well-maintained, and has good Bun support. Fallback: Prisma (heavier but more mature). |
| Hand-rolled sync has bugs | Start simple. Offline queue with retry. Server is authoritative — client conflicts resolve by accepting server state. Add CRDT/sync engine only if this becomes painful. |
| React Native SQLite performance with large media metadata | Media files stored on filesystem, not in DB. SQLite stores only metadata (JSON rows). Index on timestamps and user IDs. |
| Schema drift between local and server | Drizzle migrations are the single source of truth. Same migration runs on local SQLite and server PostgreSQL. Shared types package (`@aura/shared`) enforces API contract. |

## Consequences

- Farm and Card each have a local SQLite database, created on first launch
- Backend uses SQLite for local dev (`bun run dev`), PostgreSQL for production
- Drizzle schema definitions live in `aura-apps/packages/db/` (shared between all three)
- Migrations generated via `drizzle-kit` and committed to the repo
- Sync is explicit: Farm calls `POST /attributions`, Card calls `GET /feed`
- No background sync daemon, no CRDT, no conflict-free replicated data types
- This decision can be revisited at P-7 (multi-device correlation) if sync complexity demands it
- ADR-005 (Identity) and ADR-006 (API Protocol) can now reference this database strategy
