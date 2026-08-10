# Recording Analysis — Farm Analyze Mode

- **Status:** Draft (post-brainstorm, pre-plan)
- **Date:** 2026-08-10
- **Owner:** Farm app — `apps/farm-capacitor/`
- **Initiative track:** P (Product) — extends P-14 ("Video Farming", already shipped)
- **Repo split:** Spec lives in `aura-workspace/docs/`. Code lands in `aura-apps/apps/farm-capacitor/`. Cypress lives in `aura-apps/apps/farm-capacitor/cypress/`.

---

## 1. Problem

The Farm has two modes for farming aura points:

- **Live** — camera → MediaPipe WASM → particles + game logic.
- **File** — drop a recorded video into the page → MediaPipe WASM replay → ✅ Validate shows the detected move sequence.

Per Sergio:

> Right now we have two modes of farming points. Live, which streams the camera image and does calculations in runtime. File which allows the user to pick a file and analyze it. At the moment, it is broken though.

Verification of the broken behavior: "I can't playback the video I uploaded and clicking on Validate shows an empty list."

The three capabilities needed on top of fixing this:

1. **Automation** — Cypress end-to-end coverage of the file-mode pipeline. The single biggest concern; without it, every tracking-algorithm change is a hand-test.
2. **Manual analysis & tuning** — when Analyze is clicked, the analyzed movements are **overlaid on the video**, so the user can see exactly frame-by-frame where the hands were, what the bounding box looked like, where the move trail led.
3. **A/B testing (later)** — different `.yaml` tuning configs run against the same set of webvm recordings; diff produces KPIs. Comparison lives in CI first; a browser compare UI is a later layer.

The goal is confidence when changing the tracking algorithm reliably against a set of webvm recordings (expectations).

---

## 2. Approach (chosen)

**A. Pure browser, MediaPipe-in-Cypress, with tolerance-based assertions.**

The tracking engine stays in `useMediaPipe` (already correct). Cypress drives the existing UI: load fixture → click play → wait for the trace to be ready → assert the trace JSON. No Node engine port, no separate headless harness.

Why this and not the alternatives:

|| Criterion | A (chosen) | B (Node engine port) | C (headless harness) |
||---|---|---|---|
|| Determinism | tolerance (~±N frames) | exact | medium |
|| Engine count | 1 | 2 (drift risk) | 1.5 (shared but separate harness) |
|| Automation cost | low (Cypress clicks) | medium (separate test env) | high (Playwright inside Cypress) |
|| Spec coverage | matches shipped UX | matches a port | matches shipped UX |

MediaPipe WASM is non-deterministic per-frame on the same input — that's an inherent property, not a Cypress limitation. Tolerance assertions (move spans present, in roughly the right window) are the correct shape for a vision pipeline. Exact-frame equality would be coincidental.

---

## 3. Architecture

```
apps/farm-capacitor/src/
├── screens/RecordScreen.tsx                  (extended — analyze state + layer-toggles panel)
├── analyze/                                  (NEW MODULE)
│   ├── types.ts                              FrameTrace, Trace
│   ├── traceIO.ts                            Trace ⇄ JSON + window.__AURA_TRACE__
│   └── analyze.test.ts                       stub-based self-check (matches audio.test.ts style)
└── hooks/
    └── useMediaPipe.ts                       (UNCHANGED)

apps/farm-capacitor/cypress/
├── e2e/analyze/
│   ├── smoke.cy.ts                           boots Farm, waits for MediaPipe ready
│   └── {seesaw,wave,clap,raise-roof,point}.cy.ts
├── fixtures/recordings/{seesaw,wave,clap,raise-roof,point}.webm   committed binary
├── support/
│   ├── commands.ts                           cy.loadFixture(name), cy.getAuraTrace()
│   └── assert.ts                             tolerant span-match helpers
└── cypress.config.ts                         cypress/vite dev server, HTTPS, headless

scripts/
└── build-fixtures.sh                         record + normalize 5 fixture webms (run once)
```

**One engine, three flows:**

| Flow | Surface | Driver | Output |
|---|---|---|---|
| Live (unchanged) | camera | existing RAF pump | particles + game + live websocket |
| File → Validate (unchanged) | file | existing RAF pump | ValidationSummary JSON (the buggy path we're fixing) |
| File → Analyze (NEW) | file | existing RAF pump, with `analyze = on` accumulating frames | Trace JSON + paint layers (raw + per-move trails) drawn live over the video |

**Bug hypothesis (requires verification before fix):**

1. The file-mode RAF pump in `useMediaPipe` (lines 235-245 of `useMediaPipe.ts`) gates on `!video.paused && !video.ended && video.readyState >= 2`. If the browser silently fails to play a video (unsupported codec, missing permission in iOS, etc.), `paused` stays true and no frames are sent.
2. The Validate button's empty list is then a downstream symptom — `moveLogRef` is populated by the tick loop only when `source === "file"` AND `s.move !== prevMove`, which never fires because MediaPipe gets no frames.

**First implementation step (regardless of spec approval):** stand up the analyze pipeline + 5 Cypress tests against the existing file mode. The fix to the playback bug is whatever the Cypress tests reveal — if the tests pass against the current RAF pump, the bug is somewhere else; if they fail with `incomplete: "timeout"`, the root cause is the pump gating. Document the finding either way.

**The Analyze mode is a side-effect of the existing tick loop.** When `analyze = on`, every MediaPipe `onResults` callback (which already runs per frame) appends to a Trace array in addition to the existing `moveLogRef` push. When `analyze = off` (default), the RAF pump behaves exactly as today. Analysis re-runs whenever the user presses Analyze again with `analyze = on`; the resulting Trace JSON is downloadable as an artifact.

**No changes inside `useMediaPipe`.** The hook already emits `onResults` per frame. RecordScreen subscribes a Trace-accumulator when analyze is on. Camera mode is unaffected.

---

## 4. Data shapes

```ts
// analyze/types.ts

type NormalizedLandmark = { x: number; y: number; z: number };  // 0..1, matches MediaPipe shape

interface FrameTrace {
  tMs: number;                       // floor(video.currentTime * 1000)
  landmarks: { left: NormalizedLandmark[] | null; right: NormalizedLandmark[] | null };
  gesture: "open" | "fist" | "point" | "peace" | "thumbs_up" | "unknown";
  confidence: number;                // [0..1]
  move: "seesaw" | "wave" | "clap" | "raise_roof" | "point" | null;
  moveRate: number;                  // [0..1]
}

interface Trace {
  filename: string;
  sourceWidth: number;               // video.videoWidth at run start
  sourceHeight: number;
  totalFrames: number;               // captured frames
  requestedFrames: number;           // floor(durationMs * fps / 1000)
  durationMs: number;
  fps: number;                       // observed pump rate (Hz)
  incomplete: false | "partial" | "timeout" | "decode";
  config: TuningConfig;              // snapshot — A/B lever
  frames: FrameTrace[];
  summary: ValidationSummary;        // existing buildSummary() output, derived
}
```

**Why ship landmarks, not just move logs.** The move log throws away the spatial signal. Cypress needs to assert "the seesaw window contains hand-landmark x-positions oscillating between two x-bands" — that's a landmarks assertion, not a string comparison. Landmarks are also what the overlay canvas must consume.

**Why a config snapshot per trace.** The same fixture + two different `TuningConfig` values produces two traces. Diff them in CI to characterize any tuning change. No fixture-replay server needed; we just run Analyze twice with the panel flipped between runs.

---

## 5. UX

**Playback is unchanged.** The existing file-mode controls bar (▶/⏸ + slider + speed + ✅ Validate + 📁 Choose + 📷 switch-to-camera) stays as-is. The video plays normally; the user pauses, scrubs, speed-changes, switches back to camera — all the same.

**Two additions to the bar:**

- **[🔬 Analyze]** — toggle. When on, MediaPipe frames accumulate into the Trace every time `onResults` fires. When off (default), the Trace stays empty. No waiting, no mode-switch, no special playback.
- **Layer toggles** — a small panel above the bar, visible only when `Analyze = on AND Trace.frames.length > 0`. Three checkboxes, all defaulting OFF until Analyze runs:
  - [ ] **Raw landmarks** — 21 dots per visible hand, MediaPipe stick-figure connections (cyan).
  - [ ] **Seesaw trail** — polyline of wrist positions while move === `"seesaw"` (gold).
  - [ ] **Other-move trails** — one checkbox + color per detected move (cyan wave / magenta clap / green raise_roof / orange point). The user said "XYZ-movement trail" — these are stable, one per move type, config-driven not hand-painted.

**Painting happens at runtime** during natural playback. No pre-stepped frames. Each frame: read `Trace.frames[i]` where `i` indexes into the trace array by `tMs ≈ video.currentTime*1000`. The Trace is read-only from the canvas's perspective — playback drives `i`, paint reads `frames[i]`.

**Analyze button interaction.** Click → toggle on → Trace starts filling. Click again → toggle off → Trace is frozen and the layer toggles stay visible (cached trace). Click once more → toggle on again → Trace resets and starts filling anew.

**A separate overlay canvas, sibling to `ParticleOverlay`.** Particles continue animating live (existing path); the overlay canvas paints raw landmarks + per-move trails on top, gated by the toggles. Both render under the file-mode controls bar.

---

## 6. Error states

| Failure | UI signal | Cypress signal |
|---|---|---|
| File won't decode (codec/format) | red banner "Could not load video. Try MP4/WebM." | `window.__AURA_TRACE__ = { error: "decode" }` |
| MediaPipe throws during pump | skip frame, log `[aura analyze] frame N failed: <err>`; trace `incomplete: "partial"` (frames array short of requested) | trace.frames[i] missing; Cypress uses span-presence on what exists |
| Pump stalled (0 frames after 30s wall) | "Analysis stuck. Try a shorter clip or refresh." | `incomplete: "timeout"` |
| User clicks Analyze twice (off→on while filling) | new push resets Trace; old frames are wiped | — |
| File mode but no MediaPipe (network blocked CDN) | bubbled up from `useMediaPipe` `[mediapipe]` error | trace.frames empty + `incomplete: "timeout"` |

Errors never fail silently. Cypress does NOT silently pass — a `timeout` trace fails the test with a clear message naming the failure mode.

---

## 7. Testing

**Unit-style self-check (`npx tsx src/analyze/analyze.test.ts`).**

- `toTraceJSON` round-trip (Trace → JSON → Trace equals)
- Layer-index helper — `(frames, tMs) => frameIndex` correctness on edge cases (frame before, frame after, exact match)

Pattern matches `src/audio/sound.test.ts` (project convention). No Vitest. `package.json` script: `"test:analyze": "tsx src/analyze/analyze.test.ts"`.

**Cypress end-to-end.** One spec per fixture; spec flow: load fixture, click ▶, click 🔬 Analyze, wait for `Trace.frames.length > N`, assert via tolerant span-match.

**Tolerance-based assertions.** MediaPipe is non-deterministic frame-to-frame. The assertion shape is span-presence:

```ts
cy.getAuraTrace().then((trace) => {
  assertMoveSpan(trace, "seesaw", { minStartMs: 200, maxStartMs: 1500, minDurationMs: 300 });
});
```

Strict tMs equality is a known ceiling — the upgrade path is to swap MediaPipe for a deterministic detector on the CI side. We don't go there now (YAGNI).

**Fixtures.** Five `.webm` recordings at 320×240 @ ~30fps × 4s, total ~500KB committed binary. Built once via `scripts/build-fixtures.sh`. No `.json` expectation files — type-checks against the Trace shape, that's enough.

**CI integration.** Add `cypress run --browser chrome` to `.github/workflows/`. Cypress job uploads screenshots + traces on failure.

---

## 8. Migration / rollout

1. Ship the analyze pipeline + 5 Cypress tests behind a `?analyze` URL flag (default off).
2. Wire Cypress into CI once green locally; flip default to on.
