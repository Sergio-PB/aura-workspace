# Pre-Launch Checklist — ifarm.club

> **Status:** Audit complete — 2026-08-05
> **Author:** Aura Agent (autonomous operator)
>
> Every box checked before Aura goes public. Security, abuse prevention, legal, and operational readiness.

---

## 1. Abuse Prevention

### 1.1 Duplicate Detection — DONE

- [x] `mediaHash` on every recording (schema: `recordings.mediaHash`)
- [x] `audioFingerprint` field + `PATCH /recordings/:id/fingerprint` endpoint
- [x] `duplicates.ts` route: detects overlapping recordings by time, persists pairs, merge endpoint
- [x] Duplicate tests: `test/duplicates.test.ts`

### 1.2 Rate Limiting — DONE

- [x] `rate-limit.ts` middleware: sliding window, 60 req/60s, in-memory Map
- [x] Applied to `/attributions/*` and `/validations/*`
- [x] Periodic cleanup of stale entries (5 min interval)
- [x] Test helper: `resetRateLimitStore()` for test isolation

### 1.3 Device Fingerprinting — PARTIAL

- [x] `deviceId` captured on every recording (schema: `recordings.deviceId`)
- [x] IP + geolocation captured per recording
- [x] IP clustering in anti-gaming middleware (Sybil detection)
- [ ] **Gap:** No browser/device fingerprint (canvas hash, WebGL, font enumeration). Current `deviceId` is client-generated — a determined attacker can rotate it.
- [ ] **Gap:** No anomaly detection on device+IP+geo tuples (e.g., same deviceId from different continents within minutes)

### 1.4 Minimum Effort Threshold — GAP

- [ ] **Not implemented.** No minimum tracking duration or move variety check before awarding points.
- [ ] **Needed:** Backend validation that a recording has at least N seconds of tracking data or M distinct moves before attributions from it are accepted.
- [ ] **Needed:** Farm-side enforcement — don't allow upload if tracking duration < threshold.

### 1.5 Sybil Resistance — DONE

- [x] Ed25519 keypair per device (cryptographic identity)
- [x] `anti-gaming.ts` middleware: point velocity caps, new-account restrictions, IP clustering
- [x] Self-attribution blocked (`SELF_ATTRIBUTION` error)
- [x] Reciprocal farming detection (A↔B within 24h)
- [x] User status enforcement (suspended/banned users blocked)
- [x] Anti-gaming tests: `test/anti-gaming.test.ts`

---

## 2. Security Audit — GAP

- [ ] **No formal security audit exists.** Auth flow, data at rest, data in transit, API surface have not been systematically reviewed.
- [ ] **Needed:** Auth flow review (challenge-response, JWT, key storage)
- [ ] **Needed:** API surface review (all endpoints, auth requirements, input validation)
- [ ] **Needed:** Data at rest review (SQLite encryption, key management)
- [ ] **Needed:** Dependency audit (`npm audit`, supply chain)
- [ ] **Needed:** Rate limit bypass testing
- [ ] **Needed:** WebSocket security (no auth on WS upgrade — `ponytail:` comment in index.ts)

**What exists:**
- Ed25519 challenge-response auth (`auth.ts`, `routes/auth.ts`)
- JWT session tokens with `authMiddleware`
- Input validation via Zod on all POST/PATCH endpoints
- CORS enabled
- Rate limiting on write endpoints

---

## 3. Privacy Review — PARTIAL

- [x] Privacy Policy draft: `docs/legal/privacy-policy.md` v1.0
- [x] Data retention policy: `docs/legal/data-retention.md`
- [x] Soft-delete flow: `deleted_at` columns, `DELETE /recordings/:id`, `DELETE /account`
- [x] Account export: `GET /account/export`
- [x] Audit log table
- [x] Biometric data notice (Appendix A in privacy policy)
- [ ] **Gap:** No GDPR/CCPA compliance review by a lawyer
- [ ] **Gap:** No data deletion verification flow (user can request deletion — can we prove it happened?)
- [x] **Gap:** No telemetry opt-out UI in Farm — DONE (PrivacySettingsScreen in Capacitor Farm, wired into RecordScreen)
- [x] **Gap:** No cookie consent / tracking disclosure on landing page — DONE (banner on all 8 pages)

---

## 4. Legal — PARTIAL

- [x] Terms of Service draft: `docs/legal/terms-of-service.md` v1.0
- [x] Privacy Policy draft: `docs/legal/privacy-policy.md` v1.0
- [x] Community Guidelines: `docs/community/guidelines.md` v1.0
- [x] Legal structure recommendation: `docs/company/legal-structure-recommendation.md`
- [x] **Gap:** No DMCA / copyright policy — DONE (`docs/legal/dmca-policy.md`)
- [ ] **Gap:** No lawyer review on any legal document (all marked "pending legal review")
- [ ] **Gap:** Company not yet formed (blocked on legal structure decision)
- [ ] **Gap:** No DPO or EU Representative appointed (required for GDPR)

---

## 5. App Store Readiness — PARTIAL

- [x] Native projects created: `ios/` and `android/` in farm-capacitor
- [x] App icon generated and placed in native projects
- [x] Submission prep guide: `docs/product/app-store-submission.md`
- [x] Privacy disclosures documented (camera, location, mic, face data)
- [ ] **Blocked:** Xcode not installed (iOS build impossible)
- [ ] **Blocked:** Android Studio not installed
- [ ] **Blocked:** No Apple Developer account ($99/year)
- [ ] **Blocked:** No Google Play Developer account ($25 one-time)
- [ ] **Gap:** No screenshots (need app running on device)
- [ ] **Gap:** App Store metadata not prepared (description, keywords, age rating)

---

## 6. Infrastructure — PARTIAL

- [x] Backend Dockerfile: `apps/backend/Dockerfile` (Bun Alpine, single-stage)
- [x] fly.toml: `apps/backend/fly.toml` (iad region, auto-stop, health checks)
- [x] CI/CD: `.github/workflows/deploy-backend.yml`
- [x] Deploy guide: `docs/product/backend-deploy.md`
- [x] 103 backend tests passing
- [ ] **Blocked:** Fly.io auth — founder must run `fly auth login`
- [ ] **Blocked:** Fly.io payment method — card needed even for free tier
- [ ] **Gap:** Tigris media storage not deployed (ADR-009 approved, not implemented)
- [ ] **Gap:** No CDN configured
- [ ] **Gap:** No production database (currently libSQL file-based; needs Fly Postgres or Turso for prod)

---

## 7. Monitoring — PARTIAL

- [x] Cron monitoring stack (pulse, heartbeat, watchdog, daily, review-summary, weekly)
- [x] External launchd watchdog (`ai.aura.watchdog`, 5 min)
- [x] Error logging to `logs/errors.md`
- [x] Pre-computed health state (`pulse-health.py`)
- [x] Kanban board for roadmap visibility
- [ ] **Gap:** No production error tracking (Sentry, etc.)
- [ ] **Gap:** No uptime monitoring (health check pings from external service)
- [ ] **Gap:** No abuse alerting (real-time notification when anti-gaming triggers)
- [ ] **Gap:** No dashboard for operational metrics

---

## 8. Community Guidelines — DONE

- [x] Published: `docs/community/guidelines.md` v1.0
- [x] Core principles defined
- [x] Enforcement ladder (warning → restriction → reversal → suspension → ban)
- [x] Moderation process: `docs/community/moderation.md`
- [x] Feedback loop: `docs/community/feedback-loop.md`

---

## 9. Launch Plan — GAP

- [ ] **No rollout strategy exists.**
- [ ] **Needed:** Rollout phases (invite-only → waitlist → public)
- [ ] **Needed:** Comms plan (blog post, social media, founding members announcement)
- [ ] **Needed:** Success criteria (what does "launched" mean?)
- [ ] **Needed:** Rollback plan (what if something breaks?)
- [ ] **Needed:** Support plan (how do users get help?)

---

## 10. Landing Page — DONE

- [x] All assets present (homepage, about, FAQ, blog, styles, favicon, OG image, robots, sitemap, CNAME)
- [x] Deploy workflow: `.github/workflows/deploy-landing.yml`
- [x] DNS guide: `docs/company/dns-setup.md`
- [ ] **Blocked:** DNS records not yet pointed to GitHub Pages (founder action)
- [ ] **Blocked:** GitHub Pages not enabled with custom domain

---

## Summary

| Area | Status | Action |
|------|--------|--------|
| Duplicate detection | DONE | — |
| Rate limiting | DONE | — |
| Device fingerprinting | PARTIAL | Add browser fingerprint, anomaly detection |
| Minimum effort threshold | GAP | Implement duration/move variety gate |
| Sybil resistance | DONE | — |
| Security audit | GAP | Formal review needed |
| Privacy review | PARTIAL | Lawyer review, telemetry opt-out UI (done), cookie consent (done) |
| Legal | PARTIAL | Lawyer review, DMCA policy (done), company formation |
| App store readiness | PARTIAL | Xcode, Android Studio, developer accounts |
| Infrastructure | PARTIAL | Fly.io deploy, Tigris, CDN, production DB |
| Monitoring | PARTIAL | Production error tracking, uptime, abuse alerting |
| Community guidelines | DONE | — |
| Launch plan | GAP | Rollout strategy, comms, success criteria |

**Blockers requiring founder action:**
1. Fly.io auth + payment method (infrastructure)
2. Xcode + Android Studio install (app store)
3. Apple Developer + Google Play Developer accounts (app store)
4. DNS records → GitHub Pages (landing page)
5. Legal structure decision (company formation)
6. Lawyer review of ToS + Privacy Policy (legal)

**Next agent work (in dependency order):**
1. Minimum effort threshold (backend + Farm)
2. Browser device fingerprinting (Farm)
3. DMCA/copyright policy doc
4. Launch plan doc
5. Security audit doc
