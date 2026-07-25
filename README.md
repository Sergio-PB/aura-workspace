# Aura Workspace

Aura builds a fair community based on social scores. Two products:

- **The Farm** — a local media studio that streams telemetry (IP, geolocation, face recognition) from camera or local media files. Users upload "aura points" to themselves or others by recording and reacting to real-world moments.
- **The Card** — an identification beacon that uniquely identifies users and their IPs, letting them claim points attributed by a Farm. Surfaces as a social feed with quick reactions.

The backend validates and attributes aura by triangulating and correlating input, and/or by community consensus. Others at the same event can confirm or challenge point attribution.

## Workspace

This repository is the company brain for Aura. Product code lives in the [aura-apps](https://github.com/Sergio-PB/aura-apps) monorepo. This repo contains:

- `docs/` — architecture, ADRs, company culture
- `scripts/` — one-off automation scripts
- `skills/` — custom Hermes Agent skills
- `memories/` — persistent agent memories exported from Hermes
- `.github/` — CI/CD workflows

## Repos

| Repo | Purpose |
|------|---------|
| [aura-workspace](https://github.com/Sergio-PB/aura-workspace) | Company brain: docs, ADRs, culture, memories, scripts |
| [aura-apps](https://github.com/Sergio-PB/aura-apps) | Monorepo: The Farm + The Card source code |

## Operator

Aura is operated autonomously by Aura Agent (Hermes Agent with a custom persona). The agent runs the startup — coding, monitoring, documenting, and improving itself. All agent work is committed here.

**Transparency is the number one pillar.**
