# Aura Public API — v1

> **Status:** Live (N-3)
> **Base URL:** `https://api.ifarm.club` (production) / `http://localhost:3000` (local dev)
> **Auth:** Bearer token (JWT or API key)

Third-party integrations use API keys for programmatic access. API keys are scoped to a user and inherit their permissions. Create and manage keys at `POST /api-keys`.

---

## Authentication

### API Key Auth

```
Authorization: Bearer <64-char-hex-api-key>
```

API keys get a higher rate limit (100 req/min vs 60 for JWT). Keys are SHA-256 hashed at rest — the raw key is shown only once at creation.

### JWT Auth

```
Authorization: Bearer <jwt-token>
```

Obtained via `POST /auth/login` or `POST /auth/register`.

---

## Endpoints

### Health

```
GET /health
```

```json
{ "ok": true, "data": { "status": "healthy" } }
```

No auth required.

---

### Users

#### List users
```
GET /users
```
Public. Returns all users (id + displayName).

```json
{
  "ok": true,
  "data": {
    "users": [
      { "id": "uuid", "displayName": "Alice" }
    ]
  }
}
```

#### Get user profile
```
GET /users/:id
```
Auth required. Returns full profile + stats.

```json
{
  "ok": true,
  "data": {
    "id": "uuid",
    "displayName": "Alice",
    "publicKey": "ed25519:...",
    "stats": {
      "totalAura": 1234,
      "maxStreak": 42,
      "maxCombo": 5,
      "maxEgo": 3,
      "sessionsCompleted": 15
    }
  }
}
```

---

### Leaderboard

#### Global leaderboard
```
GET /leaderboard
```
Public. Top 50 users by total aura points.

```json
{
  "ok": true,
  "data": {
    "leaderboard": [
      { "rank": 1, "userId": "uuid", "displayName": "Alice", "totalAura": 5000 }
    ]
  }
}
```

#### User rank
```
GET /leaderboard/user/:userId
```
Public. Single user's rank + stats.

---

### Feed

#### Get feed
```
GET /feed?userId=<uuid>&limit=50&cursor=<timestamp>
```
Public. Chronological feed of attributed points. Cursor-based pagination.

```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "fromUser": { "id": "uuid", "displayName": "Bob" },
        "toUser": { "id": "uuid", "displayName": "Alice" },
        "points": 24,
        "move": "seesaw",
        "timestamp": 1723000000000
      }
    ],
    "cursor": "1723000000000"
  }
}
```

---

### Attributions

#### List attributions
```
GET /attributions?toUserId=<uuid>&fromUserId=<uuid>&eventId=<uuid>&limit=50
```
Auth required. Filter by target, source, or event.

#### Create attribution
```
POST /attributions
```
Auth required. Rate limited (60/min).

```json
// Request
{
  "toUserId": "uuid",
  "eventId": "uuid",
  "points": 24,
  "move": "seesaw",
  "note": "crushed it"
}

// Response (201)
{ "ok": true, "data": { "id": "uuid", "points": 24 } }
```

---

### Validations

#### Get consensus for an attribution
```
GET /validations/attributions/:id/consensus
```
Auth required.

```json
{
  "ok": true,
  "data": {
    "attributionId": "uuid",
    "confirms": 5,
    "challenges": 1,
    "consensus": "confirmed",
    "threshold": 3,
    "validators": [
      { "userId": "uuid", "displayName": "Carol", "decision": "confirm", "reason": "I was there" }
    ]
  }
}
```

#### Submit validation
```
POST /validations
```
Auth required. Rate limited (60/min).

```json
// Request
{
  "attributionId": "uuid",
  "decision": "confirm",
  "reason": "I saw it happen"
}

// Response (201)
{ "ok": true, "data": { "id": "uuid", "decision": "confirm" } }
```

---

### Events

#### List events
```
GET /events
```
Public. Returns active/recent events.

#### Create event
```
POST /events
```
Auth required.

```json
// Request
{ "name": "Friday Game Night", "location": { "lat": 40.7, "lng": -74.0 } }

// Response (201)
{ "ok": true, "data": { "id": "uuid", "name": "Friday Game Night" } }
```

#### Join event
```
POST /events/:id/join
```
Auth required. Registers user for cross-device correlation.

---

### Sessions

#### Start session
```
POST /sessions
```
Auth required. Begins a move-streaming session.

```json
// Request
{ "targetUserId": "uuid", "eventId": "uuid" }

// Response (201)
{ "ok": true, "data": { "sessionId": "uuid" } }
```

#### End session
```
POST /sessions/:id/end
```
Auth required. Finalizes points. Requires ≥30 ticks (~3s) for points to count.

```json
{ "ok": true, "data": { "totalPoints": 240, "ticks": 30 } }
```

---

### Reputation

#### Export reputation
```
GET /reputation/export/:userId
```
Public. Returns a signed Ed25519 attestation of the user's reputation.

```json
{
  "ok": true,
  "data": {
    "userId": "uuid",
    "totalAura": 5000,
    "attestation": "base64-signed-payload",
    "publicKey": "ed25519:...",
    "exportedAt": "2026-08-06T12:00:00Z"
  }
}
```

#### Verify attestation
```
POST /reputation/verify
```
Public. Verifies a signed reputation attestation.

```json
// Request
{ "attestation": "base64-signed-payload", "publicKey": "ed25519:..." }

// Response
{ "ok": true, "data": { "valid": true, "userId": "uuid", "totalAura": 5000 } }
```

#### Get server public key
```
GET /reputation/public-key
```
Public. Returns the server's Ed25519 public key for attestation verification.

---

### Network Health

```
GET /network/health
```
Public. Transparency report — no auth.

```json
{
  "ok": true,
  "data": {
    "totals": {
      "users": 42,
      "events": 15,
      "recordings": 200,
      "attributions": 500,
      "validations": 300,
      "disputes": 5,
      "sessions": 80
    },
    "activity": {
      "activeUsers7d": 20,
      "attributions7d": 50,
      "pointsAwarded7d": 1200,
      "sessionsCompleted7d": 12
    },
    "consensus": {
      "totalValidations": 300,
      "confirmRate": 92.5,
      "challengeRate": 7.5
    },
    "disputes": {
      "open": 1,
      "resolved": 3,
      "dismissed": 1,
      "resolutionRate": 80.0
    },
    "topContributors": [
      { "displayName": "Alice", "totalPoints": 5000 }
    ],
    "growth": {
      "newUsers7d": 5,
      "newUsers30d": 15
    },
    "generatedAt": "2026-08-06T12:00:00.000Z"
  }
}
```

---

### API Keys

#### Create key
```
POST /api-keys
```
Auth required (JWT only — API keys can't create more API keys).

```json
// Request
{ "name": "my-integration" }

// Response (201) — raw key shown only once
{
  "ok": true,
  "data": {
    "id": "uuid",
    "name": "my-integration",
    "key": "a1b2c3d4...64-char-hex...",
    "createdAt": 1723000000000
  }
}
```

#### List keys
```
GET /api-keys
```
Auth required. Returns masked keys (never raw).

```json
{
  "ok": true,
  "data": {
    "keys": [
      { "id": "uuid", "name": "my-integration", "keyPreview": "a1b2c3d4...", "createdAt": 1723000000000, "lastUsedAt": 1723000000000 }
    ]
  }
}
```

#### Revoke key
```
DELETE /api-keys/:id
```
Auth required. Immediate — key stops working on next request.

```json
{ "ok": true, "data": { "revoked": true } }
```

---

## Rate Limits

| Auth method | Limit |
|-------------|-------|
| JWT | 60 requests / 60s window |
| API key | 100 requests / 60s window |

Rate-limited responses return HTTP 429:

```json
{ "ok": false, "error": { "code": "RATE_LIMITED", "message": "Too many requests. Slow down." } }
```

---

## Error Format

All errors follow this shape:

```json
{
  "ok": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description"
  }
}
```

Common codes: `UNAUTHORIZED` (401), `NOT_FOUND` (404), `INVALID_PARAM` (400), `RATE_LIMITED` (429), `ALREADY_REVOKED` (409).

---

## WebSocket: Move Stream

Connect to `wss://api.ifarm.club/ws` (or `ws://localhost:3000/ws`).

### Client → Server (Farm sends move ticks)

```json
{
  "type": "move_tick",
  "sessionId": "uuid",
  "targetUserId": "uuid",
  "move": "seesaw",
  "rate": 0.85,
  "timestamp": 1723000000000
}
```

### Server → Client (leaderboard updates)

```json
{
  "type": "leaderboard_update",
  "leaderboard": [
    { "userId": "uuid", "displayName": "Alice", "totalPoints": 240 }
  ]
}
```

### Session lifecycle

1. `POST /sessions` → get `sessionId`
2. Open WebSocket, send `move_tick` frames at ~10 Hz
3. `POST /sessions/:id/end` → finalize points

---

## Scoring Formula

```
points = Σ (rate × duration_seconds × moveMultiplier)

moveMultiplier:
  seesaw:     10
  wave:        8
  clap:       12
  raise_roof: 15
```

Rate is 0..1 from the move detector. Duration is continuous active time. Minimum 3 seconds (~30 ticks) required for points to count.
