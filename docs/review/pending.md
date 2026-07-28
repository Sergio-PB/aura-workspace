# Aura — Decisions Pending CTO Review

> **Status key:** `pending` = awaiting review | `approved` = signed off | `rejected` = vetoed
> 
> Pulse MUST check this file before working on any item that depends on an unapproved decision.
> If a decision is `pending`, do NOT implement follow-up work. Write the ADR, then wait.

---

## Active Reviews

<!-- Add new decisions below. Format:
### [DATE] Decision Title
- **What:** [one-line summary]
- **Why:** [rationale]
- **Blocks:** [what can't proceed until approved]
- **Status:** pending
-->

_No decisions pending review._

### 2026-07-27: Farm Platform Pivot — Web SPA + Capacitor (cross-platform)

- **What:** Pivot The Farm from React Native (mobile-only) to Web SPA + Capacitor (mobile + web + VR via WebXR). One TypeScript codebase everywhere.
- **Why:** React Native can't run on VR headsets or as a web SPA. New requirement: Farm must work on Meta Quest, Ray-Ban Meta (as camera source), desktop web, and mobile. Web SPA + Capacitor gives native camera on mobile, WebXR for VR, and web for everything else.
- **Blocks:** All Farm development (P-3 through P-8). Current React Native Farm code (~15 commits) would be rewritten. Card can also become a web SPA.
- **Status:** pending
- **ADR:** docs/adr/ADR-008-farm-platform-pivot.md

---

## Resolved

<!-- Approved or rejected decisions move here -->

