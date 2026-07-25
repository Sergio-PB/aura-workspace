# Workspace Health Baseline

> Established: 2026-07-25 (Pulse Run #1)
> Updated: automatically by aura-watchdog and aura-pulse

## System

| Metric | Baseline | Threshold | Current |
|--------|----------|-----------|---------|
| Disk usage (/) | 3% (9.6 GiB / 460 GiB) | Alert >85% | 3% |
| Memory used | ~11 GB / 16 GB (69%) | Alert >90% | 69% |
| Memory pressure | Normal | Alert if not Normal | Normal |
| CPU | M1 Pro (8 perf + 2 eff) | — | — |
| macOS | 14.8.7 | — | — |

## Git State

| Repo | Status | Last Commit |
|------|--------|-------------|
| aura-workspace | Clean | 745f906 (W-1: switch to OpenCode) |
| aura-apps | Clean | — |

## Cron Jobs

| Job | Schedule | Status |
|-----|----------|--------|
| aura-pulse | */30 * * * * | Active |
| aura-watchdog | */30 * * * * | Active |
| aura-daily | 0 9 * * * | Active |

## Agent

| Component | Version | Status |
|-----------|---------|--------|
| Hermes Agent | v0.19.0 | Running |
| OpenCode | v1.18.5 | Working (Ollama/Caveman) |
| DeepSeek v4 Pro | ollama-cloud | Available |
| Ollama (local) | — | 5 models loaded |

## Notes

- OpenCode uses local Ollama with Caveman model (kavai/Caveman-Library:qwen3-5-2b) — no cloud API keys needed
- All three cron jobs are active and properly scheduled
- Disk usage is negligible (3%) — no storage concerns
- Memory at 69% is healthy for a dev machine
