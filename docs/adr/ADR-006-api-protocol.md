# ADR-006: API Protocol

Date: 2026-07-25
Status: proposed

## Context

Aura's backend serves two client types: The Farm (uploads attributions) and The Card (claims points, reads feed). The API protocol choice affects type safety, real-time capabilities, tooling, and agent productivity.

Key requirements:
- Farm → Backend: upload attributions (point assignments with telemetry metadata)
- Card → Backend: claim attributions, read social feed, quick reactions
- Type safety across the stack (Farm, Card, Backend all TypeScript per ADR-002, ADR-003)
- Real-time feed updates (new attributions appear without manual refresh)
- Offline resilience: clients queue operations when disconnected
- Solo developer + agent — minimize boilerplate and codegen

## Options Considered

### A: REST (with Hono RPC)

Standard HTTP methods + JSON. Hono RPC provides end-to-end type safety by sharing Zod schemas between client and server — no codegen, no OpenAPI drift.

- **Pros:** Universal (every HTTP client works), simple mental model, excellent caching (CDN, browser, client-side), Hono RPC gives type-safe clients without codegen, well-understood error semantics (HTTP status codes), easy to debug (curl, browser devtools), aligns with ADR-003 decision
- **Cons:** No built-in real-time (requires SSE/WebSocket side channel), over-fetching/under-fetching possible (mitigated by small API surface), no subscription primitive

### B: GraphQL

Single endpoint, client-specified queries, built-in subscriptions for real-time.

- **Pros:** No over-fetching, built-in subscriptions, strong typing via schema, good tooling (Apollo, GraphiQL)
- **Cons:** Complex server-side (resolvers, N+1 problem, dataloaders), complex client-side (cache normalization, query deduplication), auth at field level adds complexity, heavy for our small API surface, agent less productive with GraphQL patterns, adds a query language to learn

### C: gRPC

Binary protocol with Protobuf schemas, code generation for clients.

- **Pros:** Fast (binary, HTTP/2), strong typing via .proto files, built-in streaming, excellent for service-to-service
- **Cons:** Not browser-friendly (requires gRPC-Web proxy), Protobuf codegen step, harder to debug (binary, not human-readable), overkill for a mobile app → server API, agent less productive, adds build complexity

### D: WebSocket-Only

Persistent bidirectional connection for all communication.

- **Pros:** Real-time by default, low latency, single connection
- **Cons:** No request/response semantics (must build RPC layer on top), no built-in caching, connection state management is complex, reconnection logic is non-trivial, harder to debug, overkill as the sole protocol

## Decision

**REST with Hono RPC for request/response, Server-Sent Events (SSE) for real-time feed updates.**

| Concern | Approach |
|---------|----------|
| **Request/Response** | REST via Hono RPC. Type-safe, cacheable, simple. |
| **Real-time** | SSE endpoint (`GET /feed/events`) for new attributions and reactions. |
| **Type safety** | Zod schemas in `@aura/shared` package. Hono RPC shares types automatically. |
| **Offline** | Clients queue operations locally (SQLite), replay on reconnect. REST is naturally retry-friendly. |
| **Auth** | Ed25519 signature in `Authorization` header. Public key identifies user; signature proves ownership. |
| **Versioning** | URL prefix (`/v1/...`). Hono RPC handles versioned clients. |

### API Surface (v1)

```
POST   /v1/attributions          — Farm uploads a point attribution
GET    /v1/attributions          — List attributions (filtered by target, event, etc.)
GET    /v1/attributions/:id      — Single attribution detail
POST   /v1/attributions/:id/claim    — Card claims an attribution
POST   /v1/attributions/:id/confirm  — Community member confirms attribution
POST   /v1/attributions/:id/challenge — Community member challenges attribution
POST   /v1/attributions/:id/reactions — Quick reaction (emoji) on attribution
GET    /v1/feed                  — Card's social feed (paginated)
GET    /v1/feed/events           — SSE stream of new feed items
GET    /v1/users/:publicKey      — Public profile
PUT    /v1/users/:publicKey      — Update display name, avatar
GET    /v1/events                — List events
POST   /v1/events                — Create event
POST   /v1/events/:id/join      — Join event
```

## Rationale

1. **REST is the right default.** Our API surface is small and resource-oriented. REST maps naturally: attributions, users, events, feed. No need for query language flexibility — clients always need the same shapes.

2. **Hono RPC eliminates the main REST criticism.** The traditional REST pain point is type drift between client and server. Hono RPC solves this: Zod schemas in `@aura/shared` are the single source of truth. Client gets `client.attributions.$post({...})` with full type inference. No codegen, no OpenAPI spec to maintain.

3. **SSE is simpler than WebSocket for one-way real-time.** The feed is a one-way stream (server → client). SSE is native HTTP, auto-reconnects, works through proxies, and is trivial to implement in Hono (`stream()` helper). WebSocket would be overkill — we don't need bidirectional streaming for feed updates.

4. **GraphQL is too much for our needs.** Our API has ~12 endpoints. GraphQL's flexibility (client-specified queries) solves a problem we don't have — our clients always need the same data shapes. The complexity cost (resolvers, dataloaders, cache normalization) isn't justified.

5. **gRPC is wrong for mobile → server.** gRPC shines in service-to-service communication. For mobile clients, it requires gRPC-Web (a proxy), adds a Protobuf build step, and makes debugging harder. The performance gains are negligible for our payload sizes (small JSON attribution objects).

6. **Aligns with ADR-003.** The backend stack decision already assumed REST + Hono RPC. This ADR formalizes that choice and extends it with SSE for real-time.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| SSE not supported in all environments | SSE is standard HTTP — works everywhere. React Native has EventSource polyfills. |
| REST over-fetching for feed | Feed endpoint returns exactly what the Card needs. If feed shapes diverge, add query params (`?include=reactions`). |
| Hono RPC is Hono-specific | The underlying protocol is standard REST. If we ever leave Hono, the API doesn't change — only the RPC client. |
| Real-time at scale (many concurrent SSE connections) | SSE is connection-per-client. For early user counts (N-1: founding community), this is fine. At scale (P-10), add a pub/sub layer (Redis) behind the SSE endpoint. |

## Consequences

- All API endpoints are RESTful, versioned under `/v1/`
- Type-safe client via Hono RPC — shared Zod schemas in `@aura/shared`
- Real-time feed via SSE (`GET /v1/feed/events`)
- No GraphQL, no gRPC, no WebSocket (except possibly for future bidirectional features)
- Auth via Ed25519 signature header — no sessions, no cookies, no OAuth tokens
- Offline queue in local SQLite, replay via REST on reconnect
- This decision can be revisited if API complexity grows significantly (unlikely before P-10)

## Alternatives Not Chosen

- **GraphQL:** Too complex for our API surface. Adds resolver, dataloader, and cache normalization overhead we don't need.
- **gRPC:** Wrong fit for mobile clients. Requires gRPC-Web proxy and Protobuf build step.
- **WebSocket-only:** Overkill. We need request/response for most operations. SSE covers the one real-time need.
- **tRPC:** Excellent but tightly coupled to Next.js/React. Hono RPC gives the same end-to-end type safety without framework lock-in.

## References

- ADR-002: Farm Platform (React Native)
- ADR-003: Backend Stack (TypeScript/Hono/Bun)
- ADR-004: Database & Sync (SQLite local + PostgreSQL server)
- ADR-005: Identity Model (Ed25519 keypairs)
- [Hono RPC](https://hono.dev/docs/guides/rpc)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Zod](https://zod.dev/)
