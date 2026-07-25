# ADR-003: Backend Stack

Date: 2026-07-25
Status: proposed

## Context

Aura's backend connects Farms (capture) to Cards (identity/feed). It must validate attributions, deliver feeds, and manage user identity. The backend is built by a solo founder + autonomous agent (OpenCode with Caveman model).

Key requirements:
- Validate point attributions (same-IP correlation, temporal proximity, community consensus)
- Serve social feeds to Card clients
- Manage user identity and authentication
- Store recordings metadata, attributions, validations
- Admin dashboard (minimal)
- Eventual multi-device correlation (P-7), community validation (P-8)

Constraints:
- Single developer (Sergio) + Aura Agent (OpenCode)
- Agent most productive in TypeScript
- Farm is React Native/TypeScript (ADR-002) — shared types desirable
- No cloud infra yet — local dev on M1 Pro
- Privacy-by-design: telemetry processed on-device, backend stores only what users choose to share

## Options Considered

### A: TypeScript / Node.js (Express, Fastify, or Hono)

- **Pros:** Same language as Farm (shared types, shared validation), agent highly productive, massive ecosystem, well-documented patterns, easy to hire for later, Hono is lightweight and fast on Bun/Node, Fastify has great DX and plugin system
- **Cons:** Single-threaded (mitigated by clustering/workers), less performant than Go/Rust for CPU-bound work (not our bottleneck — I/O heavy), npm ecosystem has supply-chain risk

### B: Python (FastAPI or Django)

- **Pros:** Great for ML/validation logic, FastAPI has excellent DX, large ecosystem, good for prototyping
- **Cons:** Different language from Farm (no shared types), agent less productive in Python than TypeScript, slower runtime, GIL limits concurrency, two-language codebase increases cognitive overhead

### C: Go

- **Pros:** Fast, simple, great concurrency, single binary deploy, excellent for API servers
- **Cons:** Different language from Farm, agent less productive, smaller web ecosystem (more boilerplate), type sharing requires codegen (OpenAPI/Protobuf), steeper learning curve for founder

### D: Rust (Axum or Actix)

- **Pros:** Fastest, safest, great for long-running services
- **Cons:** Different language, steepest learning curve, agent least productive, slowest iteration speed, overkill for an I/O-bound CRUD API, hardest to hire for

## Decision

**TypeScript with Hono on Bun runtime.**

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Runtime** | Bun | Fast startup, native TypeScript, built-in test runner, SQLite, and file APIs. Single binary. Drop-in Node compat. |
| **Framework** | Hono | Ultralight (13KB), fast, great DX, Web Standard-based (works on Bun/Node/Cloudflare/Deno), built-in validation (Zod), RPC client for end-to-end type safety |
| **Validation** | Zod | Shared schemas between Farm and Backend. Single source of truth for API contracts. |
| **Database** | SQLite (libSQL/Turso) → PostgreSQL | Start with SQLite via Bun's built-in bindings or Turso for local dev. Migrate to PostgreSQL when cloud deploys. Schema stays the same (Drizzle ORM). |
| **ORM** | Drizzle | Type-safe, lightweight, SQL-like DX, works with SQLite and PostgreSQL, good Bun support |
| **Auth** | Lucia (or simple JWT) | Lightweight, framework-agnostic, works with Bun |
| **API Style** | REST (with Hono RPC for type-safe client) | Simpler than GraphQL for our use case, Hono RPC gives end-to-end types without codegen |
| **Real-time** | Server-Sent Events (SSE) or WebSocket via Hono | For feed updates. Start simple, scale when needed. |

## Rationale

1. **One language across the stack.** Farm (React Native) and Backend both TypeScript. Shared types package (`@aura/shared`) for API contracts, telemetry models, validation schemas. No codegen, no drift.

2. **Agent productivity.** OpenCode with Caveman model is most productive in TypeScript. Well-known patterns, large training corpus, fast iteration.

3. **Bun over Node.** Faster startup (important for serverless/edge later), native TypeScript (no ts-node/tsx needed), built-in SQLite (no separate DB for local dev), built-in test runner. If Bun proves unstable, fallback to Node is trivial — Hono runs on both.

4. **Hono over Express/Fastify.** Web Standard-based (future-proof), ultralight, built-in Zod integration, RPC client for end-to-end types. Express is legacy; Fastify is good but heavier. Hono is the right size for our API surface.

5. **SQLite-first, PostgreSQL-later.** No cloud infra yet. SQLite (via Bun or Turso) gives us a real database with zero setup. Drizzle ORM abstracts the difference — migration to PostgreSQL is a config change, not a rewrite. This aligns with "local-first" philosophy.

6. **REST + RPC over GraphQL.** Our API surface is simple (upload attribution, claim points, read feed). GraphQL adds complexity (caching, N+1, auth at field level) we don't need. Hono RPC gives type-safe clients without the GraphQL overhead.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Bun is younger/less proven than Node | Hono runs on Node too — fallback is a one-line runtime change. Start with Bun, monitor stability. |
| SQLite concurrency limits | Single-writer model is fine for early user count. Turso (libSQL) adds read replicas if needed. PostgreSQL migration path is clear. |
| Hono ecosystem smaller than Express | Hono covers our needs (routing, validation, middleware, RPC). If we hit a gap, Fastify is the fallback. |
| Shared types create coupling between Farm and Backend | Version the shared package. Farm can run offline without backend. Types are a convenience, not a runtime dependency. |

## Consequences

- Backend code lives in `aura-apps/apps/backend/` within the monorepo
- Shared types in `aura-apps/packages/shared/`
- All backend code is TypeScript
- Local dev: `bun run dev` starts the API with SQLite
- CI/CD: Bun-based test/lint/build in GitHub Actions
- Cloud deploy: Bun binary on Fly.io or VPS (single binary, no Docker needed initially)
- ADR-004 (Database) and ADR-005 (Identity) can now be written with this stack context
