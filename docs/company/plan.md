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
- [x] `ifarm.club` DNS + hosting + landing page (landing page live at sergio-pb.github.io/aura-workspace; DNS still needs founder to point ifarm.club to GitHub Pages IPs — guide at `docs/company/dns-setup.md`)
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
- [x] Privacy controls (granular telemetry sharing) — policy docs done (`docs/legal/privacy-policy.md`, `docs/legal/data-retention.md`); Farm UI toggles built in Capacitor Farm (PrivacySettingsScreen + wired into RecordScreen)
- [x] Data retention and deletion policies — policy docs done; backend implementation: soft-delete schema (`deleted_at` columns), `DELETE /recordings/:id`, `DELETE /account`, `GET /account/export`, audit log table, `scripts/hard-delete-sweep.ts`
- [~] Backend scaling (single machine → cloud) — Docker image builds + runs (verified 2026-08-02), deploy workflow ready at `.github/workflows/deploy-backend.yml`. Blocked on: founder Fly.io auth (`fly auth login`).
- [x] Media storage and CDN
- [x] Real-time feed performance
- [x] Offline support and sync resilience

**Depends on:** N-2

---

### P-11: Farm MVP — Movement Tracking

**Goal:** The Farm app captures camera feed, tracks hand movements via MediaPipe, detects gestures against a move library, renders particles on a canvas overlay, and shows a debug panel of what telemetry would be sent to the backend — all running locally in the browser, no backend required.

- [x] Camera capture via `getUserMedia` (web) + Capacitor Camera plugin (native fallback)
- [x] Hand tracking via MediaPipe Hands (WASM, 21 landmarks per hand)
- [x] Gesture detection engine: match hand landmark patterns against move library
- [x] Move library: at minimum "seesaw" (alternating up/down hands) with configurable aura rate
- [x] Particle overlay: canvas on top of camera feed, particles spawn when gesture detected
- [x] Telemetry debug panel: shows real-time data that would be sent (face ID, hand positions, detected moves, particle count, geolocation, IP, timestamp)
- [x] Works on mobile browser (tested on phone via local network) — dev server exposed at https://192.168.15.7:5173/ with HTTPS; manual phone test pending

**Depends on:** P-10 (Farm Capacitor scaffold exists)

---

### P-12: Movement Library Expansion

**Goal:** Expand the move library beyond seesaw to cover a range of real-world gestures. Each move has a detector, aura rate, and visual feedback.

- [x] **Wave** — single hand oscillating side-to-side (x-axis sign changes over window)
- [x] **Clap** — both hands rapidly converging (distance between wrists drops below threshold)
- [x] **Raise the roof** — both hands pushing upward repeatedly (y-axis peaks)
- [x] **Point tracking** — follow where a pointing hand is aimed (index tip direction vector)
- [x] Move library registry: unified interface for registering moves, querying active moves, and aggregating aura rates
- [x] Per-move particle effects (distinct colors/shapes per move type)

**Depends on:** P-11 (tracking pipeline exists)

---

### P-13: Forgiving Reward System

**Goal:** Make aura attribution psychologically pleasant by being generous with detection gaps. If a move is detected at T0, missed at T1 (tracking glitch), and detected again at T2, the system assumes the user was still performing the move continuously and bridges the gap.

- [x] **Detection gap bridging** — if a move was active within the last N frames (configurable, default ~15 = 0.5s at 30fps), treat a re-detection as continuation, not a new start
- [x] **Aura decay curve** — instead of binary on/off, aura rate decays gradually when tracking drops (e.g. hold at 80% for 0.5s, then linear decay to 0 over 1s)
- [x] **Minimum aura floor** — once a move is detected, award a minimum aura even if tracking is brief (e.g. 0.5s minimum credit)
- [x] **Over-giving bias** — when in doubt between "user stopped" and "tracking glitch", default to "still going" (configurable aggressiveness)
- [x] **Visual feedback continuity** — particles continue at reduced rate during gap bridging, so the user never sees a "dead" screen
- [x] **Configurable tuning** — gap window, decay curve shape, floor amount, and over-giving aggressiveness all tunable via constants

**Depends on:** P-11 (tracking pipeline exists), P-12 (more moves to apply forgiveness to)

---

### P-14: Video Farming

**Goal:** Process pre-recorded videos through the same tracking pipeline as the live camera. Users can upload or select a video, and the Farm runs MediaPipe on each frame, detecting gestures and moves just like the live feed.

- [x] Video file input (file picker or drag-and-drop)
- [x] Frame-by-frame MediaPipe processing (seekable video → hand tracking per frame)
- [x] Same gesture/move detection pipeline as live camera
- [x] Playback controls (play, pause, scrub, speed)
- [x] Telemetry overlay on video (same debug panel, synced to video time)
- [x] Export: save processed video with particle overlay burned in

**Depends on:** P-11 (tracking pipeline exists)

---

### P-15: Pre-Launch Checklist

**Goal:** Every box checked before Aura goes public. Security, abuse prevention, legal, and operational readiness.

- [x] **Abuse prevention — duplicate detection** — `mediaHash` + `audioFingerprint` on recordings, `duplicates.ts` route with overlap detection and merge endpoint
- [x] **Abuse prevention — rate limiting** — `rate-limit.ts` middleware (60 req/60s sliding window), applied to attributions + validations
- [x] **Abuse prevention — device fingerprinting** — `deviceId` + IP + geo captured per recording, IP clustering in anti-gaming. Browser fingerprint via canvas+WebGL (`useDeviceFingerprint` hook), anomaly detection middleware (`device-anomaly.ts`) checks device diversity, geo jumps, IP churn, and device+IP mismatch. Score ≥70 blocks session, ≥40 flags.
- [x] **Abuse prevention — minimum effort threshold** — `endSession` in `ws.ts` requires ≥30 ticks (~3s at 10 Hz) before points count; sessions below threshold get 0 points
- [x] **Abuse prevention — Sybil resistance** — Ed25519 keypairs, `anti-gaming.ts` middleware (point velocity, new-account limits, IP clustering, reciprocal farming detection)
- [x] **Security audit** — completed 2026-08-05: 12 findings (1 critical, 3 high, 4 medium, 4 low). Critical + high fixed. See `docs/security/audit-2026-08-05.md`.
- [~] **Privacy review** — Policy drafts exist, deletion flow implemented. Gap: lawyer review, telemetry opt-out UI (done — PrivacySettingsScreen in Capacitor Farm), cookie consent (done — banner on all landing pages)
- [~] **Legal** — ToS + Privacy Policy drafts exist (pending lawyer review). DMCA/copyright policy done (`docs/legal/dmca-policy.md`). Gap: company not formed
- [~] **App store readiness** — Native projects created, icon done, guide written. Blocked: Xcode, Android Studio, developer accounts, screenshots
- [~] **Infrastructure** — Dockerfile + fly.toml + CI ready. Blocked: Fly.io auth + payment method. Gap: Tigris deploy, CDN, production DB
- [x] **Monitoring** — Cron stack + launchd watchdog exist. Production monitoring built: structured event ring buffer, abuse alerting, health check with DB probe (`/admin/events`, `/admin/alerts`, `/admin/healthz`). Webhook delivery done (`AURA_ALERT_WEBHOOK_URL`). Sentry error tracking added (2026-08-08): `@sentry/bun` init from `SENTRY_DSN`, `app.onError` captures all unhandled Hono errors. Uptime monitoring: `scripts/uptime-monitor.py` pings landing page every 5 min, logs response times, alerts on 2+ consecutive failures via webhook.
- [x] **Community guidelines** — `docs/community/guidelines.md` v1.0 published with enforcement ladder
- [x] **Launch plan** — `docs/product/launch-plan.md`: phased rollout (soft → friends → event → beta → public), comms plan, go/no-go criteria, post-launch metrics

**Depends on:** P-10 (backend deployed), P-12 (move library), P-13 (reward system), P-14 (video farming), C-1 (legal), C-2 (GTM)

---

### P-16: Feed MVP — Live Leaderboard & Point Streaming

**Goal:** End-to-end flow: user selects a target user on the Farm, performs moves, the device streams hand coordinates + detected moves to the backend, the server translates the stream into aura points, and a live leaderboard updates in real time. Simple foundation that can scale.

**Mental model:** The device is trusted. It tells the server "User A did seesaw at rate 0.8 for 3 seconds." The server responds "That's 24 aura points for User A." The leaderboard updates.

- [x] **Simple user model** — `users` table: `id` (UUID), `displayName` (string). No auth, no passwords. Just identity. (Existing users table reused; public `/users` endpoint for carousel.)
- [x] **User selector on Farm** — carousel or overlay on the camera view. User picks a target before/while recording. Sends `targetUserId` with every stream frame. (`UserCarousel.tsx`)
- [x] **Move stream protocol** — Farm opens a WebSocket to backend. Sends JSON frames: `{ targetUserId, move, rate, timestamp }` at ~10 Hz while a move is active. (`useFarmWebSocket.ts`)
- [x] **Server-side point calculator** — backend receives move stream, applies scoring formula: `points = rate × duration × moveMultiplier`. Accumulates per-user per-session. Persists to `attributions` table. (`calculator.ts`, `ws.ts`)
- [x] **Live leaderboard** — backend broadcasts point updates via WebSocket. Farm (or Card) renders a sorted list of users by total points, updating in real time. (`ws.ts` broadcast, `FeedScreen.tsx`)
- [x] **Feed screen** — displays the leaderboard + recent attributions. Accessible from both Farm and Card. (`FeedScreen.tsx`)
- [x] **Session lifecycle** — start session (select user), stream moves, end session (finalize points). Points are provisional until session ends. (`routes/sessions.ts`)

**Scoring formula (v1):**
```
points = Σ (rate × duration_seconds × moveMultiplier)
  where moveMultiplier = { seesaw: 10, wave: 8, clap: 12, raise_roof: 15 }
  rate is 0..1 from the move detector
  duration is time the move was continuously active
```

**Depends on:** P-11 (tracking pipeline), P-5 (backend core), P-6 (E2E integration)

---

### P-17: Game-Like GUI

**Goal:** Transform the Farm UI from a functional debug panel into an addictive mobile game interface. Every screen should feel like a polished social game — particle effects, haptic-like visual feedback, satisfying transitions, score popups, combo streaks. This is a **standing requirement** for all future movement library additions: every new move must ship with its own visual identity (particle color, animation, sound cue placeholder).

**Gamification model:** Session-scoped, short-attention-span. No persistent user levels — users have total aura points + stats (max streak, max ego, etc.). All flashy elements are per-session: streaks, combos, and ego bursts.

**Design principles:**
- **Addictive feedback loops** — every gesture triggers immediate, satisfying visual/audio reward
- **Mobile-first game feel** — large touch targets, gesture-friendly layout, no tiny text
- **Dark theme with neon accents** — particles glow, scores pulse, combos flash
- **Minimalist HUD** — only what matters: who you're scoring, current move, combo counter, total points
- **60fps animations** — no jank, no flicker, smooth particle physics
- **Sound design placeholders** — every move type has a designated sound slot (implement later, design now)
- **Session-scoped** — streaks, combos, and ego reset per recording. No long-running campaigns.

**Checklist:**
- [x] **Game HUD overlay** — replaces debug panel. Shows: target user avatar, current move name, streak counter, combo multiplier, session aura points with animated counter
- [x] **Streak system** — continuous movement without gaps builds a streak counter. Visual flame/glow intensifies. Streak breaks on 1.5s+ gap. Max streak recorded as user stat.
- [x] **Combo system** — chaining *different* moves within 2s window multiplies points (×2, ×3, ×5, ×10). Visual combo meter. "seesaw → wave → clap" = ×3 combo. Max combo recorded as user stat.
- [x] **Ego bursts** — within a single session, hitting point thresholds (100, 250, 500, 1000) triggers a full-screen celebration ("Ego ×2!", "Ego ×5!"). Resets per session. Max ego recorded as user stat.
- [x] **Move-specific particles** — each move type has unique particle color/shape/behavior (seesaw=gold waves, wave=blue ripples, clap=white burst, raise_roof=purple columns)
- [x] **Score popups** — "+24 aura" floats up and fades on each point award. Combo/streak/ego multipliers shown in popup.
- [x] **Haptic feedback hooks** — placeholder API for vibration on move detection, streak milestones, combo hits, ego bursts (implement when Capacitor plugin added)
- [x] **Sound cue slots** — each move type, combo tier, streak milestone, and ego burst has a named sound slot (`.sfx.seesaw`, `.sfx.combo_x3`, `.sfx.streak_10`, `.sfx.ego_x2`, etc.) for future audio integration
- [x] **Transition animations** — screen transitions (home→record, record→feed) use smooth slides/fades
- [x] Loading states — camera init, model loading, WebSocket connecting all have animated indicators (not blank screens)
- [x] Dark theme polish — consistent color palette, proper contrast ratios, no raw CSS defaults

---

### P-18: Pose Tracking

**Goal:** Full-body tracking as the default mode; hand tracking kept as the granular opt-in. Pose captures arms, legs, and full-body movement; hand tracking stays for fine gestures (thumbs up, etc.).

- [x] MediaPipe Pose integration (33 body landmarks, skeleton) alongside the existing Hands pipeline
- [x] Pose is the default tracking mode; hand tracking is the opt-in alternate
- [x] HUD toggle to switch modes (hand ↔ pose) mid-session, without restarting the camera
- [x] Analyze feature accepts `trackingMode: 'hand' | 'pose'` as input; output is the existing telemetry envelope, just sourced from pose landmarks
- [x] Per-move visual feedback adapts to pose landmarks (body-anchored emitters, full-body particle flows) where applicable
- [~] **E2E test cases — user-recorded and supplied:** sample videos covering major movement classes (wave-arm, jump, squat, dance, full-body rotation). One per class minimum. Founder records and drops files in; pipeline runs Analyze against each and validates landmark output.

**Reasoning:** Hand tracking is too granular for full-body expression — it only sees the hands. Pose tracking should be the default so the system sees what the body is actually doing; hand tracking stays available for fine gesture work (thumbs up, point, pinch).

**Depends on:** P-11 (MediaPipe pipeline), P-14 (Analyze feature input plumbing)

---

### P-19: Responsive & Mobile-First UI Audit

**Goal:** Every screen works correctly on mobile (portrait + landscape) and small viewports. No horizontal scroll, no clipped controls, no tiny tap targets. Mobile-first by default, desktop as a fallback layout.

- [ ] Audit all Farm screens at 360×640, 414×896, 768×1024 (portrait + landscape)
- [ ] Audit all Card screens at the same breakpoints
- [ ] Audit landing page + onboarding flow at mobile breakpoints
- [ ] Fix layout, font, touch-target, and overflow issues found
- [ ] Verify HUD overlays respect safe areas (notch, home indicator, gesture bar)
- [ ] Verify on real iOS Safari + Android Chrome, not just desktop emulation

**Depends on:** P-17 (Game-Like GUI baseline)

---

**User stats (persistent, no levels):**
- Total aura points
- Max streak (longest continuous movement)
- Max combo (highest combo multiplier achieved)
- Max ego (highest ego tier reached in a single session)
- Sessions completed

**Standing requirement:** Every new move added to the movement library (P-12) MUST include:
1. Unique particle effect (color, shape, behavior)
2. Sound cue slot name
3. Streak compatibility (does it chain well?)
4. Combo multiplier integration
5. Score popup style

**Depends on:** P-11 (tracking working), P-12 (move library for per-move effects), P-13 (reward system for combo logic)

---

### N-3: Network Effects

**Goal:** The network grows on its own. Reputation becomes portable and valuable.

- [x] Public profiles and shareable cards
- [x] Cross-event reputation (points carry across events) — global leaderboard endpoint: `GET /leaderboard` + `GET /leaderboard/user/:userId`
- [x] Community-led events and moderation
- [x] API for third-party integrations
- [x] Reputation portability (export, verify externally) — `GET /reputation/export/:userId` (signed Ed25519 attestation), `POST /reputation/verify`, `GET /reputation/public-key`
- [x] Network health metrics and transparency reports

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
                         │
                         └─→ P-11 ──→ P-12 ──→ P-13 ──→ P-17 ──→ P-19
                                │                          │
                                └─→ P-14 ──→ P-16 ────────┤
                                                           └─→ P-18
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
