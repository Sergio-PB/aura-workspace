# ADR-009: Media Storage & CDN

Date: 2026-07-30
Status: proposed

## Context

Aura's backend needs to store and serve media: recording thumbnails, user avatars, and potentially short video clips. The architecture doc (2026-07-25) already references Tigris as the media storage layer, but no formal decision has been documented.

Key requirements:
- Store user-uploaded media (avatars, thumbnails, short clips)
- Serve media efficiently to mobile clients (Farm, Card)
- Low operational overhead (solo founder + agent)
- Free tier or very low cost for bootstrap phase
- S3-compatible API (standard, portable, no vendor lock-in)
- CDN for global delivery (users anywhere, not just US)
- Privacy: media is user-controlled, deletable, not publicly accessible by default

Constraints:
- Bootstrapped, no funding
- Backend hosted on Fly.io (ADR-007)
- No Docker installed on M1 Pro (flyctl installed but not authed)
- Media volume at bootstrap: low (dozens of users, hundreds of recordings)

## Options Considered

### A: Tigris (Fly.io native, S3-compatible)

- **Pros:** Built into Fly.io (no separate account), S3-compatible API, automatic CDN (global edge caching), free tier (5 GB storage, 25 GB egress), zero-config with Fly.io apps, designed for indie devs, same billing as Fly.io
- **Cons:** Smaller ecosystem than AWS S3, less tooling, vendor lock-in to Fly.io (mitigated by S3-compatible API — can migrate to any S3 provider), newer service (GA 2024)

### B: Cloudflare R2

- **Pros:** Zero egress fees (huge for media serving), S3-compatible API, global CDN (Cloudflare network), generous free tier (10 GB storage), well-established, great docs
- **Cons:** Separate account from Fly.io, another vendor to manage, free tier has rate limits, not Fly.io native (adds latency hop)

### C: AWS S3 + CloudFront

- **Pros:** Industry standard, infinite scale, every tool supports it, mature CDN
- **Cons:** Egress fees (expensive for media), complex IAM, separate AWS account, operational overhead, overkill for bootstrap, easy to rack up unexpected bills

### D: Backblaze B2 + Cloudflare

- **Pros:** Very cheap storage ($6/TB/month), free egress via Bandwidth Alliance with Cloudflare, S3-compatible API
- **Cons:** Two vendors to manage (B2 + Cloudflare), not Fly.io native, more moving parts

### E: Local filesystem on Fly Machine

- **Pros:** Zero additional services, simplest possible, no egress fees (served by Fly proxy)
- **Cons:** Ephemeral storage (lost on deploy/restart), doesn't scale beyond one machine, no CDN, no redundancy, not suitable for production

## Decision

**Tigris (Fly.io native, S3-compatible).**

Rationale:
1. We're already on Fly.io (ADR-007). Tigris is the path of least resistance — same account, same billing, zero additional config.
2. S3-compatible API means zero vendor lock-in. If Tigris doesn't work out, we swap the S3 endpoint URL and keep the same code.
3. Free tier (5 GB storage, 25 GB egress/month) is more than enough for bootstrap. At 100 KB per thumbnail and 50 KB per avatar, that's ~30,000 media objects before hitting the free tier.
4. Automatic CDN — no separate CDN config needed. Tigris edges cache globally.
5. The architecture doc already references Tigris. This ADR formalizes that choice.

**What we store:**
- User avatars (small, ~50 KB, public)
- Recording thumbnails (small, ~100 KB, public)
- Short video clips (optional, future — stay on-device for now)

**What we DON'T store (privacy-by-design):**
- Raw video recordings (stay on-device, per privacy architecture)
- Face vectors, hand positions, raw telemetry (never leave device)
- Full-resolution media (thumbnails only)

## Implementation Plan

1. Add `@aws-sdk/client-s3` (or lighter `@aws-sdk/s3-request-presigner`) to backend deps
2. Create `src/media.ts` module: upload, getSignedUrl, delete
3. Add `POST /media/upload` endpoint (multipart, auth-required)
4. Add `GET /media/:key` proxy or use Tigris public URLs directly
5. Add `DELETE /media/:key` for user-controlled deletion (GDPR compliance)
6. Update `recordings` table: add `thumbnail_key` column
7. Update `users` table: `avatar_url` → point to Tigris URL

**ponytail:** Single `media.ts` module with three functions (upload, getUrl, delete). No abstraction layer — S3-compatible API IS the abstraction. Swap endpoint URL to migrate providers.

## Consequences

- **Positive:** Zero-config media storage on Fly.io. S3-compatible = portable. Free tier covers bootstrap. CDN included.
- **Negative:** Another Fly.io service dependency. If Fly.io has an outage, both backend AND media are down. Mitigation: S3-compatible API means we can fail over to Cloudflare R2 or AWS S3 by changing one env var.
- **Risk:** Tigris is newer than AWS S3. Mitigation: S3-compatible API is the escape hatch. We're not using Tigris-specific features.

## Revisit Trigger

Re-evaluate if:
- Media volume exceeds Tigris free tier (5 GB storage or 25 GB egress/month)
- Tigris has a significant outage or reliability issue
- We need features Tigris doesn't support (e.g., video transcoding, advanced CDN rules)
