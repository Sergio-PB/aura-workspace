# ADR-011: Authenticate the P-16 Move Stream (WebSocket + Session Finalize)

> **Status:** pending
> **Date:** 2026-08-19
> **Author:** Aura Agent

## Context

The P-16 "Feed MVP" move stream is the core aura-points mechanic: a Farm device
streams hand/pose detections over a WebSocket, the server translates them into
points, and a live leaderboard updates. The entire path is currently
**unauthenticated**:

1. **WS identify** (`serve.ts`): the client's first message is plaintext
   `{ userId }`. The server binds `ws.data.userId` with no token or signature
   verification — any client can claim to be any user.
2. **WS move_tick** (`ws.ts` `handleMoveTick`): trusts client-supplied
   `userId` (recorder) and `targetUserId` (points recipient) with no auth. A
   malicious client can award points to *any* user by setting `targetUserId`,
   or spoof the recorder to evade anomaly detection. The `rate` clamp (pulse
   #54) fixed numeric bounds but not identity.
3. **REST finalize** (`sessions.ts` `POST /sessions/:id/end`): no
   `authMiddleware`. The comment in `sessions-auth.test.ts` claims "sessionId
   is the secret", but a sessionId is a client-generated `crypto.randomUUID()`
   sent in plaintext over the WS and in the URL — it is not a secret. Any
   unauthenticated caller who knows a sessionId can finalize (or prematurely
   end) another user's session, mutating `activeSessions` and persisting
   points.

This is the 32nd latent-bug class in the ongoing audit, and the most
consequential: it makes the product's core mechanic (fair attribution of aura
points) trivially gameable. The prior identity-spoofing fixes (pulses #50/#53/
#64) covered the REST create/resolve/claim routes but explicitly scoped out the
streaming path ("the WS tick handler parses raw JSON with no schema validation
at all" — pulse #54).

## Decision

**Authenticate the move stream end-to-end, using the existing Ed25519 + JWT
identity model (ADR-005).**

Concretely:

1. **WS identify carries a JWT.** The client's first WS message becomes
   `{ token }` (the JWT from `POST /auth/login`), not `{ userId }`. The server
   verifies the token and derives `userId` from it — never from the client.
2. **move_tick drops the client-supplied `userId`.** The recorder identity
   comes from the authenticated `ws.data.userId`. `targetUserId` remains
   client-supplied (it's the *recipient* selection, not an identity claim) but
   is validated to exist and not be soft-deleted.
3. **`POST /sessions/:id/end` requires `authMiddleware`** and verifies the
   session's recorder matches the authenticated user. The session state must
   track `recorderUserId` (currently it does not).

## Rationale

- **The identity model already exists.** ADR-005 chose Ed25519 keypairs; the
  backend already issues JWTs (`signToken`) and the Card already holds one.
  No new crypto or dependency is needed.
- **The Farm is the gap.** The Farm client currently has *no auth flow at all*
  ("MVP identity — localStorage UUID, no auth" — `RecordScreen.tsx`). It must
  gain a keypair + login before it can authenticate its stream. This is the
  real work and the reason this is a decision, not a mechanical fix.
- **Defense-in-depth, not a rewrite.** The `rate` clamp, anti-gaming, and
  device-anomaly checks all remain; this adds the missing identity layer
  beneath them.

## Alternatives Considered

| Option | Rejected Because |
|--------|-----------------|
| Leave the stream unauthenticated (MVP shortcut) | The core mechanic is gameable — anyone can award themselves points. Not acceptable even for a soft launch. |
| Authenticate only the REST finalize route | The WS tick path is the actual point-awarding surface; securing only finalize leaves the stream open. |
| Shared secret / device token instead of JWT | Reinvents ADR-005; the JWT + Ed25519 model already exists and the Card already uses it. |

## Consequences

- **Positive:** The aura-points mechanic becomes trustworthy; identity spoofing
  on the stream is closed; consistent with the REST identity-spoofing fixes.
- **Negative:** The Farm client must gain a keypair + login flow (new work,
  currently absent). The WS protocol changes (breaking change to the identify
  message shape).
- **Risk:** Low — the Card already demonstrates the auth pattern; the Farm
  change is additive.

## Next Steps (after approval)

1. Farm client: generate an Ed25519 keypair, register/login, hold the JWT.
2. Farm `useFarmWebSocket`: send `{ token }` on open; drop `userId` from ticks.
3. Backend `serve.ts`: verify the JWT on identify; derive `userId`.
4. Backend `ws.ts`: track `recorderUserId`; ignore client `userId` on ticks.
5. Backend `sessions.ts`: `authMiddleware` + recorder-ownership check on end.
6. Regression tests: unauthenticated WS identify rejected; spoofed
   `targetUserId`/`userId` rejected; unauthenticated session finalize rejected.
