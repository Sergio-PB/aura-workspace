# Aura — Launch Plan

> **Status:** Draft v1
> **Author:** Aura Agent (autonomous operator)
> **Created:** 2026-08-06

## Success Criteria

Aura's public launch is successful when:

1. **Any visitor to `ifarm.club` can open The Farm in their browser**, grant camera permission, and see hand tracking + particle effects within 30 seconds — no account, no download, no friction.
2. **Two people at the same physical location can use The Farm simultaneously**, each selecting the other as target, and see points accumulate on a shared live leaderboard.
3. **Points persist across sessions.** A user who closes the browser and returns sees their accumulated aura on their Card.
4. **Zero server errors in the first 24 hours** of public traffic. The backend stays up, WebSockets stay connected, points are calculated correctly.
5. **First 10 users are not the founder or the agent.** Real people, real moves, real points.

## Rollout Strategy

### Phase 0: Soft Launch (Now → Ready)

**Who:** Founder + agent only.
**What:** Every P-15 item checked off. Backend deployed. Farm accessible at `ifarm.club`. End-to-end flow works: open browser → track hands → see particles → points appear on leaderboard → points persist on reload.
**Success gate:** Founder performs a full session end-to-end and confirms it works.

### Phase 1: Friends & Family (1-2 weeks after Phase 0)

**Who:** 5-10 trusted people (see `docs/community/founding-members.md`).
**What:** Invite-only. Each person gets a link. They try The Farm on their own device. No event needed — solo sessions count. Goal is to find bugs, UX friction, and browser compatibility issues.
**Success gate:** At least 5 people complete a session. All critical bugs filed and fixed.

### Phase 2: First Event (1-2 weeks after Phase 1)

**Who:** Same 5-10 people, same physical location.
**What:** Multi-device event. Everyone runs The Farm simultaneously. Cross-device leaderboard updates in real time. Test the "two people attributing each other" flow.
**Success gate:** Leaderboard shows points from multiple devices updating live. No WebSocket drops. No point calculation errors.

### Phase 3: Public Beta (2-4 weeks after Phase 2)

**Who:** Anyone with the link. Capped at 100 users.
**What:** `ifarm.club` goes live. No invite required, but no public announcement yet. Monitor infrastructure, abuse patterns, and user behavior.
**Success gate:** 100 users, zero server errors, zero abuse incidents requiring manual intervention.

### Phase 4: Public Launch

**Who:** Open to everyone.
**What:** Public announcement. Social media push. App Store submission (if ready). The door is open.
**Success gate:** All launch success criteria met.

## Communication Plan

| Phase | Channel | Message |
|-------|---------|---------|
| Phase 1 | Direct message (Telegram/Signal) | Personal invite: "I built something. Want to try it? It tracks your hand movements and gives you aura points. Takes 30 seconds." |
| Phase 2 | Group chat | Event coordination: "Bring your phone to [location]. We're testing the multi-device thing." |
| Phase 3 | Twitter/X, product hunt (optional) | "Aura is in beta: a social reputation network where points are earned by doing things, not posting things. ifarm.club" |
| Phase 4 | All channels | Full launch announcement with demo video, screenshots, and user testimonials from Phase 1-3. |

## Pre-Launch Checklist (P-15)

All items must be checked before Phase 1:

- [x] Abuse prevention — duplicate detection
- [x] Abuse prevention — rate limiting
- [x] Abuse prevention — device fingerprinting (browser fingerprint + anomaly detection)
- [x] Abuse prevention — minimum effort threshold
- [x] Abuse prevention — Sybil resistance
- [x] Security audit — critical + high fixed
- [~] Privacy review — telemetry opt-out UI (done), cookie consent (done). Gap: lawyer review.
- [~] Legal — DMCA/copyright policy (done). Gap: company formation.
- [~] App store readiness — native projects + icon + guide done. Blocked: Xcode, Android Studio, developer accounts.
- [~] Infrastructure — Docker + fly.toml + CI ready. Blocked: Fly.io auth + payment method.
- [x] Monitoring — production error tracking (Sentry), uptime monitoring (scripts/uptime-monitor.py), abuse alerting (webhook)
- [x] Community guidelines
- [x] Launch plan (this document)

## Go/No-Go Criteria

**Go for Phase 1 when:**
- Backend deployed and healthy
- Farm loads at `ifarm.club` in < 5 seconds
- End-to-end session works (founder-verified)
- Security audit critical + high findings resolved
- Rate limiting active

**Go for Phase 3 when:**
- Phase 1 + 2 complete with no critical regressions
- Monitoring and alerting in place
- Privacy policy and ToS published
- Abuse detection running

**No-go (any phase):**
- Any critical security vulnerability unfixed
- Backend errors > 0 in the last 24 hours
- Data loss or corruption detected
- Founder veto

## Post-Launch Metrics

Track these from day one:

| Metric | Target (Phase 3) | Target (Phase 4+) |
|--------|-------------------|---------------------|
| Daily active users | > 20 | > 100 |
| Sessions per user per week | > 2 | > 5 |
| Points attributed per session | > 50 | > 100 |
| WebSocket connection stability | > 99% | > 99.9% |
| Server error rate | 0% | < 0.1% |
| Time to first point (landing → points) | < 30s | < 15s |
| Abuse reports per 1000 sessions | < 1 | < 0.5 |

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Browser compatibility (Safari WebRTC, Firefox MediaPipe) | Medium | Test on all major browsers in Phase 1. Fallback: "Works best on Chrome" messaging. |
| WebSocket scaling under load | Low (Phase 3 cap: 100 users) | Single-server WebSocket handles 100 concurrent easily. Revisit at 1000+. |
| Abuse/gaming in public beta | Medium | Rate limiting + minimum effort threshold already in place. Monitor and tune. |
| Privacy backlash (camera access) | Medium | All processing on-device. Clear messaging: "Nothing leaves your browser until you choose." |
| App Store rejection | High | PWA works without App Store. Native apps are additive, not required. |
| Founder bandwidth | High | Agent handles operations. Founder reviews decisions, not code. |
