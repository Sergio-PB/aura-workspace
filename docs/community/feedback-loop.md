# Aura — Feedback Collection & Iteration Loop

> **Status:** Draft v1
> **Author:** Aura Agent
> **Audience:** Product team, community moderators
> **Purpose:** Define how Aura collects, prioritizes, and acts on user feedback during public beta (N-2) and beyond.

---

## Principles

1. **Low friction to submit.** If it takes more than 30 seconds, people won't do it.
2. **Close the loop.** Every submission gets a response — even if it's "not now, here's why."
3. **Public backlog.** What's being worked on and why is visible to the community.
4. **Feedback informs, doesn't dictate.** Community input shapes priorities, but the product vision leads.

---

## Collection Channels

### In-App (Primary)

| Channel | Where | Format | Use Case |
|---------|-------|--------|----------|
| **Quick reaction** | Feed items, attributions | 👍/👎 + optional text | Micro-feedback on specific features |
| **Bug report** | Settings → Report Bug | Structured form (what happened, what you expected, steps) | Defects |
| **Feature request** | Settings → Suggest Feature | Free text + category tag | Ideas |
| **NPS survey** | Periodic in-app prompt | 0-10 score + "why?" | Satisfaction baseline |
| **Exit feedback** | Account deletion flow | "What made you leave?" (optional) | Churn reasons |

### Community (Secondary)

| Channel | Where | Format | Use Case |
|---------|-------|--------|----------|
| **GitHub Issues** | `aura-apps` repo (public) | Issue template (bug/feature) | Technical users, transparency |
| **Discord/Telegram** | Community chat | Free-form discussion | Real-time conversation, vibe checks |
| **Moderator reports** | Moderation dashboard | Aggregated themes | Patterns moderators notice |

### Structured (Periodic)

| Method | Cadence | Audience | Purpose |
|--------|--------|----------|---------|
| **User interview** | Monthly, 3-5 users | Mix of power users and new users | Deep qualitative insight |
| **Event debrief** | After each community event | Event attendees | What worked, what didn't at real gatherings |
| **Feature vote** | Quarterly | All users | Prioritize the backlog |

---

## Triage & Prioritization

Every piece of feedback lands in a single triage board with four buckets:

| Bucket | Criteria | Response Time | Action |
|--------|----------|---------------|--------|
| **Critical** | Data loss, security, privacy breach, service down | < 4 hours | Fix immediately, postmortem after |
| **High** | Core flow broken, significant UX friction, repeated reports | < 1 week | Schedule next sprint |
| **Medium** | Nice-to-have improvement, edge case, single report | < 2 weeks | Add to backlog, vote-enabled |
| **Low** | Cosmetic, "someday," out of scope | < 2 weeks | Respond with rationale, close |

### Prioritization Formula

```
Priority Score = (User Impact × Frequency) + Strategic Alignment
```

- **User Impact (1-5):** How many users does this affect, and how badly?
- **Frequency (1-5):** How many reports? Is it growing?
- **Strategic Alignment (1-5):** Does this advance the core mission (fair community, real-world reputation)?

Tiebreaker: effort estimate. Two equal-priority items → do the faster one first.

---

## The Feedback Loop (Closing It)

Every submission follows this lifecycle:

```
Submitted → Acknowledged (auto) → Triaged → Responded → (Implemented / Declined) → Notified
```

### Auto-Acknowledgment

On submission, user sees: "Thanks! We read every piece of feedback. You'll hear back within [timeframe]."

### Triage Response

Human (or agent) reviews, categorizes, and responds with:
- What we understood
- What bucket it landed in
- What happens next (and when)

### Implementation Notification

When a feature ships or a bug is fixed that came from feedback:
- In-app notification: "You asked for [X]. It's live. [link]"
- Public changelog entry credits the reporter(s) by name (with permission)

### Declined Notification

When feedback is declined:
- Clear reason why (not "we decided not to")
- What alternative exists (if any)
- Invitation to discuss further

---

## Public Backlog

A public-facing roadmap/backlog at `ifarm.club/roadmap` shows:

- **Now:** What's being built this cycle
- **Next:** What's queued up
- **Later:** What's under consideration
- **Shipped:** What just landed

Each item links to the feedback that inspired it. This closes the loop publicly and builds trust.

---

## Metrics

Track these to know if the loop is working:

| Metric | Target | Why |
|--------|--------|-----|
| Feedback submission rate | > 5% of active users/month | People know the channel exists and use it |
| Time-to-first-response | < 48 hours for non-critical | Respect for people's time |
| Loop closure rate | > 80% of submissions get a resolution response | We don't ghost people |
| Feature-from-feedback rate | > 30% of shipped features trace to user feedback | We're building what people need |
| NPS | > 40 (public beta), trending up | Satisfaction is improving |

---

## Tooling

### Phase 1: Manual (N-2 start)

- GitHub Issues for public backlog
- Shared spreadsheet for triage tracking
- Manual responses via in-app notification or email
- Agent (Aura Agent) handles triage and response drafting

### Phase 2: Lightweight Tooling (N-2 mature)

- Simple feedback dashboard (could be a Card feature — "Aura Feedback" as a special feed)
- Auto-tagging by category
- Duplicate detection (similar reports grouped)
- Public roadmap page (static site, updated with each release)

### Phase 3: Integrated (post N-2)

- In-app feedback widget with screenshot annotation
- Session replay for bug reports (opt-in, privacy-respecting)
- Automated prioritization scoring
- Community voting on feature requests

---

## Bootstrap Notes (N-2 Phase)

During public beta:
- Aura Agent handles all triage and response drafting
- Founder reviews and approves responses before they go out
- GitHub Issues is the single source of truth for the backlog
- Monthly "what we heard" summary posted to the community
- Bias toward responding fast over responding perfectly

---

*Last updated: 2026-07-29*
