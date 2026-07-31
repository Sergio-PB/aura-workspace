# Pre-Launch Checklist — ifarm.club

> **Status:** Ready for founder action
> **Last updated:** 2026-07-31

## Before Going Live

- [ ] **DNS records** — Add A/AAAA/CNAME records per `docs/company/dns-setup.md`
- [ ] **GitHub Pages** — Enable in repo Settings → Pages, set custom domain to `ifarm.club`
- [ ] **TLS cert** — Auto-provisioned by GitHub after DNS propagates (~5 min)
- [ ] **Verify HTTPS** — `curl -I https://ifarm.club` returns 200
- [ ] **Verify www redirect** — `curl -I https://www.ifarm.club` redirects to apex
- [ ] **Verify subpages** — `/about`, `/faq`, `/blog` all load
- [ ] **Verify OG tags** — Paste `https://ifarm.club` into Twitter/Discord/Slack to check link preview
- [ ] **Verify robots.txt** — `curl https://ifarm.club/robots.txt`
- [ ] **Verify sitemap** — `curl https://ifarm.club/sitemap.xml`
- [ ] **Google Search Console** — Submit sitemap for indexing
- [ ] **Announce** — Blog post, social media, founding members

## Landing Page Assets (All Present)

| Asset | Path | Status |
|-------|------|--------|
| Homepage | `landing/index.html` | ✅ |
| About | `landing/about.html` | ✅ |
| FAQ | `landing/faq.html` | ✅ |
| Blog | `landing/blog/index.html` | ✅ |
| Styles | `landing/style.css` | ✅ |
| Favicon | `landing/favicon.svg` | ✅ |
| OG Image | `landing/og-image.svg` | ✅ |
| Robots | `landing/robots.txt` | ✅ |
| Sitemap | `landing/sitemap.xml` | ✅ |
| CNAME | `landing/CNAME` | ✅ (`ifarm.club`) |
| Deploy workflow | `.github/workflows/deploy-landing.yml` | ✅ |

## Post-Launch

- [ ] Set up Google Analytics or Plausible (privacy-first)
- [ ] Add email signup form (waitlist)
- [ ] Monitor GitHub Pages bandwidth (100 GB/month free tier)
