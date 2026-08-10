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

Decisions recorded on user silence (no objection assumed, can flip):

- **Playback model:** run-once + scrubber (vs. "play clip and overlay in sync"). Run-once avoids the race where CI is slower than the actual video — overlay frames are stamped against `video.currentTime`, not wall clock.
- **A/B comparison location:** **CI-only** at first; browser-compare UI is a future milestone. Sergio's #1 priority is automation, and A/B was framed as "later in the future".

---

## 3. Architecture

```
apps/farm-capacitor/src/
├── screens/RecordScreen.tsx                  (extended — analyze state machine + scrubber;
│                                                also hosts the `useAnalyzeRun` driver)
├── analyze/                                  (NEW MODULE)
│   ├── types.ts                              FrameTrace, Trace
│   ├── runOnce.ts                            file → Trace (deterministic driver)
│   ├── overlayDraw.ts                        FrameTrace + canvas → draw calls
│   ├── kpis.ts                               Trace → per-move stats (counts, durations)
│   ├── traceIO.ts                            Trace ⇄ JSON + window.__AURA_TRACE__
│   └── analyze.test.ts                       stub-based self-check (matches audio.test.ts style)
├── components/
│   ├── AnalyzeOverlay.tsx                    (NEW — sibling canvas to ParticleOverlay)
│   └── AnalyzeScrubber.tsx                   (NEW — slider + transport)
└── hooks/
    └── useMediaPipe.ts                       (UNCHANGED core + one new export:
                                              a `sendOnce(video)` stepper that
                                              bypasses the RAF pump when called from
                                              analyze mode — does NOT change camera/file behavior)

apps/farm-capacitor/cypress/
├── e2e/analyze/
│   ├── smoke.cy.ts                           boots Farm, waits for MediaPipe ready
│   ├── seesaw.cy.ts                          one fixture per move (5 total)
│   ├── wave.cy.ts
│   ├── clap.cy.ts
│   ├── raise-roof.cy.ts
│   └── point.cy.ts
├── fixtures/
│   ├── recordings/{seesaw,wave,clap,raise-roof,point}.webm   committed, ~50–150KB each
│   └── expectations/{seesaw,wave,clap,raise-roof,point}.json  expected TraceSummary
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
| File → Analyze (NEW) | file | `useAnalyzeRun` stepper (NEW) | Trace JSON + canvas overlay + scrubber |

**Bug hypothesis (requires verification before fix):**

1. The file-mode RAF pump in `useMediaPipe` (lines 235-245 of `useMediaPipe.ts`) gates on `!video.paused && !video.ended && video.readyState >= 2`. If the browser silently fails to play a video (unsupported codec, missing permission in iOS, etc.), `paused` stays true and no frames are sent.
2. The Validate button's empty list is then a downstream symptom — `moveLogRef` is populated by the tick loop only when `source === "file"` AND `s.move !== prevMove`, which never fires because MediaPipe gets no frames.

**First implementation step (regardless of spec approval):** stand up the analyze pipeline + 5 Cypress tests against the existing file mode. The fix to the playback bug is whatever the Cypress tests reveal — if the tests pass against the current RAF pump, the bug is somewhere else; if they fail with `incomplete: "timeout"`, the root cause is the pump gating. Document the finding either way.

**The Analyze mode adds an additional driver on top.** It pauses, then for each frame index N: `video.currentTime = N / fps`, wait for `requestVideoFrameCallback` (or a RAF-fallback polled 5x), call `hands.send({ image: video })`, await the next `onResults`, append `{ tMs, landmarks, gesture, move, moveRate }` to `frames`. When all frames are captured, swap transport to scrubber.

Note: the analyze driver **replaces** the file-mode RAF pump while running. Once analyze completes, scrubbing is driven by `requestVideoFrameCallback` (decoded-frame ticks), not by MediaPipe — scrubbing does not re-run hand tracking per frame. If a user wants per-scrub-frame re-detection, that's a future enhancement, not in MVP.

**Why no changes inside `useMediaPipe` core.** It already exposes the right hooks (an `onResults` callback that fires per-frame, a `source: "file"` mode with a RAF pump). We add one escape hatch: a function `sendFrameOnce(videoEl)` exported from the hook ONLY when `source === "file"`. This calls `hands.send({ image: videoEl })` and is gated by the caller (not by the RAF pump racing with the analyze stepper). Camera mode is unaffected.

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

**File-mode controls bar (existing).** Pressing the existing ▶/⏸ button is always natural video playback. The ✅ Validate button keeps working and is unchanged.

**Analyze button (new, in the file-mode controls bar, next to Validate):**

```
┌── file mode controls bar ───────────────────────────────────────────┐
│ [⏪ -1f] [▶ / ⏸ Play trace] [⏩ +1f]   ──◯───  1.20s / 4.00s       │
│ [🔬 Analyze]   ← only enabled in "natural" file mode                │
│ [💾 Copy Trace] [💾 Download Trace]    ← visible in scrub mode      │
│ Layers: [✓ Raw landmarks] [✓ Move trail] [○ Particles]   Speed 1x    │
└────────────────────────────────────────────────────────────────────┘
```

Pressing 🔬 Analyze:

1. Pauses natural playback (via `video.pause()`).
2. Swaps transport to scrubber.
3. Runs the deterministic stepper; while running, the button shows `🔬 Analyzing...` (disabled).
4. On completion, scrubber becomes interactive, overlay renders frame 0, control bar shows the copy/download buttons.

Re-pressing Analyze from scrub mode re-runs and replaces the trace. Validate JSON is independently available via the existing ✅ button (it consumes the same `moveLogRef`).

**Overlay canvas (sibling to `ParticleOverlay` canvas).**

- **Raw landmarks layer** — 21 dots per visible hand, MediaPipe stick-figure connections (cyan). Border becomes lime if `gesture !== 'unknown'`. Confidence shown above the bounding box.
- **Move trail layer** — per move, a polyline of the last N wrist positions (gold seesaw / cyan wave / magenta clap / green raise_roof / orange point). Cleared on move change.
- **Particles layer** — toggleable; OFF by default in analyze mode (keeps the overlay readable).

Default layers: Raw + Move trail ON, Particles OFF.

**Why a separate canvas.** `ParticleOverlay` is its own RAF loop with internal state. Sharing a canvas with a different draw API would tangle two renderers. Ponytail rungs 2 (existing patterns) and 4 (don't add a new dep): a sibling canvas is ~80 LOC, zero coupling.

---

## 6. Error states

| Failure | UI signal | Cypress signal |
|---|---|---|
| File won't decode (codec/format) | red banner "Could not load video. Try MP4/WebM." | `window.__AURA_TRACE__ = { error: "decode" }` |
| MediaPipe throws during pump | skip frame, log `[aura analyze] frame N failed: <err>`; trace `incomplete: "partial"` (frames array short of requested) | trace.frames[i] missing; Cypress uses span-presence on what exists |
| Pump stalled (0 frames after 30s wall) | "Analysis stuck. Try a shorter clip or refresh." | `incomplete: "timeout"` |
| User clicks Analyze twice | second click is no-op while `analyzeMode === "play-once"` | — |
| File mode but no MediaPipe (network blocked CDN) | bubbled up from `useMediaPipe` `[mediapipe]` error | trace.frames empty + `incomplete: "timeout"` |

Errors never fail silently. Cypress does NOT silently pass — a `timeout` trace fails the test with a clear message naming the failure mode.

---

## 7. Testing

**Unit-style self-check (`npx tsx src/analyze/analyze.test.ts`).**

- `buildSummary` correctness (1 happy + 2 edge cases)
- `toTraceJSON` round-trip (Trace → JSON → Trace equals)
- `kpis` per-move counts (5 fixtures worth of synthetic frames)
- `overlayDraw` draw-call counts per visible layer (stub canvas)

Pattern matches `src/audio/sound.test.ts` (project convention). No Vitest. `package.json` script: `"test:analyze": "tsx src/analyze/analyze.test.ts"`.

**Cypress end-to-end.**

```
cypress/
├── cypress.config.ts                 vite dev server + HTTPS, headless, video off
├── e2e/analyze/smoke.cy.ts           boots Farm, clicks 🔬 Analyze on a synthetic clip,
│                                     waits for window.__AURA_TRACE__, asserts summary
├── e2e/analyze/{seesaw,wave,clap,raise-roof,point}.cy.ts
│                                     one per move — load fixture, run analyze, assert
│                                     expected summary span
├── support/commands.ts               cy.loadFixture(name), cy.getAuraTrace()
└── support/assert.ts                 assertMoveSpan(trace, move, {minStartMs, maxStartMs, minDurationMs})
```

**Tolerance-based assertions.** MediaPipe is non-deterministic frame-to-frame. The assertion shape is span-presence:

```ts
cy.getAuraTrace().then((trace) => {
  assertMoveSpan(trace, "seesaw", {
    minStartMs: 200,
    maxStartMs: 800,
    minDurationMs: 500,
  });
});
```

Strict tMs equality is a known ceiling — the spec records it and the upgrade path is to swap MediaPipe for a deterministic fixed-point detector on the CI side. We don't go there now (YAGNI — the user's tolerance target is "the same fixture in CI has the same move landed roughly the same place", not "exact same frame").

**Fixtures.** Five `.webm` recordings at 320×240 @ ~30fps × 4s, total ~500KB committed binary. Built once via `scripts/build-fixtures.sh` (uses existing Farm recording path or a synthetic generator). Expected traces live next to the recordings as `.json` files.

**CI integration.** Add `cypress run --browser chrome` to `.github/workflows/`. Cypress job uploads screenshots + traces on failure. Job name matches the existing test conventions.

---

## 8. Migration / rollout

1. Ship the analyze pipeline + 5 Cypress tests behind the existing file mode. (No UI change to Validate; it gets fixed as a side-effect of fixing the file-mode RAF pump.)
2. Land 🔬 Analyze button + scrubber + overlay canvas as the same PR (visually distinct, can be hidden behind `?analyze` URL param while testing).
3. Wire Cypress into CI once green locally.
4. Later: A/B comparison UI reading CI-produced trace diffs.

---

## 9. Out of scope

- **A/B browser UI** — later. CI trace-diff is the first deliverable.
- **Multi-move composite fixtures** — kept single-move per Sergio's request.
- **Changing the live-mode pump** — works, untouched.
- **Porting the engine to Node** — explicit non-goal. Two-engine drift is worse than tolerance-based assertions.

---

## 10. Open questions

- Should the scrubber auto-advance during "Play trace" mode, or always wait for user input? Spec assumes auto-advance; can flip.
- Should the A/B config swap (B-section) be a single selector in the TuningPanel (one of N snapshots), or always the current live tuning? Spec assumes current live tuning; can flip.
- Should fixtures be regenerated by `build-fixtures.sh` on every CI run (synthetic), or remain committed? Spec assumes committed for first rollout; can flip to synthetic later.

---

## 11. Test deliverables (summary)

- `analyze.test.ts` — 5 stub-based self-checks.
- 5 Cypress fixture specs + 1 smoke spec.
- 5 fixture `.webm` files + 5 `.json` expectations, committed.
- 1 fixture-builder script (`scripts/build-fixtures.sh`), runnable manually.
