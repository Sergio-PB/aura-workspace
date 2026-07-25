# ADR-007: Cloud Provider

Date: 2026-07-25
Status: proposed

## Context

Aura currently has no cloud infrastructure — everything runs on the founder's M1 Pro. The backend (P-5) will need a production host. The Farm and Card are local-first, so the backend is the only cloud dependency for the foreseeable future.

Key requirements:
- Host a TypeScript/Node.js backend (Hono or Fastify, per ADR-003)
- Serve API traffic for Farms (upload attributions) and Cards (claim points, read feed)
- Store media metadata (recordings, attributions, validations) — actual media may stay on-device or use object storage later
- Low operational overhead (solo founder + agent, no DevOps team)
- Free tier or very low cost for bootstrap phase
- PostgreSQL for server-side data (per ADR-004), SQLite for local dev
- Eventual scaling: multi-region for P-7 (multi-device correlation), real-time feeds

Constraints:
- Bootstrapped, no funding
- Solo developer (Sergio) + Aura Agent (OpenCode)
- No cloud infra yet — greenfield choice
- Privacy-by-design: user data stays on-device by default, backend stores minimal metadata

## Options Considered

### A: Fly.io

- **Pros:** Simple `fly deploy` from Dockerfile, auto-scaling, free tier (3 shared VMs), PostgreSQL managed offering, global edge deployment (deploy close to users), great for Node.js, minimal config, good docs, built for indie devs
- **Cons:** Smaller ecosystem than AWS, fewer managed services (no object storage — would need S3-compatible external service), cold starts on free tier, less enterprise tooling

### B: Railway

- **Pros:** Excellent DX, GitHub integration, zero-config deploys, PostgreSQL included, usage-based pricing, good for prototypes
- **Cons:** No free tier (starts at $5/mo), US-only regions (latency for non-US users), less control over infrastructure, vendor lock-in risk

### C: Vercel + Supabase/Neon

- **Pros:** Vercel is great for frontend, Supabase/Neon for PostgreSQL, generous free tiers, edge functions
- **Cons:** Vercel's serverless model is awkward for long-running WebSocket connections (real-time feeds), cold starts, vendor lock-in across two services, edge functions have runtime limits

### D: AWS (EC2, RDS, S3)

- **Pros:** Industry standard, every service imaginable, generous free tier (12 months), no vendor lock-in concerns, S3 for media storage
- **Cons:** Massive operational overhead, complex IAM, steep learning curve, overkill for bootstrap, easy to rack up unexpected bills, DevOps burden on solo founder

### E: Defer decision until P-5

- **Pros:** No premature commitment, can evaluate options with real code and real requirements, avoids analysis paralysis now
- **Cons:** Delays infrastructure setup, may need to refactor if assumptions change, no CI/CD pipeline for backend until decision is made

## Decision

**Defer the final decision until P-5 (Backend Core), with Fly.io as the strong default recommendation.**

Rationale:
1. We don't need cloud until P-5. The Farm (P-3) and Card (P-4) are local-first and can be built entirely on-device.
2. Fly.io aligns with our constraints: free tier, simple deploy, PostgreSQL, global edge, minimal ops. It's the "lazy" choice — least code to write, least config to maintain.
3. If Fly.io proves insufficient at P-5 time (e.g., we need S3-compatible storage, or real-time WebSocket scaling is poor), we can re-evaluate with real requirements.
4. The ADR exists to document the reasoning and default, so the decision isn't made from scratch at P-5.

**Default:** Fly.io for backend hosting + Fly Postgres for database. Object storage (for media) deferred to P-10 — media stays on-device through P-6.

## Consequences

- **Positive:** No cloud bill until P-5. No infrastructure to maintain during P-2/P-3/P-4. Clean separation: local-first products built first, cloud added when needed.
- **Negative:** CI/CD pipeline (P-2) won't have a production target until P-5. Landing page (ifarm.club) still needs hosting — but that's a static site, deployable to GitHub Pages or similar without a full cloud provider decision.
- **Risk:** If Fly.io's free tier or PostgreSQL offering changes before P-5, we re-evaluate. Mitigation: this ADR is revisited at P-5 kickoff.

## Revisit Trigger

Re-evaluate at P-5 kickoff. If Fly.io still meets requirements, adopt it. If not, run a fresh ADR with real constraints from P-3/P-4 implementation experience.
