# Aura — Monetization Strategy

> **Status:** Draft — pending founder review
> **Author:** Aura Agent
> **Date:** 2026-07-29

## Context

Aura is a social reputation network. The core mechanic — recording real-world moments and attributing aura points — is inherently social and community-driven. Monetization must align with the company's values: transparency, fairness, and community governance. It must not create perverse incentives (pay-to-win reputation, algorithmic engagement bait).

We are bootstrapped, pre-revenue, with no funding. This strategy outlines paths to sustainability without compromising the product's integrity.

## Principles

1. **Never sell reputation.** Aura points cannot be bought. Period.
2. **Never sell user data.** Telemetry stays on-device by default. What's shared is user-controlled.
3. **Never optimize for engagement.** No ad-driven model. No algorithmic feeds designed to maximize time-on-screen.
4. **Value must precede revenue.** Users must love the free product before we ask for money.

## Strategy: Freemium + Event Economy

### Phase 1: Free Forever (Now → Public Beta)

Everything is free. No paywalls. No limits. Goal: grow the network.

- Unlimited recordings, attributions, validations
- Unlimited events and participants
- Full telemetry features (face recognition, audio detection, etc.)
- Full Card features (feed, reactions, profile)

**Why:** Network effects are the moat. A reputation network with 100 users is worthless; one with 10,000 is defensible. Charging early caps growth.

### Phase 2: Premium Features (Post Public Beta)

Introduce optional paid tiers that enhance — not gate — the experience.

| Feature | Free | Premium ($5/mo) |
|---------|------|-----------------|
| Recordings | Unlimited | Unlimited |
| Event participants | Unlimited | Unlimited |
| Feed | Standard | Standard |
| Profile customization | Basic | Custom colors, badges, flair |
| Analytics dashboard | — | Personal reputation trends, event stats |
| Export reputation | — | Portable reputation package (verified JSON) |
| API access | — | Personal API key for integrations |
| Storage retention | 90 days | Permanent (or configurable) |
| Early access | — | Beta features |

**Why these:** They're power-user features. Casual users lose nothing. Heavy users (event organizers, community leaders) get tools they'll pay for. None of them affect the core reputation mechanic.

### Phase 3: Event Economy (When Network Is Large)

The real monetization opportunity is the event layer.

**Event Organizer Tools ($20–$100/mo):**
- Multi-Farm management dashboard
- Event analytics (attribution heatmaps, engagement metrics)
- Custom event branding
- Exportable event reports
- Priority support

**Event Sponsorship Marketplace (10–20% platform fee):**
- Brands sponsor events → attendees earn bonus aura points
- Transparent: "Sponsored by X" is visible on every attribution
- Community-governed: sponsors must be approved, can be challenged
- No algorithmic placement — sponsors appear in chronological feed alongside organic content

**Why this works:** Events are where Aura happens. Organizers already pay for event tools (Eventbrite, etc.). Sponsors already pay for brand exposure at events. Aura adds the reputation layer — "this brand sponsored an event where real people earned real points." That's more valuable than an ad impression.

### Phase 4: Enterprise/API (Long-Term)

If the network grows large enough:

- **Verified Organization accounts** — companies, venues, festivals get verified badges
- **Reputation API** — third parties query public reputation data (with user consent)
- **White-label event reputation** — embed Aura attribution in third-party event apps

## What We Will NOT Do

| Anti-pattern | Why |
|-------------|-----|
| Sell aura points | Destroys trust. Reputation must be earned. |
| Ad-supported feed | Creates engagement optimization incentives. |
| Sell user data | Violates privacy-by-design principle. |
| Pay-to-boost (promoted posts) | Creates inequality in visibility. |
| Transaction fees on point transfers | Points aren't currency. |
| NFT/crypto integration | Unnecessary complexity, environmental concerns, wrong audience. |

## Revenue Projections (Speculative)

These are order-of-magnitude estimates, not forecasts.

| Phase | Users | Conversion | Monthly Revenue |
|-------|-------|------------|-----------------|
| Phase 1 (free) | 0–1,000 | 0% | $0 |
| Phase 2 (premium) | 1,000–10,000 | 3–5% | $150–$2,500/mo |
| Phase 3 (events) | 10,000–100,000 | 1–3% organizers + sponsorships | $5,000–$50,000/mo |
| Phase 4 (enterprise) | 100,000+ | Enterprise deals | Variable |

## Immediate Actions

- [ ] Founder review and approval of this strategy
- [ ] No code changes needed until Phase 2
- [ ] When Phase 2 begins: Stripe integration for subscriptions
- [ ] When Phase 3 begins: event organizer dashboard, sponsorship marketplace

## Open Questions

1. Should premium be subscription-only, or also offer lifetime/one-time options?
2. Should event organizers get a free tier (e.g., first 3 events free)?
3. Should we take investment to accelerate growth, or stay bootstrapped? (See funding strategy doc — TBD)
4. What's the right price point for emerging markets vs. developed markets?

## References

- [Company Plan](../company/plan.md)
- [Analytics Architecture](./analytics-architecture.md)
- [Brand Guidelines](../company/brand.md)
- [Bank Setup Guide](../company/bank-setup.md) — payment infrastructure when needed
