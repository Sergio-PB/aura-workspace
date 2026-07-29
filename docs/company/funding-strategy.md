# Aura — Funding Strategy

> **Status:** Draft — pending founder review
> **Author:** Aura Agent
> **Date:** 2026-07-29

## Context

Aura is bootstrapped, pre-revenue, with a solo founder and an autonomous agent operator. The monetization strategy (freemium + event economy) projects $0 revenue through Phase 1 (0–1,000 users) and modest revenue ($150–$2,500/mo) at Phase 2 (1,000–10,000 users). This document answers: do we raise money, and if so, when and how?

## Principles

1. **Values-aligned capital only.** Money that demands we compromise on privacy, transparency, or community governance is not worth taking.
2. **Raise when we have leverage, not when we need it.** Desperation fundraising is a race to the bottom.
3. **Revenue before investment.** Prove someone will pay before asking investors to believe they will.
4. **Default alive.** The company should be able to survive indefinitely on $0 external capital. Investment accelerates, it doesn't rescue.

## Recommendation: Stay Bootstrapped Through Phase 2

### Phase 1 (Now → Public Beta): $0 needed

- Solo founder, no salary draw
- Agent operator runs on existing hardware (M1 Pro)
- No cloud costs (local-first architecture, no backend until P-5)
- Domain + GitHub Pages = ~$15/year
- Open source tooling, free tiers for everything

**Burn rate: effectively $0/mo.** There is nothing to fund.

### Phase 2 (Public Beta → 10,000 users): Bootstrap

- Cloud costs begin (Fly.io hobby tier: ~$5–25/mo)
- Media storage (Cloudflare R2 or similar: ~$0–50/mo at this scale)
- Optional: founder begins drawing minimal salary if revenue supports it
- Premium subscriptions ($5/mo) at 3–5% conversion on 1,000–10,000 users = $150–$2,500/mo

**Burn rate: $50–$200/mo.** Revenue covers costs. No funding needed.

### Phase 3 (10,000+ users, event economy): Decision Point

At this stage, two paths:

**Path A: Stay bootstrapped.** Revenue from event organizer tools + sponsorship marketplace ($5,000–$50,000/mo) funds a small team (2–4 people). Grow organically. No dilution. Full control.

**Path B: Raise a seed round.** If the network shows strong growth and the event economy is working, raise $500K–$1.5M to hire a team (5–10 people) and accelerate. This is the "pour fuel on the fire" scenario.

**Decision criteria for Path B:**
- 10,000+ active users with month-over-month growth > 20%
- Event economy showing real revenue (not just projections)
- Clear customer acquisition cost (CAC) and lifetime value (LTV) metrics
- Founder wants to scale faster than organic growth allows

## If We Raise: What It Looks Like

### Instrument: SAFE (Simple Agreement for Future Equity)

- Standard Y Combinator SAFE with a valuation cap
- No board seats, no preferred shares, no investor control
- Converts to equity at next priced round (Series A or acquisition)

### Target: $500K–$1.5M Seed

| Use of Funds | Allocation |
|-------------|------------|
| Engineering (2–3 hires) | 50–60% |
| Design (1 hire) | 10–15% |
| Community/ops (1 hire) | 10–15% |
| Infrastructure & tools | 5–10% |
| Legal, compliance, misc | 5–10% |

### Ideal Investor Profile

- **Values-aligned:** understands and supports privacy-by-design, community governance, no ad model
- **Patient capital:** comfortable with 7–10 year horizon, not pushing for a quick flip
- **Consumer social experience:** has backed social networks before, understands cold start and network effects
- **Operationally helpful:** introductions to event industry, community builders, potential early adopters

### Red Flags (Walk Away)

- Demands ad-based monetization
- Pushes for data sales or surveillance model
- Wants crypto/token integration
- Demands board control or veto rights
- Pressures for rapid growth at expense of community trust

## What We Will NOT Do

| Anti-pattern | Why |
|-------------|-----|
| Raise before we have users | No leverage. Bad terms. Distraction from building. |
| Raise before we have revenue | Investors price risk higher. Revenue is proof. |
| Take money from misaligned investors | Values are the product. Compromising them kills the company. |
| Raise to pay founder salary pre-revenue | Founder should have other income or savings. Investment is for growth, not lifestyle. |
| ICO / token sale / crypto | Wrong audience, regulatory risk, doesn't align with product. |

## Immediate Actions

- [ ] Founder review and approval of this strategy
- [ ] No fundraising activity until Phase 3 decision point
- [ ] Track metrics that matter for future fundraising: MAU, retention, revenue, CAC, LTV
- [ ] When approaching Phase 3: build investor target list, prepare pitch deck

## Open Questions

1. Should we consider grants (e.g., privacy tech, open source, EU innovation funds) as non-dilutive funding?
2. Is there a scenario where a very small pre-seed ($50K–$100K) from aligned angels makes sense before Phase 3?
3. Should the founder take a salary from revenue before the company is profitable, or reinvest everything?

## References

- [Monetization Strategy](../product/monetization-strategy.md)
- [Company Plan](../company/plan.md)
- [Bank Setup Guide](./bank-setup.md)
- [Legal Structure Recommendation](./legal-structure-recommendation.md)
