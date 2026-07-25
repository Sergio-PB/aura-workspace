# Aura — Stack Specification

> **Status:** Draft
> **Last updated:** 2026-07-25

---

## Language

**TypeScript** — all software across The Farm, The Card, backend, and shared packages.

<new fact>All software is written in TypeScript.</new fact>

---

## Package Manager

**pnpm** — fast, disk-efficient, strict dependency resolution.

<new fact>pnpm is the package manager for all projects.</new fact>

---

## E2E Testing

**Playwright** — mature, cross-browser, natural-language test scenarios.

- Tests described as user journeys: `test('user records a seesaw move and claims aura points', ...)`
- Cross-browser (Chromium, Firefox, WebKit)
- Built-in assertions, screenshots, traces, video recording
- CI-native with GitHub Actions integration

<new fact>E2E testing uses Playwright with natural-language scenario descriptions.</new fact>

---

## Monorepo

```
aura-apps/
├── pnpm-workspace.yaml
├── package.json              # root
├── apps/
│   ├── farm/                 # The Farm
│   └── card/                 # The Card
├── packages/
│   └── shared/               # shared types, utils, API client
└── e2e/                      # Playwright tests
    └── scenarios/
        ├── record-move.spec.ts
        └── claim-points.spec.ts
```

<new fact>Monorepo uses pnpm workspaces.</new fact>
<new fact>E2E tests live in a top-level e2e/ directory with scenario-based specs.</new fact>

---

## Open Decisions

| Decision | Status |
|----------|--------|
| Frontend framework (Farm + Card) | TBD |
| Backend runtime/framework | TBD |
| Database | TBD |
| Visual computing library (face/hand tracking) | TBD — open source, specific choice later |
| Move library format/storage | TBD |
