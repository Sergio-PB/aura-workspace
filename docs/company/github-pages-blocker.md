# GitHub Pages Blocker — Private Repo Limitation

> **Status:** Discovered 2026-08-01 — needs founder decision
> **Author:** Aura Agent

## What Happened

The deploy-landing workflow has been failing on every run (5 consecutive failures) with:

```
Get Pages site failed. Please verify that the repository has Pages enabled
and configured to build using GitHub Actions.
```

Attempted to enable Pages via API:

```
gh api repos/Sergio-PB/aura-workspace/pages -X POST ...
→ HTTP 422: "Your current plan does not support GitHub Pages for this repository."
```

**Root cause:** `aura-workspace` is a **private repository** on a **free GitHub plan**. GitHub Pages is only available for private repos on GitHub Team or Enterprise plans. Free plans only support Pages on **public** repos.

## Current State

- `ifarm.club` DNS currently points to Squarespace IPs (198.49.23.144/145, 198.185.159.144/145) — showing a "Coming Soon" Squarespace page
- Landing page is fully built and ready (`landing/` directory with index, about, faq, blog, CSS, favicon, OG image, robots.txt, sitemap.xml, CNAME)
- Deploy workflow is correct but can't succeed until Pages is enabled

## Options

| Option | Cost | Effort | Notes |
|--------|------|--------|-------|
| **Make repo public** | Free | 1 click | Simplest. All code becomes public. May be fine since we "build in the open." |
| **Upgrade to GitHub Team** | $4/month | 1 click | Enables Pages on private repos. Also gets required status checks, protected branches. |
| **Cloudflare Pages** | Free | ~30 min | Free tier supports private GitHub repos. Connect repo, set build command, done. |
| **Netlify** | Free | ~30 min | Same as Cloudflare. Free tier, private repo support. |
| **Vercel** | Free | ~30 min | Same. Good DX. |

## Recommendation

**Make the repo public.** Aura's culture is transparency and "built in the open." The landing page already links to the GitHub repo. There's nothing sensitive in the repo (no secrets, no keys). This is the zero-effort, zero-cost path that aligns with company values.

If the founder prefers to keep the repo private, Cloudflare Pages is the best free alternative — it has the same simple static-site deploy model as GitHub Pages.

## What Changes

Whichever option is chosen, the DNS records in `docs/company/dns-setup.md` will need updating (different IPs for Cloudflare/Netlify/Vercel vs GitHub Pages).

## Next Step

Founder decision needed. Once decided, I can:
- Make repo public (1 click) OR set up alternative hosting
- Update DNS setup guide with correct IPs
- Verify the deploy workflow succeeds
- Check off the C-1 DNS/hosting item
