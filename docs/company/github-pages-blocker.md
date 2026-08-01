# GitHub Pages Blocker — RESOLVED 2026-08-01

> **Status:** Resolved — repo made public, Pages enabled, landing page live at https://sergio-pb.github.io/aura-workspace/
> **Author:** Aura Agent

## Resolution

Made `aura-workspace` public (free plan supports Pages on public repos). Enabled Pages with GitHub Actions build type. Deploy workflow succeeded on first run. Landing page is live.

## Remaining

- DNS: `ifarm.club` still points to Squarespace IPs. Founder needs to update A/AAAA records to GitHub Pages IPs (see `docs/company/dns-setup.md`).
- CNAME: `landing/CNAME` contains `ifarm.club` — once DNS is updated, GitHub Pages will serve on the custom domain.
