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

- [ ] Legal structure (LLC, incorporation, or sole proprietorship — decide)
- [ ] `ifarm.club` DNS + hosting + landing page
- [x] Brand identity (logo, colors, typography, voice)
- [ ] Company bank account + payment infrastructure
- [x] Operating rhythm: daily agent briefings, weekly founder review
- [x] Compliance baseline: privacy policy, terms of service drafts
- [ ] Public presence: GitHub org (or keep private), social accounts, domain email

**Depends on:** Nothing. This is the starting line.

---

### P-1: Architecture & Tech Stack

**Goal:** Every technical decision is made, documented, and justified before code is written.

- [x] **ADR: Farm platform** — native (Swift/Kotlin) vs React Native vs Flutter vs PWA
- [x] **ADR: Backend stack** — language, framework, runtime
- [x] **ADR: Database & sync** — PostgreSQL vs SQLite vs hybrid local-first
- [x] **ADR: Identity model** — self-sovereign keypairs vs email/phone vs OAuth
- [x] **ADR: API protocol** — REST vs GraphQL vs gRPC vs WebSocket
- [ ] **ADR: Cloud provider** — defer or choose now
- [ ] System architecture diagram (Farm → Backend → Card)
- [ ] Data flow: telemetry capture → upload → validation → attribution → feed
- [ ] Database schema (users, events, points, validations)
- [ ] Security & privacy architecture

**Depends on:** C-1 (need brand context for tech choices)

---

### P-2: Development Infrastructure

**Goal:** CI/CD, tooling, and dev environment — so every subsequent P-initiative has a clean pipeline.

- [ ] Monorepo tooling (Turborepo, Nx, or manual workspaces)
- [ ] CI/CD pipelines (GitHub Actions): lint, test, build
- [ ] Local dev environment (one-command setup)
- [ ] Testing framework + strategy (unit, integration, e2e)
- [ ] Code quality: linting, formatting, type checking, pre-commit hooks
- [ ] Shared packages: types, API contracts, auth client, telemetry models

**Depends on:** P-1 (need stack decisions)

---

### P-3: The Farm — Core

**Goal:** Local media studio that captures telemetry and attributes aura points. Works on a single device, no network required.

- [ ] Camera capture with telemetry (IP, geolocation)
- [ ] Local face detection (detect faces, no recognition yet)
- [ ] Recording UI (start/stop, preview, retake)
- [ ] Aura point attribution UI (select person, assign points, add note)
- [ ] Local storage: recordings + attributions persisted on-device
- [ ] Playback and review of past recordings

**Depends on:** P-2

---

### P-4: The Card — Core

**Goal:** Identity beacon and social feed. Users claim points and see their reputation.

- [ ] Local identity generation (cryptographic keypair)
- [ ] Basic profile (display name, avatar)
- [ ] Point claim flow (receive attribution → accept/reject)
- [ ] Chronological social feed of claimed points
- [ ] Quick reactions on feed items
- [ ] Point history and basic stats

**Depends on:** P-2 (can be built in parallel with P-3)

---

### P-5: Backend — Core

**Goal:** Server that connects Farms to Cards. Validates attributions, delivers feeds.

- [ ] User registration + authentication
- [ ] Event/recording storage
- [ ] Point attribution API (Farm uploads, Card claims)
- [ ] Basic validation (same-IP correlation, temporal proximity)
- [ ] Feed aggregation and delivery
- [ ] Admin dashboard (minimal)

**Depends on:** P-1, P-2

---

### P-6: End-to-End Integration

**Goal:** First complete flow: record on Farm → upload → validate → claim on Card → view in feed.

- [ ] Farm → Backend upload pipeline
- [ ] Backend → Card feed delivery
- [ ] End-to-end test suite
- [ ] Error handling: offline queue, retry, conflict resolution
- [ ] Performance baseline (latency, payload sizes)

**Depends on:** P-3, P-4, P-5

---

### N-1: Founding Community

**Goal:** First real users. Bootstrap the network with a trusted circle.

- [ ] Invite founding members (friends, early adopters)
- [ ] First real-world event with multiple Farm instances
- [ ] Gather feedback on core flow
- [ ] Community guidelines draft
- [ ] Moderation and dispute resolution process

**Depends on:** P-6 (need working product)

---

### P-7: Multi-Device & Event Correlation

**Goal:** Multiple Farms at the same event. Cross-device telemetry correlation.

- [ ] Event creation and joining (create event → others join)
- [ ] Cross-device time + location correlation
- [ ] Duplicate detection and merging
- [ ] Bluetooth proximity for same-room detection
- [ ] Audio fingerprinting for event matching

**Depends on:** P-6, N-1

---

### P-8: Community Validation

**Goal:** Points aren't just claimed — they're confirmed or challenged by others who were there.

- [ ] Confirm/challenge attribution UI
- [ ] Consensus algorithm (threshold-based, configurable)
- [ ] Reputation weighting for validators
- [ ] Dispute resolution flow
- [ ] Validation transparency (who confirmed, who challenged, why)

**Depends on:** P-7

---

### P-9: Enhanced Telemetry

**Goal:** Richer data for better attribution and validation.

- [ ] Face recognition (match faces across recordings)
- [ ] Activity/gesture recognition
- [ ] Audio event detection (applause, laughter, etc.)
- [ ] Location precision improvements
- [ ] Telemetry privacy controls (user-configurable)

**Depends on:** P-7

---

### N-2: Public Beta

**Goal:** Open the doors. Real users, real events, real reputation.

- [ ] Invite system (member invites member)
- [ ] Onboarding flow for new users
- [ ] Public community guidelines
- [ ] Terms of service, privacy policy (final)
- [ ] Feedback collection and iteration loop
- [ ] Community moderation tools

**Depends on:** P-8, P-9, N-1

---

### C-2: Go-to-Market

**Goal:** Aura is a real company with real users and a path to sustainability.

- [ ] App Store / Play Store submission
- [ ] Public launch at `ifarm.club`
- [ ] Marketing site and content
- [ ] Social media presence
- [ ] Monetization strategy (if applicable)
- [ ] Metrics and analytics
- [ ] Funding strategy (if applicable)

**Depends on:** N-2

---

### P-10: Scale & Hardening

**Goal:** Production-ready. Secure, performant, reliable.

- [ ] Cryptographic identity verification (no spoofing)
- [ ] Anti-gaming measures (prevent point farming, Sybil attacks)
- [ ] Privacy controls (granular telemetry sharing)
- [ ] Data retention and deletion policies
- [ ] Backend scaling (single machine → cloud)
- [ ] Media storage and CDN
- [ ] Real-time feed performance
- [ ] Offline support and sync resilience

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

## Key Decisions (ADRs Needed)

| # | Decision | Track | Options |
|---|----------|-------|---------|
| 1 | Farm platform | P-1 | Native (Swift/Kotlin) vs React Native vs Flutter vs PWA |
| 2 | Backend stack | P-1 | Node/TypeScript vs Python vs Go vs Rust |
| 3 | Database & sync | P-1 | PostgreSQL vs SQLite (local-first) vs hybrid |
| 4 | Identity model | P-1 | Self-sovereign keypairs vs email/phone vs OAuth |
| 5 | API protocol | P-1 | REST vs GraphQL vs gRPC |
| 6 | Cloud provider | P-1 | AWS vs Fly.io vs Vercel vs defer |
| 7 | Legal structure | C-1 | LLC vs C-Corp vs sole proprietorship |
| 8 | Monorepo tooling | P-2 | Turborepo vs Nx vs pnpm workspaces |

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
