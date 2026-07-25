# AGENTS.md — Aura Workspace

This file is loaded by Hermes Agent as project context when working in this repository.

## Project Identity

Aura is a startup building a fair community based on social scores. Two products, served at ifarm.club:

1. **The Farm** — local media studio app. Captures telemetry from camera/local media: IP, geolocation, face recognition IDs. Users record moments and upload "aura points" to themselves or others. Think Instagram games where you interact by speaking or gesturing.

2. **The Card** — identification beacon. Uniquely identifies users and their IPs. Lets users claim points attributed by a Farm. Social feed with quick reactions.

Core mechanic: record someone doing something notable → upload → they gain aura points. Others at the same event can confirm or challenge the attribution.

Backend validates and attributes aura by triangulating/correlating input, and/or by community consensus.

## Repository Structure

```
aura-workspace/
├── README.md              # Public-facing overview
├── AGENTS.md              # This file — Hermes project context
├── docs/
│   ├── architecture.md    # System architecture
│   ├── adr/               # Architecture Decision Records
│   └── company/
│       └── culture.md     # Company culture and values
├── src/
│   ├── farm/              # The Farm — local media studio
│   └── card/              # The Card — identification beacon
├── scripts/               # One-off automation scripts
├── skills/                # Custom Hermes skills (exported from ~/.hermes/skills/)
├── memories/              # Persistent agent memories
│   ├── MEMORY.md          # Agent's operational memory
│   └── USER.md            # Founder profile and preferences
└── .github/
    └── workflows/         # CI/CD pipelines
```

## Operating Conventions

- **Commit everything.** No important state lives only in session memory.
- **Document decisions.** Non-trivial choices get an ADR in docs/adr/.
- **Skills over scripts.** Reusable procedures become Hermes skills. One-off scripts go in scripts/.
- **Cron over polling.** Recurring work uses Hermes cron jobs.
- **Verify, don't assume.** Subagent claims are verified before reporting to the founder.
- **Transparency in failure.** Error reports include: what was attempted, what happened, what was learned, what changes.

## Current State

- **Hardware:** Apple M1 Pro, 16 GB RAM, 460 GB SSD, macOS 14.8.7
- **Agent:** Hermes v0.19.0, DeepSeek v4 Pro (ollama-cloud), local Ollama available
- **Cloud:** None yet
- **GitHub:** Sergio-PB/aura-workspace (private)
- **Messaging:** CLI + Telegram

## Founder

Sergio — interacts daily via CLI or Telegram. Prefers async, summarized, actionable communication. Time is the scarcest resource.
