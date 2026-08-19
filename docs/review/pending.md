# Aura — Decisions Pending CTO Review

> **Status key:** `pending` = awaiting review | `approved` = signed off | `rejected` = vetoed
> 
> Pulse MUST check this file before working on any item that depends on an unapproved decision.
> If a decision is `pending`, do NOT implement follow-up work. Write the ADR, then wait.

---

## Active Reviews

### 2026-08-19: Authenticate the P-16 Move Stream (WebSocket + Session Finalize)

- **Status:** pending
- **What:** The P-16 move stream (WS identify + move_tick + `POST /sessions/:id/end`) is entirely unauthenticated — anyone can award aura points to any user. Fix requires the Farm client to gain a keypair + login flow (currently absent), so it's a product decision, not a mechanical fix.
- **ADR:** docs/adr/ADR-011-move-stream-auth.md

---

### 2026-08-13: Legal Structure — Single-Member LLC

- **Status:** pending
- **What:** Formalize Aura as a single-member LLC. Unblocks bank account, vendor contracts, app store publishing, and liability protection.
- **ADR:** docs/adr/ADR-010-legal-structure.md
- **Recommendation:** docs/company/legal-structure-recommendation.md

---

## Resolved

### 2026-07-30: Media Storage & CDN — Tigris (Fly.io native, S3-compatible)

- **Status:** approved
- **What:** Formalize media storage choice. Tigris (S3-compatible, Fly.io native, free tier: 5 GB storage + 25 GB egress). Portable via S3 API.
- **ADR:** docs/adr/ADR-009-media-storage.md

### 2026-07-27: Farm Platform Pivot — Web SPA + Capacitor (cross-platform)

- **Status:** approved
- **What:** Pivot The Farm from React Native (mobile-only) to Web SPA + Capacitor (mobile + web + VR via WebXR). One TypeScript codebase everywhere.
- **ADR:** docs/adr/ADR-008-farm-platform-pivot.md
