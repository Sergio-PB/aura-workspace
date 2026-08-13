# ADR-010: Legal Structure — Single-Member LLC

> **Status:** pending
> **Date:** 2026-08-13
> **Author:** Aura Agent

## Context

Aura needs a legal structure to: open a bank account, sign contracts (hosting, APIs), publish apps, and limit personal liability. We're bootstrapped with no funding, no employees beyond the founder, and no revenue yet.

Full analysis: `docs/company/legal-structure-recommendation.md`

## Decision

**Form a single-member LLC.**

## Rationale

- **Liability protection matters.** Aura handles biometric data (face detection) and user-generated content. Privacy claims are real.
- **Low cost, low overhead.** $70–$800 one-time + ~$100–$300/year. Delaware or Wyoming for low fees, or founder's home state for simplicity.
- **Converts cleanly to C-Corp** if/when we raise funding.
- **Credible enough** for App Store, vendors, bank account.
- **No reason to pay C-Corp overhead** before revenue or funding.

## Alternatives Considered

| Option | Rejected Because |
|--------|-----------------|
| Sole proprietorship | No liability protection — personal assets at risk with biometric data handling |
| Delaware C-Corp | Overkill for pre-revenue startup; $500+ filing + $400+/year minimum franchise tax; double taxation |

## Consequences

- **Positive:** Liability shield, business bank account possible, credible with vendors
- **Negative:** Filing fees, annual maintenance, some paperwork
- **Risk:** None — converts to C-Corp cleanly if needed

## Next Steps (after approval)

1. Founder chooses state (Delaware for standard, home state for simplicity)
2. File Articles of Organization
3. Get EIN from IRS (free, online, instant)
4. Open business bank account
5. Draft operating agreement (single-member, simple template)
