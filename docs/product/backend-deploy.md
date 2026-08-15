# Backend Deployment — Fly.io

> **Status:** Ready for founder action
> **Author:** Aura Agent
> **Date:** 2026-07-31

## What's Ready

- **Code:** 103 tests pass, Bun + Hono + libSQL
- **Dockerfile:** `apps/backend/Dockerfile` — Bun Alpine, single-stage
- **fly.toml:** `apps/backend/fly.toml` — iad region, auto-stop, HTTP health checks
- **CI/CD:** `.github/workflows/deploy-backend.yml` — deploys on push to main when backend files change

## What's Needed (Founder Action)

### 1. Install Fly CLI + Auth

```bash
brew install flyctl   # already installed
flyctl auth login     # opens browser, sign up/login
```

### 2. Create the App

```bash
cd aura-apps/apps/backend
flyctl apps create aura-backend
```

### 3. Set Secrets

```bash
# Generate a secure session secret
flyctl secrets set SESSION_SECRET="$(openssl rand -hex 32)"

# Set any other env vars from .env.example
flyctl secrets set DATABASE_URL="file:./data.db"
```

### 4. Deploy

```bash
flyctl deploy
```

Or push to main — the GitHub Actions workflow handles it automatically.

### 5. Add FLY_API_TOKEN to GitHub Secrets

For CI/CD deploys:
1. Run `flyctl auth token`
2. Go to https://github.com/Sergio-PB/aura-apps/settings/secrets/actions
3. Add `FLY_API_TOKEN` with the token value

## Post-Deploy

```bash
# Check status
flyctl status

# View logs
flyctl logs

# Open in browser
flyctl open
```

The app will be at `https://aura-backend.fly.dev`.

## Notes

- **Free tier:** Fly.io free allowance covers 3 shared-cpu-1x VMs with 256 MB RAM. Our Bun app uses ~50 MB at idle.
- **Auto-stop:** `auto_stop_machines = true` means the VM sleeps when idle and wakes on request (cold start ~1-2s).
- **PostgreSQL:** Uncomment the `[[postgres]]` block in fly.toml when ready for Fly Postgres. Currently using libSQL (file-based).
- **Tigris (media storage):** ADR-009 approved. `src/media.ts` + `routes/media.ts` implemented. To enable, create a Tigris bucket and set the S3 env vars (see `.env.example`):
  ```bash
  flyctl storage create          # creates a Tigris bucket, prints creds
  flyctl secrets set AWS_ENDPOINT_URL_S3="https://fly.storage.tigris.dev" \
    AWS_REGION="auto" \
    AWS_ACCESS_KEY_ID="<tigris-access-key>" \
    AWS_SECRET_ACCESS_KEY="<tigris-secret>" \
    S3_BUCKET="aura-media"
  ```
