# Aura — Company Plan & Roadmap

> **Date:** 2026-07-24
> **Status:** Draft v1
> **Author:** Aura Agent (autonomous operator)

---

## Vision

Aura builds a fair community where social reputation is earned through real-world actions, not manufactured online personas. Points are attributed by people who were actually there — recorded, verified, and validated by community consensus. No algorithms optimizing for engagement. No bots. Just people recognizing people.

## Mission

Launch two products at `ifarm.club` that make social scoring transparent, local, and community-governed:

1. **The Farm** — capture the moment (local media studio with telemetry)
2. **The Card** — carry your reputation (identity beacon + social feed)

---

## Current State

| Area | Status |
|------|--------|
| Company formation | Bootstrapped (2026-07-24) |
| Product code | None — design phase |
| Infrastructure | None — local dev only |
| Team | Founder (Sergio) + Aura Agent (autonomous operator) |
| Domain | `ifarm.club` — registered, no DNS configured |
| Repos | `aura-workspace` (company brain), `aura-apps` (monorepo) |
| Funding | Bootstrapped |

---

## Roadmap

### Phase 0: Foundation (Q3 2026 — Now)

**Goal:** Make all architectural and technical decisions. Set up development infrastructure. Nothing is built yet — this phase is about choosing right.

#### 0.1 Tech Stack Decision
- **Farm:** Native mobile (Swift/Kotlin) vs cross-platform (React Native/Flutter) vs PWA
- **Card:** Mobile app + web companion
- **Backend:** Language, framework, database
- **Shared:** Types, API contracts, auth model
- **Decision criteria:** Time-to-MVP, local processing capability, camera/ML access, single-developer maintainability

#### 0.2 Architecture Design
- System architecture diagram (Farm → Backend → Card)
- Data flow: telemetry capture → upload → validation → attribution → feed
- API design: REST vs GraphQL vs WebSocket
- Database schema: users, events, points, validations
- Security model: identity, authentication, privacy

#### 0.3 Development Infrastructure
- CI/CD pipelines (GitHub Actions)
- Local dev environment setup scripts
- Testing framework and strategy
- Code quality tooling (linting, formatting, type checking)

#### 0.4 ifarm.club Landing Page
- Static landing page at `ifarm.club`
- Product descriptions, waitlist signup
- DNS + hosting setup

**Deliverables:** ADRs for tech stack and architecture, CI/CD running, landing page live.

---

### Phase 1: Core Prototype (Q3–Q4 2026)

**Goal:** Build the minimum end-to-end flow: record → attribute → claim → validate. Working on a single device, no network yet.

#### 1.1 The Farm — MVP
- Camera capture with basic telemetry (IP, geolocation)
- Local face detection (no recognition yet — just detect faces)
- Simple recording UI (start/stop, preview)
- Aura point attribution UI (select person, assign points)
- Local storage of recordings + attributions

#### 1.2 The Card — MVP
- Local identity generation (keypair)
- Basic profile (display name, avatar)
- Point claim flow (receive attribution → accept/reject)
- Minimal social feed (chronological list of claimed points)

#### 1.3 Backend — MVP
- User registration + authentication
- Event/recording storage
- Point attribution API
- Basic validation (same-IP correlation)
- Feed aggregation

#### 1.4 Integration
- Farm → Backend upload flow
- Backend → Card feed delivery
- End-to-end test: record, upload, claim, view in feed

**Deliverables:** Working prototype on a single device, all three components talking to each other.

---

### Phase 2: Network & Validation (Q4 2026 – Q1 2027)

**Goal:** Multi-user, multi-device. Community validation mechanics. Real telemetry correlation.

#### 2.1 Multi-Device Farm
- Multiple Farm instances at same event
- Cross-device event correlation (time + location)
- Duplicate detection and merging

#### 2.2 Community Validation
- Confirm/challenge attribution UI
- Consensus algorithm (threshold-based)
- Reputation weighting for validators
- Dispute resolution flow

#### 2.3 Enhanced Telemetry
- Face recognition (match faces across recordings)
- Audio fingerprinting for event matching
- Bluetooth proximity for same-room detection

#### 2.4 The Card — Social Features
- Quick reactions (emoji, short responses)
- Activity feed with filters
- Point history and analytics
- Share card/profile externally

**Deliverables:** Multi-user alpha, community validation working, enhanced telemetry.

---

### Phase 3: Beta & Launch (Q2 2027)

**Goal:** Public beta. Polish, security, scale. Go to market.

#### 3.1 Security Hardening
- Cryptographic identity verification
- Anti-gaming measures (prevent point farming)
- Privacy controls (what telemetry is shared)
- Data retention policies

#### 3.2 Scale & Performance
- Backend scaling (from single dev machine to cloud)
- Media storage and delivery (CDN)
- Real-time feed performance
- Offline support for Farm

#### 3.3 Public Beta
- Invite-only beta program
- Feedback collection and iteration
- Community guidelines and moderation
- Terms of service, privacy policy

#### 3.4 Launch
- App Store / Play Store submission
- Public launch at `ifarm.club`
- Marketing and community building
- Monetization strategy (if applicable)

**Deliverables:** Live products, real users, community growing.

---

## Key Decisions Pending

These need ADRs before Phase 1 begins:

| # | Decision | Options | Impact |
|---|----------|---------|--------|
| 1 | Farm platform | Native (Swift/Kotlin) vs React Native vs Flutter vs PWA | Camera access, ML perf, dev speed |
| 2 | Backend stack | Node/TypeScript vs Python vs Go vs Rust | Dev speed, ecosystem, hiring |
| 3 | Database | PostgreSQL vs SQLite (local-first) vs hybrid | Offline support, sync complexity |
| 4 | Identity model | Self-sovereign (keypairs) vs email/phone vs OAuth | Privacy, UX, security |
| 5 | API protocol | REST vs GraphQL vs gRPC | Real-time needs, client complexity |
| 6 | Cloud provider | None yet — decide before Phase 2 | Cost, scale, region |

---

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Privacy/regulatory (GDPR, face data) | High | Privacy-by-design, on-device processing, legal review in Phase 0 |
| Gaming/manipulation of scores | High | Community consensus, anti-gaming heuristics, reputation weighting |
| Single-developer bottleneck | Medium | Agent automation, clean architecture, documentation-first |
| No cloud infrastructure yet | Medium | Local-first design, defer cloud decisions until needed |
| Cold start (no users → no validation) | Medium | Single-user mode works without network, bootstrap with trusted circle |
| Platform risk (app store rejection) | High | PWA as fallback, clear privacy disclosures |

---

## Success Metrics

- **Phase 1:** One end-to-end flow working (record → claim → view)
- **Phase 2:** 10+ users at a single event, community validation functioning
- **Phase 3:** 100+ active users, < 24h point dispute resolution

---

## Operating Principles (How We Build)

1. **Local-first.** Everything works offline. Network is additive, not required.
2. **Privacy-by-design.** Telemetry is processed on-device. Users control what's shared.
3. **Transparent scoring.** Point attribution is public and challengeable. No black-box algorithms.
4. **Community-governed.** Validation is by consensus, not by central authority.
5. **Agent-built.** The autonomous agent is the primary builder. Code is committed, documented, and reviewable.
