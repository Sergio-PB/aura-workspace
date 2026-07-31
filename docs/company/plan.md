# Aura — Company Plan & Roadmap

> **Status:** Draft v2
> **Author:** Aura Agent (autonomous operator)
>
> Aura does not use deadlines or due dates. Milestones are sequenced by dependency, not by calendar. We ship when the work is done.

---

## Vision

A fair community where social reputation is earned through real-world actions, not manufactured online personas. Points are attributed by people who were actually there — recorded, verified, and validated by community consensus. No algorithms optimizing for engagement. No bots. Just people recognizing people.

## Mission

Launch a social reputation network at `ifarm.club` with two products: **The Farm** (capture the moment) and **The Card** (carry your reputation).

---

## Initiative Tracks

| Prefix | Track | Scope |
|--------|-------|-------|
| **W** | Workspace | Agent autonomy, tooling, cron jobs, self-improvement, infrastructure |
| **C** | Company | Legal, funding, brand, infrastructure, team, operations |
| **P** | Product | The Farm, The Card, backend, shared packages |
| **N** | Network | Community, users, governance, content, growth |

---

## Current State

| Area | Status |
|------|--------|
| Company formation | Bootstrapped |
| Product code | None — design phase |
| Infrastructure | Local dev only (M1 Pro) |
| Team | Founder (Sergio) + Aura Agent (autonomous operator) |
| Domain | `ifarm.club` — registered, no DNS |
| Repos | `aura-workspace` (company brain), `aura-apps` (monorepo) |
| Funding | Bootstrapped |

---

## Roadmap

### W-1: Autonomous Agent Kickoff

**Goal:** The Aura Agent runs autonomously on a 30-minute cadence, self-improving and advancing the roadmap without manual prompting.

- [x] **OpenCode auth** — authenticate `opencode` CLI with provider credentials so the cron can delegate coding tasks
- [x] **Cron job: `aura-pulse`** — runs every 30 minutes. Picks the highest-priority unblocked milestone, works on it via OpenCode (`opencode run`), commits results, reports to founder
- [x] **Cron job: `aura-watchdog`** — monitors system health (disk, memory, git state, agent liveness), alerts on anomalies
- [x] **Cron job: `aura-daily`** — daily briefing to founder: what was done, what's blocked, what's next
- [x] **Self-improvement loop** — after each pulse run, the agent evaluates its own performance and patches skills/memories
- [x] **Workspace health baseline** — disk usage, memory pressure, git cleanliness, cron job health all tracked

**Depends on:** Nothing. This is the agent's own foundation — it must run before it can build anything else.

**Runtime:** Hermes Agent (DeepSeek v4 Pro via ollama-cloud) orchestrating OpenCode v1.18.5 with Caveman model (kavai/Caveman-Library:qwen3-5-2b via local Ollama) for coding tasks. Runs on M1 Pro (16 GB RAM, macOS 14.8.7).

---

### C-1: Company Foundation

**Goal:** Aura exists as a real entity with infrastructure, brand, and operating rhythm.

- [~] Legal structure (LLC, incorporation, or sole proprietorship — decide) — recommendation doc ready: `docs/company/legal-structure-recommendation.md`
- [~] `ifarm.club` DNS + hosting + landing page (landing page built + GitHub Pages workflow ready; DNS setup guide ready: `docs/company/dns-setup.md`; needs: founder to add DNS records + enable Pages in repo Settings)
- [x] Brand identity (logo, colors, typography, voice)
- [~] Company bank account + payment infrastructure — setup guide ready: `docs/company/bank-setup.md`; blocked on legal structure decision
- [x] Operating rhythm: daily agent briefings, weekly founder review
- [x] Compliance baseline: privacy policy, terms of service drafts
- [~] Public presence: GitHub org (or keep private), social accounts, domain email — strategy doc ready: `docs/company/public-presence.md`; blocked on DNS/email setup

**Depends on:** Nothing. This is the starting line.

---

### P-1: Architecture & Tech Stack

**Goal:** Every technical decision is made, documented, and justified before code is written.

- [x] **ADR: Farm platform** — native (Swift/Kotlin) vs React Native vs Flutter vs PWA
- [x] **ADR: Backend stack** — language, framework, runtime
- [x] **ADR: Database & sync** — PostgreSQL vs SQLite vs hybrid local-first
- [x] **ADR: Identity model** — self-sovereign keypairs vs email/phone vs OAuth
- [x] **ADR: API protocol** — REST vs GraphQL vs gRPC vs WebSocket
- [x] **ADR: Cloud provider** — defer until P-5, Fly.io as default (ADR-007)
- [x] System architecture diagram (Farm → Backend → Card)
- [x] Data flow: telemetry capture → upload → validation → attribution → feed
- [x] Database schema (users, events, points, validations)
- [x] Security & privacy architecture

**Depends on:** C-1 (need brand context for tech choices)

---

### P-2: Development Infrastructure

**Goal:** CI/CD, tooling, and dev environment — so every subsequent P-initiative has a clean pipeline.

- [x] Monorepo tooling (Turborepo, Nx, or manual workspaces)
- [x] CI/CD pipelines (GitHub Actions): lint, test, build
- [x] Local dev environment (one-command setup)
- [x] Testing framework + strategy (unit, integration, e2e)
- [x] Code quality: linting, formatting, type checking, pre-commit hooks
- [x] Shared packages: types, API contracts, auth client, telemetry models

**Depends on:** P-1 (need stack decisions)

---

### P-3: The Farm — Core

**Goal:** Local media studio that captures telemetry and attributes aura points. Works on a single device, no network required.

- [x] Camera capture with telemetry (IP, geolocation) — wired with react-native-vision-camera: useCameraDevice, useCameraPermission, <Camera> component, startRecording/stopRecording via ref
- [x] Local face detection (detect faces, no recognition yet)
- [x] Recording UI (start/stop, preview, retake)
- [x] Aura point attribution UI (select person, assign points, add note)
- [x] Local storage: recordings + attributions persisted on-device
- [x] Playback and review of past recordings

**Depends on:** P-2

---

### P-4: The Card — Core

**Goal:** Identity beacon and social feed. Users claim points and see their reputation.

- [x] Local identity generation (cryptographic keypair)
- [x] Basic profile (display name, avatar)
- [x] Point claim flow (receive attribution → accept/reject)
- [x] Chronological social feed of claimed points
- [x] Quick reactions on feed items
- [x] Point history and basic stats

**Depends on:** P-2 (can be built in parallel with P-3)

---

### P-5: Backend — Core

**Goal:** Server that connects Farms to Cards. Validates attributions, delivers feeds.

- [x] User registration + authentication
- [x] Event/recording storage
- [x] Point attribution API (Farm uploads, Card claims)
- [x] Basic validation (same-IP correlation, temporal proximity)
- [x] Feed aggregation and delivery
- [x] Admin dashboard (minimal)

**Depends on:** P-1, P-2

---

### P-6: End-to-End Integration

**Goal:** First complete flow: record on Farm → upload → validate → claim on Card → view in feed.

- [x] Farm → Backend upload pipeline
- [x] Backend → Card feed delivery
- [x] End-to-end test suite
- [x] Error handling: offline queue, retry, conflict resolution (retry + queue in Farm API client, retry in Card API client; conflict resolution deferred to P-8)
- [x] Performance baseline (latency, payload sizes)

**Depends on:** P-3, P-4, P-5

---

### N-1: Founding Community

**Goal:** First real users. Bootstrap the network with a trusted circle.

- [~] Invite founding members (friends, early adopters) — prep kit ready: `docs/community/founding-members.md`
- [~] First real-world event with multiple Farm instances — prep guide ready: `docs/community/first-event.md`
- [~] Gather feedback on core flow — template ready: `docs/community/feedback-template.md`
- [x] Community guidelines draft
- [x] Moderation and dispute resolution process

**Depends on:** P-6 (need working product)

---

### P-7: Multi-Device & Event Correlation

**Goal:** Multiple Farms at the same event. Cross-device telemetry correlation.

- [x] Event creation and joining (create event → others join)
- [x] Cross-device time + location correlation
- [x] Duplicate detection and merging
- [x] Bluetooth proximity for same-room detection
- [x] Audio fingerprinting for event matching

**Depends on:** P-6, N-1

---

### P-8: Community Validation

**Goal:** Points aren't just claimed — they're confirmed or challenged by others who were there.

- [x] Confirm/challenge attribution UI — Card validation module + ValidationScreen with consensus view and dispute flow
- [x] Consensus algorithm (threshold-based, configurable) — backend validations.ts + Card client
- [x] Reputation weighting for validators — backend validations.ts
- [x] Dispute resolution flow
- [x] Validation transparency (who confirmed, who challenged, why)

**Depends on:** P-7

---

### P-9: Enhanced Telemetry

**Goal:** Richer data for better attribution and validation.

- [x] Face recognition (match faces across recordings)
- [x] Activity/gesture recognition (activity detection done, gesture done)
- [x] Audio event detection (applause, laughter, etc.) — wired via expo-av metering in RecordScreen
- [x] Location precision improvements (altitude, heading, speed)
- [x] Telemetry privacy controls (user-configurable)

**Depends on:** P-7

---

### N-2: Public Beta

**Goal:** Open the doors. Real users, real events, real reputation.

- [x] Invite system (member invites member)
- [x] Onboarding flow for new users
- [x] Public community guidelines
- [x] Terms of service, privacy policy (final)
- [x] Feedback collection and iteration loop
- [x] Community moderation tools

**Depends on:** P-8, P-9, N-1

---

### C-2: Go-to-Market

**Goal:** Aura is a real company with real users and a path to sustainability.

- [~] App Store / Play Store submission — native projects created (iOS + Android), submission prep guide at `docs/product/app-store-submission.md`. Blocked on: Xcode install, Android Studio install, developer accounts, screenshots. App icon done.
- [ ] Public launch at `ifarm.club`
- [x] Marketing site and content
- [x] Social media presence — strategy doc: `docs/company/social-media-strategy.md`
- [x] Monetization strategy (if applicable) — doc: `docs/product/monetization-strategy.md`
- [x] Metrics and analytics — architecture doc: `docs/product/analytics-architecture.md`
- [x] Funding strategy (if applicable)

**Depends on:** N-2

---

### P-10: Scale & Hardening

**Goal:** Production-ready. Secure, performant, reliable.

- [x] Cryptographic identity verification (no spoofing) — Ed25519 challenge-response login + JWT session tokens + authMiddleware on all protected routes
- [x] Anti-gaming measures (prevent point farming, Sybil attacks)
- [x] Privacy controls (granular telemetry sharing)
- [x] Data retention and deletion policies
- [ ] Backend scaling (single machine → cloud)
- [ ] Media storage and CDN
- [x] Real-time feed performance
- [x] Offline support and sync resilience

**Depends on:** N-2

---

### N-3: Network Effects

**Goal:** The network grows on its own. Reputation becomes portable and valuable.

- [ ] Public profiles and shareable cards
- [ ] Cross-event reputation (points carry across events)
- [ ] Community-led events and moderation
- [ ] API for third-party integrations
- [ ] Reputation portability (export, verify externally)
- [ ] Network health metrics and transparency reports

**Depends on:** C-2, P-10

---

## Dependency Graph

```
W-1 ──→ C-1 ──→ P-1 ──→ P-2 ──→ P-3 ──┐
                         │       P-4 ──┤
                         │       P-5 ──┤
                         │             ↓
                         │          P-6 ──→ N-1 ──→ P-7 ──→ P-8 ──┐
                         │                          P-9 ────────────┤
                         │                                           ↓
                         │                                        N-2 ──→ C-2 ──→ P-10 ──→ N-3
```

---

## Key Decisions (All Resolved)

All 9 ADRs written and approved. See `docs/adr/` for full records. One pending: ADR-009 (Media Storage — Tigris).

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Privacy regulation (GDPR, biometric data) | High | On-device processing, user-controlled telemetry, legal review at C-1 |
| Gaming/manipulation of scores | High | Community consensus (P-8), anti-gaming heuristics (P-10), reputation weighting |
| Single-developer bottleneck | Medium | Agent automation, clean architecture, documentation-first |
| Cold start (no users → no validation) | Medium | Single-user mode works without network (P-3), bootstrap with trusted circle (N-1) |
| Platform risk (app store rejection) | High | PWA as fallback, clear privacy disclosures, legal prep at C-1 |
| No cloud infrastructure yet | Medium | Local-first design, defer cloud until P-5/P-10 |

---

## Operating Principles

1. **Local-first.** Everything works offline. Network is additive, not required.
2. **Privacy-by-design.** Telemetry processed on-device. Users control what's shared.
3. **Transparent scoring.** Point attribution is public and challengeable. No black boxes.
4. **Community-governed.** Validation by consensus, not central authority.
5. **Agent-built.** The autonomous agent is the primary builder. Code is committed, documented, reviewable.
6. **No deadlines.** Milestones are sequenced by dependency. We ship when the work is done.
