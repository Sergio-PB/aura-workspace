# ADR-001: Workspace Bootstrap and Autonomous Agent Architecture

Date: 2026-07-24
Status: accepted

## Context

Aura is being bootstrapped from scratch. The company has a clear product vision (The Farm + The Card) but no existing code, infrastructure, or operational processes. The founder (Sergio) wants an autonomous agent to run the startup — not just assist with it.

Key constraints:
- No cloud infrastructure yet
- Single developer machine (Apple M1 Pro, 16 GB RAM)
- Hermes Agent v0.19.0 as the agent runtime
- Private GitHub repo as the single source of truth

## Decision

1. **Hermes Agent as the autonomous operator.** The agent runs the startup via a custom persona (SOUL.md) that encodes company culture, operating principles, and product context. The agent is proactive, self-improving, and transparent.

2. **aura-workspace as the single source of truth.** All code, docs, skills, memories, and decisions live in one private GitHub repo. Nothing important exists only in session memory.

3. **Skills as the unit of reusable procedure.** Recurring work patterns become Hermes skills. One-off scripts go in `scripts/`. Cron jobs handle scheduled work.

4. **ADRs for all non-trivial decisions.** Architecture Decision Records in `docs/adr/` following the standard format.

5. **Memory export to repo.** Persistent agent memories are mirrored to `memories/MEMORY.md` and `memories/USER.md` in the repo for transparency and backup.

## Consequences

- The agent's persona is now Aura-specific, not the stock Hermes default
- All future work is committed to aura-workspace
- The founder interacts daily via CLI or Telegram
- The agent is expected to be proactive — identifying work, suggesting initiatives, automating itself
- Skills and cron jobs will grow organically as patterns emerge
