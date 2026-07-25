# Aura Design Template

> **Purpose:** Every piece of work at Aura — feature, architecture decision, design system, brand asset — follows this template. Prepare before building. Review before shipping. Commit the artifact.

---

## When to Use

| Work Type | Template Section | Persona Lead | Reviewer |
|-----------|-----------------|--------------|----------|
| New feature or product change | §1 PRD | PM (`aura-pm`) | Architect + UX |
| Architecture decision | §2 ADR | Architect (`aura-architect`) | PM + Senior Dev |
| UI/UX design or design system | §3 Design Spec | UX (`aura-ux`) | PM + Brand |
| Brand asset or guideline | §4 Brand Spec | Brand (`aura-brand`) | PM + UX |
| Code change (any size) | §5 Code Change | Developer | Architect + Reviewer |

---

## §1 — Product Requirements Document (PRD)

**Use when:** Building a new feature, changing existing behavior, or scoping a milestone from the roadmap.

**Lead:** `aura-pm` persona
**Reviewers:** `aura-architect` + `aura-ux`

### Template

```markdown
# PRD: [Feature / Initiative Name]

**Status:** Draft | In Review | Approved | In Development | Shipped
**Author:** [Name]  **Last Updated:** [Date]
**Roadmap Ref:** [e.g., P-3: The Farm — Core]

---

## 1. Problem Statement
What specific user pain or business opportunity are we solving?
Who experiences this, how often, and what is the cost of not solving it?

**Evidence:**
- User research: [findings, n=X]
- Behavioral data: [metric showing the problem]
- Support signal: [ticket volume / theme]

---

## 2. Goals & Success Metrics
| Goal | Metric | Current Baseline | Target |

---

## 3. Non-Goals
What this initiative will NOT address in this iteration.

---

## 4. User Stories
**As a** [persona], **I want to** [action] **so that** [outcome].

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [edge case], when [action], then [fallback behavior]

---

## 5. Solution Overview
[Narrative description — 2-4 paragraphs]
[Key UX flows, major interactions, core value delivered]

**Key Design Decisions:**
- [Decision]: We chose [A] over [B] because [reason]. Trade-off: [what we give up].

---

## 6. Technical Considerations
**Dependencies:** [System / team / API] — needed for [reason]
**Known Risks:** [Risk] — Likelihood: [H/M/L] — Impact: [H/M/L] — Mitigation: [plan]
**Open Questions:** [Question] — Owner: [name]

---

## 7. Launch Plan
| Phase | Audience | Success Gate |
|-------|----------|-------------|
| Internal alpha | Team + design partners | No P0 bugs, core flow complete |
| Closed beta | N opted-in users | <5% error rate |
| GA rollout | All users | Metrics on target |

**Rollback Criteria:** If [metric] drops below [threshold], revert and page on-call.
```

### Review Checklist
- [ ] Problem is stated with evidence, not assumptions
- [ ] Success metrics are specific and measurable
- [ ] Non-goals are explicit — we know what we're NOT building
- [ ] User stories have clear acceptance criteria
- [ ] Every design decision names its trade-off
- [ ] Dependencies and risks are identified with owners
- [ ] Launch plan includes rollback criteria

---

## §2 — Architecture Decision Record (ADR)

**Use when:** Making any non-trivial technical decision — tech stack, pattern choice, data model, API design, infrastructure.

**Lead:** `aura-architect` persona
**Reviewers:** `aura-pm` + developer

### Template

```markdown
# ADR-NNN: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Author:** [Name]
**Roadmap Ref:** [e.g., P-1: Architecture & Tech Stack]

---

## Context
What issue is motivating this decision? What constraints are we operating under?
What is the current state, and why is it insufficient?

---

## Decision
What change are we proposing? Be specific — name the technology, pattern, or approach.

---

## Options Considered
| Option | Pros | Cons | Effort | Risk |
|--------|------|------|--------|------|
| [Option A — chosen] | [pros] | [cons] | [S/M/L] | [H/M/L] |
| [Option B] | [pros] | [cons] | [S/M/L] | [H/M/L] |
| [Option C — do nothing] | [pros] | [cons] | — | [H/M/L] |

---

## Consequences
**What becomes easier:**
- [Positive outcome 1]
- [Positive outcome 2]

**What becomes harder:**
- [Negative outcome 1]
- [Negative outcome 2]

**Migration path:** [If applicable, how do we get from current state to new state?]
```

### Review Checklist
- [ ] Context explains WHY this decision is needed now
- [ ] At least two options are presented with trade-offs
- [ ] "Do nothing" is always one of the options
- [ ] Consequences cover both positive and negative outcomes
- [ ] Migration path is defined if this changes existing systems
- [ ] Decision is reversible or has a clear rollback path

---

## §3 — Design Spec

**Use when:** Creating UI/UX for any surface — The Farm app, The Card app, ifarm.club landing page, design system components.

**Lead:** `aura-ux` persona
**Reviewers:** `aura-pm` + `aura-brand`

### Template

```markdown
# Design Spec: [Component / Screen / System]

**Status:** Draft | In Review | Approved | Implemented
**Author:** [Name]  **Last Updated:** [Date]
**Roadmap Ref:** [e.g., P-3: The Farm — Core]

---

## 1. User Context
**Who sees this?** [Persona + context]
**What are they trying to do?** [Job to be done]
**What's the emotional state?** [e.g., focused, casual, urgent]

---

## 2. Layout & Structure
**Information Architecture:**
- Primary action: [what the user does first]
- Secondary actions: [what else they can do]
- Content hierarchy: [H1 → H2 → H3 structure]

**Responsive Behavior:**
| Breakpoint | Layout |
|------------|--------|
| Mobile (320px+) | [layout description] |
| Tablet (768px+) | [layout description] |
| Desktop (1024px+) | [layout description] |

---

## 3. Design System Tokens
**Colors used:** [list semantic color tokens]
**Typography:** [heading font, body font, sizes]
**Spacing:** [key spacing values]
**Interactive states:** [hover, focus, active, disabled, loading, error]

---

## 4. Accessibility
- [ ] All interactive elements are keyboard-navigable
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for text, 3:1 for large text)
- [ ] Focus indicators are visible
- [ ] Screen reader labels are defined
- [ ] Touch targets are ≥ 44px

---

## 5. Theme Support
- [ ] Light theme defined
- [ ] Dark theme defined
- [ ] System preference respected by default

---

## 6. Developer Handoff
**Files to create/modify:**
- `css/design-system.css` — [what tokens to add]
- `css/layout.css` — [what layouts to add]
- `css/components.css` — [what components to add]

**Implementation order:**
1. Foundation (CSS variables, tokens)
2. Layout (containers, grids)
3. Components (individual UI pieces)
4. Content (real data)
5. Polish (animations, micro-interactions)
```

### Review Checklist
- [ ] User context is clear — who, what, emotional state
- [ ] Responsive behavior is defined for all breakpoints
- [ ] Design tokens are semantic, not hardcoded
- [ ] Accessibility checklist is complete
- [ ] Light + dark themes are both defined
- [ ] Developer handoff includes exact file paths and implementation order

---

## §4 — Brand Spec

**Use when:** Creating or updating any brand asset — logo, color palette, typography, voice guidelines, marketing materials.

**Lead:** `aura-brand` persona
**Reviewers:** `aura-pm` + `aura-ux`

### Template

```markdown
# Brand Spec: [Asset / Guideline Name]

**Status:** Draft | In Review | Approved | Published
**Author:** [Name]  **Last Updated:** [Date]

---

## 1. Brand Context
**What brand element is this?** [Logo, color, voice, etc.]
**Why is this needed?** [Context — new brand, refresh, new platform]
**What brand attributes should this convey?** [3-5 adjectives]

---

## 2. The Asset
[Description, specifications, usage guidelines]

**For visual assets:**
- File formats: [SVG, PNG, etc.]
- Color variants: [full color, monochrome, reversed]
- Clear space: [minimum padding around asset]
- Minimum size: [smallest reproduction size]
- Incorrect usage: [examples of what NOT to do]

**For voice/tone assets:**
- Voice characteristics: [3-5 traits with descriptions]
- Tone variations: [professional, conversational, supportive — when to use each]
- Vocabulary: [preferred terms, terms to avoid]

---

## 3. Brand Consistency Check
- [ ] Aligns with Aura's brand purpose, vision, and values
- [ ] Works across all platforms (The Farm, The Card, ifarm.club, social media)
- [ ] Accessible (color contrast, readable typography, inclusive language)
- [ ] Culturally appropriate for target audiences

---

## 4. Implementation
**Where this asset lives:**
- Repo path: [e.g., `resources/brand/`]
- Design tool file: [Figma link or file path]
- Documentation: [where guidelines are published]
```

### Review Checklist
- [ ] Brand context is clear — what, why, what it conveys
- [ ] Usage guidelines include both correct and incorrect examples
- [ ] Consistency check covers all platforms
- [ ] Accessibility and cultural sensitivity are verified
- [ ] Asset files are committed to the repo

---

## §5 — Code Change

**Use when:** Any code change — feature implementation, bug fix, refactor, dependency update.

**Lead:** Developer
**Reviewers:** `aura-architect` (architecture) + Code Reviewer (correctness)

### Template

```markdown
# Code Change: [Brief Description]

**Status:** Draft | In Review | Approved | Merged
**Author:** [Name]  **Date:** [YYYY-MM-DD]
**PR:** [link]
**Roadmap Ref:** [e.g., P-3: The Farm — Core]

---

## 1. What & Why
**What does this change do?** [One sentence]
**Why is it needed?** [Problem it solves or feature it enables]

---

## 2. Scope
**Files changed:**
- `path/to/file.ts` — [what changed and why]
- `path/to/other.ts` — [what changed and why]

**What's NOT changed:** [Explicitly call out things that might be expected but aren't included]

---

## 3. Testing
**How was this tested?**
- [ ] Unit tests: [which paths are covered]
- [ ] Integration tests: [which flows are covered]
- [ ] Manual testing: [what was manually verified]

**How to verify:**
```bash
# Commands to run to verify this change
```

---

## 4. Risks & Rollback
**What could go wrong?** [Risk — Likelihood — Mitigation]
**How to roll back:** [Steps to revert if this breaks something]

---

## 5. ADR Reference
[Link to relevant ADR if this implements an architecture decision]
```

### Review Checklist
- [ ] What & Why is clear in one sentence
- [ ] Scope includes what's NOT changed
- [ ] Tests cover the important paths
- [ ] Rollback plan exists
- [ ] Relevant ADR is referenced
- [ ] Code follows existing patterns in the codebase
- [ ] No new dependencies without ADR justification
- [ ] No dead code, commented-out code, or TODO markers without issue references

---

## Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PREPARE    │ ──→ │    REVIEW    │ ──→ │    BUILD     │ ──→ │    SHIP      │
│              │     │              │     │              │     │              │
│ Write the    │     │ Persona lead │     │ Implement    │     │ Merge, deploy │
│ appropriate  │     │ reviews for  │     │ per spec     │     │ Verify metrics│
│ template     │     │ their domain │     │ Write tests  │     │ Post-launch   │
│              │     │              │     │              │     │ review        │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

**Prepare:** The appropriate persona lead (PM, Architect, UX, Brand) fills out the template. The artifact is committed to the repo.

**Review:** The designated reviewers check the artifact against the review checklist. They approve, request changes, or reject. Review happens in the repo (PR comments or direct commits).

**Build:** Development proceeds against the approved spec. If the spec needs to change during build, the artifact is updated and re-reviewed.

**Ship:** Code is merged, deployed, and verified against the success metrics defined in the spec. A post-launch review updates the artifact with what was learned.

---

## Artifact Storage

All design artifacts live in the repo alongside the code they describe:

```
aura-workspace/
├── docs/
│   ├── adr/           # Architecture Decision Records
│   ├── prd/           # Product Requirements Documents
│   ├── design/        # Design specs (UI/UX)
│   └── brand/         # Brand specs
├── resources/
│   ├── design/        # Design assets (Figma exports, images)
│   ├── brand/         # Brand assets (logos, fonts, palettes)
│   └── legal/         # Legal documents
└── apps/              # (in aura-apps repo)
    ├── farm/
    └── card/
```

---

## Principles

1. **Write before you build.** No code without a spec. No spec without a review.
2. **Commit the artifact.** Specs are code. They live in the repo, get versioned, and are reviewed like code.
3. **Name the trade-off.** Every decision document must state what we're giving up.
4. **Review with the checklist.** Don't free-form reviews. Use the checklist. If the checklist is wrong, fix the checklist.
5. **Update after shipping.** The artifact is living documentation. Post-launch, add what was learned.
