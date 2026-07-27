# Public Presence Strategy

> **Status:** Draft — awaiting founder review
> **Author:** Aura Agent
> **Date:** 2026-07-27

## Current State

Aura has zero public presence. The repo is private. No social accounts. No domain email. The landing page is built but not deployed (waiting on DNS).

## What We Need

### 1. Domain Email

`ifarm.club` needs at least:
- `hello@ifarm.club` — public contact
- `sergio@ifarm.club` — founder

**Options:**

| Option | Cost | Effort |
|--------|------|--------|
| **Forward Email** (forwardemail.net) | Free | 5 min — add MX records, configure forwards to personal Gmail |
| **Google Workspace** | $6/mo | 30 min — full Gmail interface, Drive, etc. |
| **iCloud+ Custom Domain** | Included with iCloud+ | 10 min — if Sergio has iCloud+ already |
| **Zoho Mail** | Free (up to 5 users) | 15 min — webmail or IMAP |

**Recommendation:** Forward Email (free, zero maintenance) for now. Upgrade to Google Workspace when we need a proper inbox. iCloud+ is also zero-cost if Sergio already pays for it.

### 2. GitHub Org

Currently: `Sergio-PB/aura-workspace` (personal account, private).

**Option A: Keep as-is.** Private repos under personal account. Simple, zero overhead. Flip to public when ready.

**Option B: Create `aura-network` org.** Separate identity. Can add collaborators later. Free for private repos.

**Recommendation:** Option A for now. Create the org when we have something public to show (landing page live, first product screenshots). No reason to create an empty org.

### 3. Social Accounts

Claim handles before someone else does. Don't post yet — just reserve.

| Platform | Handle | Priority | Notes |
|----------|--------|----------|-------|
| Twitter/X | `@ifarmclub` or `@auradotclub` | High | Reserve now, even if private |
| Instagram | `@ifarm.club` | High | Visual product → Instagram matters |
| TikTok | `@ifarm.club` | Medium | Depends on content strategy |
| LinkedIn | Company page | Low | Not consumer-facing, but good for hiring later |
| Discord | Server | Medium | Community hub when N-1 launches |

**Action:** Sergio should claim these handles. Use `hello@ifarm.club` as the email for all accounts (once email is set up).

### 4. GitHub Repo Visibility

When to flip `aura-workspace` from private → public:
- Landing page is live
- Brand identity is finalized
- At least one product has a working demo (P-3 or P-4)
- Legal structure is decided (C-1)

**Recommendation:** Keep private until P-6 (end-to-end integration) is verified. Open-sourcing too early creates noise without signal.

## Execution Order

1. **DNS + landing page** (blocked on founder — see `dns-setup.md`)
2. **Domain email** (can do immediately after DNS)
3. **Claim social handles** (can do immediately, use personal email until domain email exists)
4. **GitHub org** (defer until public launch)
5. **First social post** (defer until landing page is live)

## Decision Needed

- [ ] Founder: which email provider? (Forward Email / iCloud+ / Google Workspace / Zoho)
- [ ] Founder: claim social handles now or wait?
- [ ] Founder: keep repo private until P-6, or open earlier?
