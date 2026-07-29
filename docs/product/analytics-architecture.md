# Analytics Architecture

> **Status:** Draft
> **Author:** Aura Agent
> **Date:** 2026-07-29
> **Track:** C-2 (Go-to-Market)

## Principles

1. **Privacy-first.** No third-party trackers. No PII in analytics. No fingerprinting. Users own their data.
2. **Actionable, not vanity.** Every metric must drive a decision. No dashboards for dashboards' sake.
3. **Opt-in by default.** Core product metrics are anonymized and essential. Detailed telemetry is opt-in.
4. **Transparent.** Users can see what we track. The analytics schema is public.

## What We Track

### Product Health (always-on, anonymized)

| Metric | Why | Source |
|--------|-----|--------|
| DAU/WAU/MAU | Is the product alive? | Backend auth events |
| Events created per day | Are people using The Farm? | Backend event API |
| Attributions per event | Are people giving points? | Backend attribution API |
| Validations per attribution | Is community consensus working? | Backend validation API |
| Claim rate (% of attributions claimed) | Are people engaging with The Card? | Backend claim API |
| Feed views per user | Is the social feed sticky? | Card client heartbeat |
| Error rate (5xx, crash reports) | Is the product stable? | Backend logs, client crash handler |

### Growth (anonymized)

| Metric | Why | Source |
|--------|-----|--------|
| New user signups | Growth rate | Backend auth |
| Invite conversion (% of invites accepted) | Is the invite system working? | Backend invite API |
| Retention (D1, D7, D30) | Are users coming back? | Backend auth events |
| Time to first attribution | How fast do users get value? | Backend attribution API |

### Quality (anonymized)

| Metric | Why | Source |
|--------|-----|--------|
| Attribution challenge rate | Are people gaming the system? | Backend validation API |
| Consensus time (attribution → resolved) | Is validation fast enough? | Backend validation API |
| Media upload success rate | Is the pipeline reliable? | Farm client |
| Sync latency (Farm → Card visibility) | Is the feed real-time enough? | Backend event pipeline |

### Business (if monetized later)

| Metric | Why | Source |
|--------|-----|--------|
| Revenue | Are we sustainable? | Payment processor |
| Conversion rate | Is the product worth paying for? | Payment processor |
| Churn rate | Are we losing paying users? | Payment processor |

## What We Don't Track

- Individual user behavior (no session recordings, no click heatmaps)
- PII in analytics (no emails, names, IPs in analytics DB)
- Cross-site tracking (no cookies, no fingerprinting)
- Device telemetry beyond what's needed for debugging (no battery, no installed apps)
- Content of recordings (no media analysis for analytics)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Farm Client  │────▶│              │────▶│  Analytics  │
│ (anonymized) │     │   Backend    │     │     DB      │
└─────────────┘     │  /analytics   │     │  (SQLite    │
                    │   endpoint    │     │   or PG)    │
┌─────────────┐     │              │     └─────────────┘
│ Card Client  │────▶│              │
│ (anonymized) │     │              │     ┌─────────────┐
└─────────────┘     └──────────────┘     │  Admin       │
                                         │  Dashboard   │
                                         │  (P-5)       │
                                         └─────────────┘
```

### Data Flow

1. **Client-side:** Farm and Card emit anonymized events (no PII, no IPs). Events are batched and sent on an interval (5 min) or on app background.
2. **Backend:** `/analytics/events` endpoint accepts batches. Validates schema, drops anything with PII, writes to analytics DB.
3. **Storage:** Separate analytics DB (SQLite to start, same as main DB). Partitioned by day. Raw events retained 90 days, aggregates forever.
4. **Query:** Admin dashboard queries aggregates. No raw event access without explicit audit log.

### Event Schema

```typescript
interface AnalyticsEvent {
  event: string;           // e.g. "app.open", "attribution.create"
  timestamp: string;       // ISO 8601
  session_id: string;      // random UUID, rotated on app restart
  user_id_hash: string;    // SHA-256 of user ID, for retention cohorts
  properties: Record<string, string | number | boolean>;
  // properties must NOT contain: emails, names, IPs, locations, media URLs
}
```

### Privacy Guarantees

- `user_id_hash` is one-way hashed — can't reverse to user ID
- `session_id` is random and rotated — can't correlate across sessions
- No IP logging on analytics endpoint
- No geolocation in analytics properties
- Users can view their own analytics data via API
- Users can delete their analytics data (GDPR right to erasure)

## Implementation Plan

### Phase 1: Backend endpoint (P-5 scope)

- [ ] `POST /analytics/events` — accept batched events
- [ ] Schema validation + PII scrubber
- [ ] Analytics DB table + migrations
- [ ] Daily aggregation cron (raw → hourly → daily → weekly)

### Phase 2: Client SDK (shared package)

- [ ] `@aura/analytics` package in monorepo
- [ ] `Analytics.track(event, properties)` — fire-and-forget
- [ ] Batching + retry + offline queue
- [ ] Opt-out flag (stored locally, no network call needed)

### Phase 3: Admin dashboard (P-5 scope)

- [ ] Basic charts: DAU, events, attributions, error rate
- [ ] Retention cohort table
- [ ] Export to CSV

### Phase 4: Alerts (post-launch)

- [ ] Error rate spike → Telegram alert
- [ ] DAU drop >20% → Telegram alert
- [ ] Pipeline failure (0 events for 1h) → Telegram alert

## Decisions

- **No third-party analytics.** No Mixpanel, no Amplitude, no PostHog. We build it. Privacy is a core value, not a feature.
- **SQLite for analytics DB.** Same as main DB. Separate at scale (P-10).
- **No real-time dashboard.** Aggregates updated hourly. Real-time is a P-10 concern.
- **No A/B testing framework yet.** Not needed until we have enough users to measure. Add when DAU > 1000.

## Open Questions

- Should we track "time spent in app"? Leans toward session recording — probably not.
- Should we track feature adoption (which features are used)? Yes, but only at the feature level, not per-user.
- Should analytics be open-source? The schema and aggregation logic, yes. Raw data, no.
