# Company Bank Account Setup

> **Status:** Research — awaiting legal structure decision
> **Author:** Aura Agent
> **Date:** 2026-07-27

## Prerequisites

- Legal structure decided (sole proprietorship or LLC — see `legal-structure-recommendation.md`)
- EIN from IRS (free, online, instant at irs.gov — needed for LLC, optional for sole prop)
- Personal ID (driver's license, passport)

## Options

### If Sole Proprietorship

Use a separate personal checking account. Not legally required but strongly recommended — don't mix Aura money with personal money.

| Bank | Why |
|------|-----|
| **Mercury** | Built for startups. Free. No minimums. Virtual + physical cards. But requires LLC/Corp — won't work for sole prop. |
| **Novo** | Free business checking. Accepts sole proprietorships. No minimums. Integrates with Stripe, Shopify, etc. |
| **Bluevine** | Free checking, 1.5% interest. Accepts sole props. |
| **Local credit union** | Often free, personal service. Good if Sergio has an existing relationship. |

**Recommendation:** Novo (free, startup-friendly, accepts sole props).

### If LLC

More options open up. Mercury becomes available (best UX for startups).

| Bank | Why |
|------|-----|
| **Mercury** | Best startup banking UX. Free. API access. Virtual cards. Built for tech companies. |
| **Brex** | Similar to Mercury. Requires some funding or revenue for full features. |
| **Novo** | Also works for LLCs. Good fallback. |
| **SVB (now First Citizens)** | Traditional. More paperwork. Overkill for pre-revenue. |

**Recommendation:** Mercury (if LLC). Novo as fallback.

## Payment Infrastructure

Don't build payment infrastructure until we have something to charge for. Aura is pre-revenue. When we need it:

| Need | Tool | When |
|------|------|------|
| Accept payments | Stripe | When we have a paid product |
| Subscription billing | Stripe Billing | When we have recurring revenue |
| In-app purchases | App Store / Play Store IAP | When apps are published |
| Expense tracking | Mercury (built-in) or QuickBooks | From day 1 of having expenses |

**For now:** Nothing. Open the bank account, that's it. Stripe integration is 2 hours of work when we need it.

## What You Need

1. **EIN letter** (if LLC) — free from IRS.gov, takes 5 minutes online
2. **Articles of Organization** (if LLC) — filed with state
3. **Operating Agreement** (if LLC) — simple template, single-member
4. **Personal ID** — driver's license or passport
5. **Initial deposit** — $0 for most online banks (Mercury, Novo)

## Execution Order

1. Decide legal structure (sole prop vs LLC)
2. If LLC: file Articles of Organization → get EIN → draft operating agreement
3. Open bank account (takes 10-30 minutes online)
4. Optionally: get a business credit card (for SaaS subscriptions, domains, etc.)

## Decision Needed

- [ ] Founder: sole proprietorship or LLC? (see `legal-structure-recommendation.md`)
- [ ] Founder: which bank? (Novo for sole prop, Mercury for LLC)
