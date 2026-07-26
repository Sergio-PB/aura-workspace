# Legal Structure Recommendation

> **Status:** Draft — awaiting founder decision
> **Author:** Aura Agent
> **Date:** 2026-07-26

## Context

Aura needs a legal structure to: open a bank account, sign contracts (hosting, APIs), publish apps, and limit personal liability. We're bootstrapped with no funding, no employees beyond the founder, and no revenue yet.

## Options

### 1. Sole Proprietorship (do nothing)

**What it is:** Sergio operates as an individual. No registration, no separate entity.

| Pro | Con |
|-----|-----|
| Zero cost, zero paperwork | No liability protection — personal assets at risk |
| Simplest tax filing (Schedule C) | Harder to raise funding later |
| Can convert to LLC later | Less credible with partners/vendors |
| Immediate — start today | App Store requires D-U-N-S number for organizations (but individuals can publish) |

**Cost:** $0
**Timeline:** Now

### 2. Single-Member LLC

**What it is:** A separate legal entity with one owner. Pass-through taxation (no corporate tax, income flows to owner's return).

| Pro | Con |
|-----|-----|
| Liability protection (personal assets shielded) | Filing fees ($70–$800 depending on state) |
| Pass-through taxation (no double tax) | Annual report/franchise tax in some states |
| Credible with vendors, partners, App Store | Some paperwork to maintain |
| Easy to convert to multi-member or C-Corp later | Need registered agent (can be self) |
| Can open business bank account | |

**Cost:** $70 (Delaware) to $800 (California) one-time + ~$100–$300/year
**Timeline:** 1–4 weeks

### 3. Delaware C-Corporation

**What it is:** Full corporation. Required for VC funding. Double taxation (corporate + dividend).

| Pro | Con |
|-----|-----|
| Required for institutional VC | Expensive ($500+ filing, $400+/year franchise tax) |
| Stock options possible | Double taxation |
| Most credible structure | Significant paperwork, board meetings, minutes |
| | Overkill for pre-revenue startup |

**Cost:** $500+ one-time + $400+/year minimum franchise tax
**Timeline:** 4–8 weeks

## Recommendation: Single-Member LLC

**Why:**
- Liability protection matters — Aura handles biometric data (face detection) and user-generated content. Privacy claims are real.
- Low cost, low overhead. Delaware or Wyoming for low fees, or Sergio's home state for simplicity.
- Converts cleanly to C-Corp if/when we raise funding.
- Credible enough for App Store, vendors, bank account.
- No reason to pay C-Corp overhead before revenue or funding.

**If liability isn't a concern yet:** Sole proprietorship works for now. The App Store accepts individual publishers. But the bank account and vendor relationships are harder without an entity.

## Next Steps (if LLC chosen)

1. Choose state (Delaware for standard, home state for simplicity)
2. File Articles of Organization
3. Get EIN from IRS (free, online, instant)
4. Open business bank account
5. Draft operating agreement (single-member, simple template)

## Decision Needed

- [ ] Founder: choose sole proprietorship or LLC
- [ ] If LLC: which state?
