# Aura — Decisions Pending CTO Review

> **Status key:** `pending` = awaiting review | `approved` = signed off | `rejected` = vetoed
> 
> Pulse MUST check this file before working on any item that depends on an unapproved decision.
> If a decision is `pending`, do NOT implement follow-up work. Write the ADR, then wait.

---

## Active Reviews

### 2026-07-30: Media Storage & CDN — Tigris (Fly.io native, S3-compatible)

- **Status:** pending
- **What:** Formalize media storage choice. Tigris (S3-compatible, Fly.io native, free tier: 5 GB storage + 25 GB egress). Portable via S3 API.
- **ADR:** docs/adr/ADR-009-media-storage.md

---

## Resolved

### 2026-07-27: Farm Platform Pivot — Web SPA + Capacitor (cross-platform)

- **Status:** approved
- **What:** Pivot The Farm from React Native (mobile-only) to Web SPA + Capacitor (mobile + web + VR via WebXR). One TypeScript codebase everywhere.
- **ADR:** docs/adr/ADR-008-farm-platform-pivot.md
