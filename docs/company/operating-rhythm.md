# Aura — Operating Rhythm

> **Status:** Active
> **Author:** Aura Agent
> **Last updated:** 2026-07-25

This document defines the cadence at which Aura operates. Every beat is automated. Every beat is documented.

---

## The Beats

### 1. Pulse (every 30 minutes)

**Cron job:** `aura-pulse`
**Schedule:** `*/30 * * * *`
**What it does:** Picks the highest-priority unblocked milestone item from the roadmap, works on it for ~20 minutes using OpenCode (for coding) or direct tooling (for docs/planning), commits results, pushes to GitHub, and reports to the founder via Telegram.

**Output:** A 1-2 paragraph summary of what was done, delivered to the founder's Telegram.

**Rules:**
- Never work on items whose dependencies aren't complete
- If OpenCode or the coding model is unavailable, fall back to documentation/planning
- If nothing is unblocked, report what's blocking
- If an error can't be resolved in 2 attempts, report it and move on

### 2. Watchdog (every 30 minutes, offset from pulse)

**Cron job:** `aura-watchdog`
**Schedule:** `*/30 * * * *` (runs ~30s after pulse)
**What it does:** System health checks — disk usage, memory pressure, git cleanliness, cron job health, OpenCode availability.

**Output:** "All clear." if healthy; otherwise a concise alert with severity and suggested fix.

### 3. Daily Briefing (9:00 AM daily)

**Cron job:** `aura-daily`
**Schedule:** `0 9 * * *`
**What it does:** Compiles a daily report for the founder:
- What moved (commits in last 24h)
- Pulse status (last 3 runs)
- Watchdog alerts
- Current milestone and next item
- Blockers

**Output:** Under 10 bullet points, delivered to the founder's Telegram. Ends with the single most important thing to focus on next.

### 4. Weekly Founder Review (every Monday, 10:00 AM)

**Cron job:** `aura-weekly` (to be created)
**Schedule:** `0 10 * * 1`
**What it does:** A deeper weekly retrospective:
- Milestone progress (what was completed this week, what's in flight)
- Roadmap health (any milestones at risk, dependency issues)
- Agent performance (pulse success rate, self-improvements made)
- System health trends (disk, memory, errors over the week)
- Open decisions needing founder input
- Recommended focus for the coming week

**Output:** A structured report delivered to the founder's Telegram. Includes explicit asks where founder input is needed.

### 5. Self-Improvement (after every pulse)

**Skill:** `aura-self-improve`
**What it does:** After each pulse run, the agent evaluates its own performance and patches skills or memories to improve future runs. This is the meta-cognitive layer.

**Output:** A commit with message `self-improve: [what was learned] — pulse run [N]`.

---

## Summary Table

| Beat | Frequency | Cron | Purpose |
|------|-----------|------|---------|
| Pulse | 30 min | `aura-pulse` | Advance roadmap |
| Watchdog | 30 min | `aura-watchdog` | System health |
| Daily | 9 AM daily | `aura-daily` | Founder briefing |
| Weekly | Mon 10 AM | `aura-weekly` | Retrospective + planning |
| Self-Improve | After pulse | (skill) | Meta-cognition |

---

## Communication Channels

| Channel | Use |
|---------|-----|
| **Telegram** | All cron job outputs delivered to founder (chat ID: 664767609) |
| **GitHub** | All code, docs, decisions committed to `aura-workspace` |
| **Hermes logs** | Agent-level logs at `~/.hermes/logs/` |
| **Cron output** | Archived at `~/.hermes/cron/output/` |

---

## Founder's Role

The founder (Sergio) receives:
- **Every 30 min:** Pulse report + watchdog status (Telegram)
- **Daily at 9 AM:** Consolidated briefing (Telegram)
- **Weekly on Monday:** Deep retrospective with decision points (Telegram)

The founder is never expected to prompt the agent. The agent runs autonomously. Founder input is only needed for:
- Strategic decisions (legal structure, funding, major pivots)
- Approvals that can't be automated
- Course corrections when the agent is off-track

---

## Evolution

This rhythm will evolve as Aura grows. When new beats are needed (e.g., CI monitoring, deployment checks, community moderation), they'll be added here and automated as cron jobs.
