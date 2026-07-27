# Aura Moderation & Dispute Resolution

> **Status:** Draft v1
> **Author:** Aura Agent
> **Audience:** Moderators, community members

This document defines how Aura handles violations, disputes, and moderation decisions. It exists so every action is transparent, consistent, and appealable.

---

## Moderation Roles

| Role | Who | Authority |
|------|-----|-----------|
| **Founding Moderator** | Sergio (founder) | Full moderation authority during bootstrap phase |
| **Community Moderator** | Trusted members, appointed by consensus | Review reports, issue warnings, escalate to founding moderator |
| **Validator** | Any community member at an event | Confirm or challenge individual attributions |

During N-1 (founding community), the founding moderator handles all moderation. Community moderators are added as the community grows (N-2).

---

## Report Flow

```
Report submitted → Moderator reviews → Decision → Action → Appeal (if requested)
```

### 1. Report Submission

Anyone can report a violation through:
- In-app report button (on attributions, profiles, or events)
- Direct message to a moderator
- Email to moderation@ifarm.club (once domain email is set up)

Reports must include:
- What happened (specific attribution, event, or behavior)
- When it happened
- Who was involved
- Any evidence (screenshots, recordings, witness names)

Anonymous reports are accepted but carry less weight — named reports allow follow-up.

### 2. Initial Review

A moderator reviews the report within 24 hours. They assess:
- Does this violate the [community guidelines](guidelines.md)?
- Is there sufficient evidence to act?
- What's the severity?

If the report is clearly frivolous or mistaken, it's closed with a note. Otherwise, it proceeds to investigation.

### 3. Investigation

The moderator:
- Reviews the reported content and any attached evidence
- Checks telemetry data if relevant (location, time, device proximity)
- Contacts involved parties for their side
- Reviews the reporter's and reported user's history for patterns

Investigation should be completed within 72 hours. If it takes longer, both parties are notified.

### 4. Decision

The moderator decides based on:
- **Evidence:** What actually happened, supported by data
- **Guidelines:** Does it violate a specific guideline?
- **Intent:** Was this deliberate or a mistake?
- **History:** First offense or pattern?
- **Impact:** How much harm did it cause?

Decisions are documented with:
- What was found
- Which guideline was violated (or why it wasn't)
- What action is taken
- How to appeal

### 5. Action

Actions scale with severity:

| Level | Action | Example |
|-------|--------|---------|
| 0 | Dismissed | Report was mistaken or doesn't violate guidelines |
| 1 | Warning | First minor offense, educational |
| 2 | Point reversal | Fraudulent points removed, no further penalty |
| 3 | Temporary restriction (7 days) | Repeated minor offenses or moderate violation |
| 4 | Temporary restriction (30 days) | Serious violation or pattern of moderate violations |
| 5 | Account suspension | Severe violation, pending review |
| 6 | Permanent ban | Deliberate harm, no path to return |

### 6. Appeal

Any action at level 2 or above can be appealed within 14 days. Appeals go to a different moderator than the one who made the original decision. During bootstrap (N-1), the founding moderator handles appeals directly.

Appeal process:
1. Submit appeal with reasoning and any new evidence
2. Second moderator reviews independently
3. Decision is final (no further appeals unless new evidence emerges)

---

## Attribution Disputes

Attribution disputes are the most common moderation case. Here's the specific flow:

### Challenge Flow

1. **User challenges an attribution** — "I was at this event and this didn't happen" or "This person wasn't there"
2. **System checks telemetry** — were both users at the same location and time?
3. **If telemetry conflicts** — attribution is flagged for review
4. **If telemetry aligns** — challenge is noted but attribution stands unless more challengers join
5. **Consensus threshold** — if enough event participants challenge (configurable, default: 3 or 30% of attendees, whichever is lower), attribution is reversed

### False Challenge Penalty

Challenging attributions you know are valid is itself a violation. Pattern of false challenges → level 1-3 action.

---

## Transparency Reports

Every quarter, Aura publishes a transparency report:
- Number of reports received
- Number of actions taken, by level
- Number of appeals and their outcomes
- Trends and patterns (without identifying individuals)

This keeps the community informed and the moderation team accountable.

---

## Moderator Accountability

Moderators are community members first. They:
- Are subject to the same guidelines as everyone else
- Can be reported like any other user
- Have their moderation decisions reviewed periodically
- Can be removed by community consensus if they abuse their role

---

## Emergency Actions

In cases of immediate harm (doxxing, credible threats, illegal content):
- Any moderator can suspend an account immediately
- Full review happens within 24 hours
- If the emergency action was unjustified, it's reversed and the moderator explains their reasoning publicly

---

## Bootstrap Notes (N-1 Phase)

During the founding community phase:
- Sergio is the sole moderator
- Decisions are made quickly, with a bias toward education over punishment
- Every moderation action is documented as a precedent for future cases
- Community feedback on moderation is actively solicited
- These processes will be refined based on real experience before N-2 (public beta)

---

*Last updated: 2026-07-27*
