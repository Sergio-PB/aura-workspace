# DNS Setup: ifarm.club → GitHub Pages

> **Status:** Ready to execute — awaiting founder action
> **Author:** Aura Agent
> **Date:** 2026-07-27

## What This Does

Points `ifarm.club` (and `www.ifarm.club`) to the landing page hosted on GitHub Pages. The landing page is already built (`landing/index.html`), the deploy workflow is ready (`.github/workflows/deploy-landing.yml`), and the CNAME file exists (`landing/CNAME`). Only DNS and a repo setting remain.

## Step 1: Configure DNS Records

Go to your domain registrar's DNS management panel and add these records:

### A Records (apex domain)

| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

### AAAA Records (apex domain, IPv6)

| Type | Name | Value |
|------|------|-------|
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |

### CNAME Record (www subdomain)

| Type | Name | Value |
|------|------|-------|
| CNAME | www | Sergio-PB.github.io |

> **Note:** These are GitHub Pages' static IPs. They rarely change, but verify at https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site if something doesn't work.

## Step 2: Enable GitHub Pages

1. Go to https://github.com/Sergio-PB/aura-workspace/settings/pages
2. Under "Build and deployment":
   - **Source:** GitHub Actions
3. Under "Custom domain":
   - Enter: `ifarm.club`
   - Click **Save**
4. Wait for the "DNS Check" to pass (can take up to 24 hours, usually ~15 minutes)

## Step 3: Verify

```bash
# Check DNS propagation
dig ifarm.club +short
# Should return one of the GitHub IPs above

# Check HTTPS
curl -I https://ifarm.club
# Should return HTTP/2 200

# GitHub Pages will auto-provision a Let's Encrypt TLS certificate.
# This can take a few minutes after DNS propagates.
```

## What Happens After

- `ifarm.club` → landing page (live to the world)
- `www.ifarm.club` → redirects to `ifarm.club`
- Any push to `landing/` on `main` auto-deploys via GitHub Actions
- TLS certificate auto-renews via Let's Encrypt

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| DNS check fails | Wait 15 min, retry. DNS TTL can delay propagation. |
| HTTPS not working | GitHub takes ~5 min to provision cert after DNS passes. Check Settings → Pages for status. |
| 404 on apex domain | Verify A records point to the exact IPs above. Some registrars use `@` for apex, others leave name blank. |
| www subdomain not redirecting | CNAME record must point to `Sergio-PB.github.io` (not `ifarm.club`). |
