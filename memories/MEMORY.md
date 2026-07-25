# Aura Agent — Operational Memory

Last updated: 2026-07-25

## Identity
I am Aura Agent, the autonomous operator of Aura. I run the startup. My persona is defined in ~/.hermes/SOUL.md and mirrored in the workspace repo.

## Workspace
- Repo: github.com/Sergio-PB/aura-workspace (private)
- Local: /Users/sergio/aura-workspace
- Hardware: Apple M1 Pro, 16 GB RAM, 460 GB SSD, macOS 14.8.7
- Agent: Hermes v0.19.0, DeepSeek v4 Pro (ollama-cloud)
- Local models: kimi-k2.7-code, qwen3.5 (9b, 2b), glm-4.7-flash, LFM2-8B, Caveman-Library
- Coding agent: OpenCode v1.18.5 with kavai/Caveman-Library:qwen3-5-2b

## Products
- **The Farm:** local media studio — telemetry (IP, geolocation, face recognition) from camera/media, aura point uploads
- **The Card:** identification beacon — unique user/IP ID, point claiming, social feed with quick reactions

## Company Culture
1. Transparency — everything documented, everything committed
2. Automation — if it happens twice, it becomes a skill
3. Self-improvement — every interaction ends with a takeaway
4. Founder time is sacred — async, summarized, actionable

## Current State
- Bootstrap complete: 2026-07-24
- Cron jobs active: aura-pulse (30min), aura-watchdog (30min), aura-daily (9am), aura-weekly (Mon 10am)
- W-1 milestone: fully complete (agent autonomy foundation)
- C-1 milestone: brand identity done, operating rhythm done, compliance drafts done (privacy policy + ToS in docs/legal/, awaiting lawyer review); remaining: legal structure, DNS, bank, public presence
- No cloud infrastructure
- No product code written yet (products are in design phase)
- Founder: Sergio, interacts daily via CLI or Telegram

## Conventions
- Commit everything to aura-workspace
- ADRs for non-trivial decisions
- Skills over scripts for reusable procedures
- Cron over polling for recurring work
- Verify subagent claims before reporting
- For documentation-heavy tasks (brand, planning, ADRs), write directly rather than delegating to OpenCode — OpenCode is for code
- `hermes cron create` takes positional args: `hermes cron create "<schedule>" "<prompt>" --name <name> --deliver <target> --workdir <path>` — schedule and prompt are positional, not --flag style
