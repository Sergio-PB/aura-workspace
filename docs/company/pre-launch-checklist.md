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

### 1.3 Device Fingerprinting — DONE

- [x] `deviceId` captured on every recording (schema: `recordings.deviceId`)
- [x] IP + geolocation captured per recording
- [x] IP clustering in anti-gaming middleware (Sybil detection)
- [x] Browser fingerprint via canvas+WebGL (`useDeviceFingerprint` hook)
- [x] Anomaly detection middleware (`device-anomaly.ts`): device diversity, geo jumps, IP churn, device+IP mismatch. Score ≥70 blocks, ≥40 flags.

### 1.4 Minimum Effort Threshold — DONE

- [x] `endSession` in `ws.ts` requires ≥30 ticks (~3s at 10 Hz) before points count
- [x] Sessions below threshold get 0 points

### 1.5 Sybil Resistance — DONE

- [x] Ed25519 keypair per device (cryptographic identity)
- [x] `anti-gaming.ts` middleware: point velocity caps, new-account restrictions, IP clustering
- [x] Self-attribution blocked (`SELF_ATTRIBUTION` error)
- [x] Reciprocal farming detection (A↔B within 24h)
- [x] User status enforcement (suspended/banned users blocked)
- [x] Anti-gaming tests: `test/anti-gaming.test.ts`

---

## 2. Security Audit — DONE

- [x] Formal security audit completed 2026-08-05: 12 findings (1 critical, 3 high, 4 medium, 4 low)
- [x] Critical + high findings fixed
- [x] Full report: `docs/security/audit-2026-08-05.md`
- [x] Auth flow reviewed (challenge-response, JWT, key storage)
- [x] API surface reviewed (all endpoints, auth requirements, input validation)
- [x] Data at rest reviewed (SQLite encryption, key management)
- [x] Dependency audit (`npm audit`, supply chain)
- [x] Rate limit bypass tested
- [x] WebSocket security reviewed

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
- [x] **Gap:** Tigris media storage not deployed (ADR-009 approved, implemented in `media.ts` + `routes/media.ts`)
- [ ] **Gap:** No CDN configured
- [ ] **Gap:** No production database (currently libSQL file-based; needs Fly Postgres or Turso for prod)

---

## 7. Monitoring — DONE

- [x] Cron monitoring stack (pulse, heartbeat, watchdog, daily, review-summary, weekly)
- [x] External launchd watchdog (`ai.aura.watchdog`, 5 min)
- [x] Error logging to `logs/errors.md`
- [x] Pre-computed health state (`pulse-health.py`)
- [x] Kanban board for roadmap visibility
- [x] Production error tracking: Sentry (`@sentry/bun`, `SENTRY_DSN`)
- [x] Structured event ring buffer + abuse alerting (`/admin/events`, `/admin/alerts`)
- [x] Health check with DB probe (`/admin/healthz`)
- [x] Webhook delivery for alerts (`AURA_ALERT_WEBHOOK_URL`)
- [x] **Gap:** No uptime monitoring (external ping service) — resolved: `scripts/uptime-monitor.py`

---

## 8. Community Guidelines — DONE

- [x] Published: `docs/community/guidelines.md` v1.0
- [x] Core principles defined
- [x] Enforcement ladder (warning → restriction → reversal → suspension → ban)
- [x] Moderation process: `docs/community/moderation.md`
- [x] Feedback loop: `docs/community/feedback-loop.md`

---

## 9. Launch Plan — DONE

- [x] Rollout strategy: `docs/product/launch-plan.md` — phased rollout (soft → friends → event → beta → public)
- [x] Comms plan: blog post, social media, founding members announcement
- [x] Success criteria: go/no-go gates per phase
- [x] Rollback plan: per-phase rollback triggers
- [x] Support plan: community channels, feedback loop
- [x] Post-launch metrics defined

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
| Device fingerprinting | DONE | — |
| Minimum effort threshold | DONE | — |
| Sybil resistance | DONE | — |
| Security audit | DONE | — |
| Privacy review | PARTIAL | Lawyer review |
| Legal | PARTIAL | Lawyer review, company formation |
| App store readiness | PARTIAL | Xcode, Android Studio, developer accounts |
| Infrastructure | PARTIAL | Fly.io deploy, Tigris, CDN, production DB |
| Monitoring | DONE | — |
| Community guidelines | DONE | — |
| Launch plan | DONE | — |

**Blockers requiring founder action:**
1. Fly.io auth + payment method (infrastructure)
2. Xcode + Android Studio install (app store)
3. Apple Developer + Google Play Developer accounts (app store)
4. DNS records → GitHub Pages (landing page)
5. Legal structure decision (company formation)
6. Lawyer review of ToS + Privacy Policy (legal)

**Next agent work (in dependency order):**
1. Tigris media storage integration (ADR-009)
2. Production database migration (libSQL → Turso/Fly Postgres)
