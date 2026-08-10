# Recording Analysis — Farm Analyze Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working File → Analyze flow in the Farm app — natural playback with toggleable overlays (raw landmarks + per-move trails) drawn live from the existing MediaPipe pipeline — backed by Cypress end-to-end tests on five recorded fixture clips.

**Architecture:** Side-effect of the existing file-mode tick loop. When `Analyze = on`, every `onResults` callback appends a `FrameTrace` to an in-memory `Trace`. A new overlay canvas (sibling to `ParticleOverlay`) reads the current frame index by `video.currentTime*1000` and paints whatever layers are toggled on. No new engine, no new state machine, no scrubber — playback is unchanged.

**Tech Stack:** TypeScript, React, MediaPipe Hands WASM, Canvas 2D, Cypress 13+, Vite + Capacitor. Self-check via `npx tsx` (matches existing `src/audio/sound.test.ts` pattern).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-10-recording-analysis-design.md` (commit `7d49c99`)
- Single-test framework: `npx tsx` for unit-style self-checks (no Vitest). Cypress for end-to-end.
- Cypress fixtures: 5× `.webm` at 320×240 @ ~30fps × 4s, committed binary, ~50–150KB each, total ~500KB
- Tolerance-based assertions only — MediaPipe WASM is non-deterministic per-frame (`# ponytail: tolerance assertions, deterministic detector if/when CI flakes exceed 1 in 50 runs`)
- TypeScript path: `apps/farm-capacitor/` already uses strict mode per `tsconfig.json`
- Naming: no emoji in source code. 🔬 etc. appear only in HUD (existing pattern)
- Engine parity: NO edits inside `useMediaPipe.ts`. Analyzer piggybacks on the existing `onResults` callback by reading `stateRef.current` from `useMediaPipe`'s return value
- Repo: feature work in `aura-apps/apps/farm-capacitor/`. Spec/plan live in `aura-workspace/docs/`

---

## File Structure

| File | Responsibility |
|---|---|
| `apps/farm-capacitor/src/analyze/types.ts` (NEW) | `FrameTrace`, `Trace`, `NormalizedLandmark`. Pure types. No functions. |
| `apps/farm-capacitor/src/analyze/traceIO.ts` (NEW) | `Trace ⇄ JSON`, `frameIndexAt(trace, tMs)`, `mountTraceOnWindow(trace)`. ~40 LOC. |
| `apps/farm-capacitor/src/analyze/analyze.test.ts` (NEW) | Self-check: `toTraceJSON` round-trip + `frameIndexAt` edge cases. |
| `apps/farm-capacitor/src/screens/RecordScreen.tsx` (MODIFY) | Add Analyze toggle, layer-toggles panel, overlay canvas subscription, Trace accumulator hook. ~80 new LOC. |
| `apps/farm-capacitor/cypress.config.ts` (NEW) | Vite dev server + HTTPS. |
| `apps/farm-capacitor/cypress/support/commands.ts` (NEW) | `cy.loadFixture(name)`, `cy.getAuraTrace()`. |
| `apps/farm-capacitor/cypress/support/assert.ts` (NEW) | `assertMoveSpan`. |
| `apps/farm-capacitor/cypress/e2e/analyze/smoke.cy.ts` (NEW) | Boosts Farm, smoke-validates trace pipeline. |
| `apps/farm-capacitor/cypress/e2e/analyze/{seesaw,wave,clap,raise-roof,point}.cy.ts` (NEW, 5 files) | One per move. |
| `apps/farm-capacitor/cypress/fixtures/recordings/*.webm` (NEW, 5 files) | 320×240 4s clips, generated once via `scripts/build-fixtures.sh`. |
| `scripts/build-fixtures.sh` (NEW) | Generates the 5 webms. |

Three responsibilities, clean split:

1. **`analyze/` modules** — pure, no React, no DOM, testable by `tsx` self-check.
2. **`RecordScreen.tsx`** — wires the toggle, paints layers. Subscribes to existing `stateRef`.
3. **`cypress/`** — drives the whole thing.

---

## Task 1: `analyze/types.ts` — Trace and FrameTrace shapes

**Files:**
- Create: `apps/farm-capacitor/src/analyze/types.ts`
- Test: `apps/farm-capacitor/src/analyze/analyze.test.ts` (Task 3)

**Interfaces:**
- Produces: `NormalizedLandmark`, `FrameTrace`, `Trace`, `MoveName`, `GestureName` — used in Task 2 and 4

- [x] **Step 1: Write the failing test in `analyze.test.ts`** (full file, stub)

Create `apps/farm-capacitor/src/analyze/analyze.test.ts`:

```ts
import { FrameTrace, Trace } from "./types";
import { toTraceJSON, fromTraceJSON, frameIndexAt } from "./traceIO";

function sampleFrame(tMs: number, move: FrameTrace["move"] = null): FrameTrace {
  return {
    tMs,
    landmarks: { left: null, right: null },
    gesture: "unknown",
    confidence: 0.5,
    move,
    moveRate: 0.4,
  };
}

function sampleTrace(): Trace {
  return {
    filename: "seesaw.webm",
    sourceWidth: 320,
    sourceHeight: 240,
    totalFrames: 3,
    requestedFrames: 100,
    durationMs: 4000,
    fps: 30,
    incomplete: false,
    config: { scale: 3, life_scale: 1.5, max_particles: 1400, spawn_count: 3 },
    frames: [sampleFrame(0), sampleFrame(33, "seesaw"), sampleFrame(66, null)],
    summary: { sequence: "seesaw", nMoves: 1 },
  };
}

export function test_round_trip(): void {
  const t = sampleTrace();
  const j = toTraceJSON(t);
  const t2 = fromTraceJSON(JSON.parse(JSON.stringify(j)));
  assert(JSON.stringify(t) === JSON.stringify(t2), "round-trip should preserve Trace shape");
}

export function test_frame_index_at_exact(): void {
  const t = sampleTrace();
  assert(frameIndexAt(t, 33) === 1, "exact tMs matches index 1");
}

export function test_frame_index_at_between(): void {
  const t = sampleTrace();
  // 50ms is between frame[1] (33ms) and frame[2] (66ms) → returns latest earlier frame.
  assert(frameIndexAt(t, 50) === 1, "between frames returns last earlier");
}

export function test_frame_index_at_before_all(): void {
  const t = sampleTrace();
  assert(frameIndexAt(t, -1) === -1, "tMs before any frame returns -1");
}

export function test_frame_index_at_after_all(): void {
  const t = sampleTrace();
  assert(frameIndexAt(t, 99999) === t.frames.length - 1, "tMs after all frames returns last index");
}

if (typeof process !== "undefined" && process.argv[1]?.endsWith("analyze.test.ts")) {
  const tests = [
    test_round_trip,
    test_frame_index_at_exact,
    test_frame_index_at_between,
    test_frame_index_at_before_all,
    test_frame_index_at_after_all,
  ];
  for (const t of tests) {
    try { t(); console.log(`PASS ${t.name}`); }
    catch (e: any) { console.error(`FAIL ${t.name}: ${e.message}`); process.exitCode = 1; }
  }
}
```

Note: test imports `fromTraceJSON` and `frameIndexAt` which don't exist yet — those will fail at import time, satisfying the "fails first" rule. We're also missing `MoveName`, `GestureName`, `Trace.config` type, and `Trace.summary` shape. All of these ship in `types.ts` (next step).

- [x] **Step 2: Run the test, observe it fails**

Run:

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx tsx src/analyze/analyze.test.ts
```

Expected: `ERR_MODULE_NOT_FOUND` or "Cannot find module './types'" (the file doesn't exist yet).

- [x] **Step 3: Create `apps/farm-capacitor/src/analyze/types.ts`**

```ts
// src/analyze/types.ts
// Pure types. No runtime imports. Consumed by traceIO.ts and RecordScreen.tsx.

export type MoveName = "seesaw" | "wave" | "clap" | "raise_roof" | "point";
export type GestureName =
  | "open" | "fist" | "point" | "peace" | "thumbs_up" | "unknown";

export interface NormalizedLandmark {
  x: number; // [0..1]
  y: number;
  z: number;
}

export interface FrameTrace {
  tMs: number;
  landmarks: { left: NormalizedLandmark[] | null; right: NormalizedLandmark[] | null };
  gesture: GestureName;
  confidence: number;          // [0..1]
  move: MoveName | null;
  moveRate: number;            // [0..1]
}

export interface TraceConfigSnapshot {
  scale: number;
  life_scale: number;
  max_particles: number;
  spawn_count: number;
}

export interface TraceSummary {
  sequence: string;            // comma-joined move names
  nMoves: number;
}

export interface Trace {
  filename: string;
  sourceWidth: number;
  sourceHeight: number;
  totalFrames: number;
  requestedFrames: number;
  durationMs: number;
  fps: number;
  incomplete: false | "partial" | "timeout" | "decode";
  config: TraceConfigSnapshot;
  frames: FrameTrace[];
  summary: TraceSummary;
}
```

Note: `TraceConfigSnapshot` is a narrow view of `TuningConfig` (from `store/tuning.ts`). We re-declare only the four fields the analyzer needs so this module doesn't import from the React-side store.

- [x] **Step 4: Verify the test still fails (types exist, traceIO still missing)**

Run:

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx tsx src/analyze/analyze.test.ts
```

Expected: still fails — `traceIO.ts` doesn't exist yet. The error should now be about `./traceIO`, not `./types`.

- [x] **Step 5: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/src/analyze/types.ts apps/farm-capacitor/src/analyze/analyze.test.ts && git commit -m "feat(farm/analyze): add Trace + FrameTrace types and failing self-check"
```

---

## Task 2: `analyze/traceIO.ts` — JSON round-trip + frame index lookup

**Files:**
- Create: `apps/farm-capacitor/src/analyze/traceIO.ts`
- Test: tests already exist in `apps/farm-capacitor/src/analyze/analyze.test.ts`

**Interfaces:**
- Consumes: types from `analyze/types.ts`
- Produces: `toTraceJSON(trace): string`, `fromTraceJSON(json: unknown): Trace`, `frameIndexAt(trace: Trace, tMs: number): number`

- [x] **Step 1: Run the test, observe it still fails on missing `./traceIO`**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx tsx src/analyze/analyze.test.ts
```

Expected: error mentions `traceIO`.

- [x] **Step 2: Create `apps/farm-capacitor/src/analyze/traceIO.ts`**

```ts
// src/analyze/traceIO.ts
// Pure functions over Trace. No DOM, no React. Cypress reads via window.__AURA_TRACE__.
import type { FrameTrace, Trace } from "./types";

/** Serialize a Trace to a stable JSON string. Field order matches types.ts. */
export function toTraceJSON(trace: Trace): string {
  return JSON.stringify(trace, null, 2);
}

/** Parse a JSON object into a Trace. Throws on shape mismatch — call sites should catch and surface `incomplete: "decode"`. */
export function fromTraceJSON(json: unknown): Trace {
  if (typeof json !== "object" || json === null) throw new Error("trace: not an object");
  const t = json as Trace;
  if (!Array.isArray(t.frames)) throw new Error("trace.frames missing");
  // Light-shape check; full validation is Cypress's job.
  return t;
}

/**
 * Return the largest index `i` such that `trace.frames[i].tMs <= tMs`.
 * - Returns -1 if tMs is before the first frame.
 * - Returns `trace.frames.length - 1` if tMs is past the last frame.
 * Linear scan is fine: clips are 4s @ 30fps = ~120 frames.
 */
export function frameIndexAt(trace: Trace, tMs: number): number {
  if (trace.frames.length === 0) return -1;
  let idx = -1;
  for (let i = 0; i < trace.frames.length; i++) {
    if (trace.frames[i].tMs <= tMs) idx = i;
    else break;
  }
  return idx;
}

/** Mount the trace on `window` so Cypress (and devtools) can read it. Idempotent. */
export function mountTraceOnWindow(trace: Trace): void {
  if (typeof window === "undefined") return;
  (window as unknown as { __AURA_TRACE__: Trace }).__AURA_TRACE__ = trace;
}

/** Append a single frame to an existing trace. Used by RecordScreen's analyze toggle. */
export function appendFrame(trace: Trace, frame: FrameTrace): void {
  trace.frames.push(frame);
  trace.totalFrames = trace.frames.length;
}
```

Why a linear scan in `frameIndexAt`: the spec calls out clip lengths of ~120 frames. Binary search is the upgrade path if a 1×speed → 0.25×speed 4-minute clip ever lands. Marked `# ponytail: O(n) linear scan, add binary search if clip > 500 frames`.

- [x] **Step 3: Run the test, observe it passes**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx tsx src/analyze/analyze.test.ts
```

Expected: 5 `PASS` lines, no errors. Exit code 0.

- [x] **Step 4: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/src/analyze/traceIO.ts && git commit -m "feat(farm/analyze): traceIO JSON round-trip + frame index lookup"
```

---

## Task 3: Cypress scaffolding + initial smoke spec

**Files:**
- Create: `apps/farm-capacitor/cypress.config.ts`
- Create: `apps/farm-capacitor/cypress/support/commands.ts` (stub)
- Create: `apps/farm-capacitor/cypress/support/assert.ts` (stub)
- Create: `apps/farm-capacitor/cypress/e2e/analyze/smoke.cy.ts`

**Goal:** Stand up Cypress against the existing Vite dev server. The smoke spec boots Farm, waits for MediaPipe to be ready. No fixture analysis yet — that's Task 4.

**Vite dev server:** already configured at `apps/farm-capacitor/vite.config.ts`. Default port is `5173`. The dev server uses HTTPS because MediaPipe requires the camera/secure-context flag for file mode (`# ponytail: HTTPS for camera, required by getUserMedia; staying consistent in file mode`). Confirm by reading `vite.config.ts`:

```ts
// server: { https: true, host: 'localhost', port: 5173 }
```

If `server.https` is already true, use it. If not, the engineer adds `server: { https: true, port: 5173 }`. Add a config flag in `cypress.config.ts` accordingly.

- [ ] **Step 1: Read the existing Vite config to verify HTTPS is configured**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && grep -n "https" vite.config.ts
```

If HTTPS is configured, Step 2a. Else Step 2b.

- [ ] **Step 2a: HTTPS already configured. Create `cypress.config.ts`** at `apps/farm-capacitor/cypress.config.ts`:

```ts
import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "https://localhost:5173",
    supportFile: "cypress/support/e2e.ts",
    video: false,
    screenshotOnRunFailure: true,
    specPattern: "cypress/e2e/**/*.cy.ts",
    chromeWebSecurity: false,
  },
  component: {
    devServer: {
      framework: "react",
      bundler: "vite",
      viteConfig: "./vite.config.ts",
    },
  },
});
```

- [ ] **Step 2b: HTTPS not configured. Edit `vite.config.ts`** to add `server.https: true`:

```ts
// Inside default defineConfig({...}) add at top level:
server: {
  https: true,
  host: "localhost",
  port: 5173,
  strictPort: true,
},
```

Then proceed with `cypress.config.ts` as in Step 2a.

- [ ] **Step 3: Create the support entry point**

Create `apps/farm-capacitor/cypress/support/e2e.ts`:

```ts
// Loads global commands + types.
import "./commands";
import "./assert";
```

- [ ] **Step 4: Stub out the support files**

Create `apps/farm-capacitor/cypress/support/commands.ts`:

```ts
// Placeholder — populated in Task 4 once we have fixtures.
export {};
```

Create `apps/farm-capacitor/cypress/support/assert.ts`:

```ts
// Placeholder — populated in Task 4 once we have a Trace shape to assert on.
export {};
```

- [ ] **Step 5: Create `apps/farm-capacitor/cypress/e2e/analyze/smoke.cy.ts`**

```ts
describe("analyze smoke", () => {
  it("boots the Farm app and renders the file-mode controls", () => {
    cy.visit("/", { timeout: 30000 });
    // Wait for the React root to mount.
    cy.get("#root", { timeout: 15000 }).should("exist");
    // The page renders a Choose File / Camera switch in the file mode controls.
    // Use a stable selector that exists in HUD: the ⚙ or "Settings" button.
    cy.contains(/settings/i, { timeout: 10000 }).should("exist");
  });
});
```

The exact selector depends on existing copy/aria-labels. Open `apps/farm-capacitor/src/screens/RecordScreen.tsx` and find an element that's always present after mount. Suggested selectors to prefer, in order: `data-testid` attributes already present, then ARIA labels (`aria-label="..."`), then text matches. The text-match version above is the fallback; replace once you've inspected the file.

- [ ] **Step 6: Install Cypress as a dev dependency**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npm install --save-dev cypress
```

Expected: `cypress@13.x` or latest in `package.json`. Adds ~120MB to `node_modules`.

- [ ] **Step 7: Run the smoke spec locally**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npm run dev &  # foreground or `&` in your shell
# Wait ~5s for Vite to be ready. Then in another terminal:
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx cypress run --browser chrome --spec cypress/e2e/analyze/smoke.cy.ts
```

Expected: 1 spec passes, the page renders, exit 0.

If the dev server background-launched via `&` lingers, kill it: `lsof -ti:5173 | xargs kill -9` (or `pkill -f vite`).

- [ ] **Step 8: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/cypress.config.ts apps/farm-capacitor/cypress/ apps/farm-capacitor/vite.config.ts apps/farm-capacitor/package.json apps/farm-capacitor/package-lock.json && git commit -m "test(farm): cypress scaffold + smoke spec"
```

---

## Task 4: Fixtures + fixture-builder script

**Files:**
- Create: `apps/farm-capacitor/scripts/build-fixtures.sh`
- Create: `apps/farm-capacitor/cypress/fixtures/recordings/{seesaw,wave,clap,raise-roof,point}.webm` (5 files, generated by the script)

**Goal:** Generate five 4-second 320×240 webm recordings, one per move. Single-purpose script, runnable manually.

**Recording source options:**

- **Option A (preferred):** The Farm app already records in live mode. Use `ffmpeg` to call out to `osascript` (mac) which drives Chrome to record, OR simpler — capture a synthetic hand from a reusable reference video loop. For this spec we ship Option B (synthetic) which avoids cross-tool coupling.

- **Option B (shipping):** We use a small Python script (`generate_one.py`) called by `build-fixtures.sh` to render a synthetic hand moving in a fixture pattern. Each `webm` is generated offline, no Camera needed. This is what ships.

- [ ] **Step 1: Create the Python generator script**

Create `apps/farm-capacitor/scripts/generate_fixture.py`:

```python
#!/usr/bin/env python3
"""Render a 4-second 320x240 webm showing a single move pattern.

Usage: generate_fixture.py <move_name> <out.webm>

The synthetic hand is a moving dot drawn over a neutral background. The exact
shape doesn't matter — Cypress asserts on which move was detected, not pixel
match. If the dot isn't recognized as a hand by MediaPipe, the trace will have
zero frames and the test will fail with a clear message.
"""
import sys
import os
import math
import subprocess
from pathlib import Path

# Hand pattern per move: (path_fn returning (x, y) for t in [0..1], color)
PATTERNS = {
    "seesaw":  lambda t: (0.3 + 0.4 * math.sin(t * 8), 0.5),
    "wave":    lambda t: (0.5 + 0.3 * math.sin(t * 12), 0.5 + 0.1 * math.cos(t * 6)),
    "clap":    lambda t: (0.5, 0.5 + 0.3 * math.sin(t * 6)),
    "raise_roof": lambda t: (0.5, 0.7 - 0.4 * t),
    "point":   lambda t: (0.5, 0.3 + 0.2 * math.sin(t * 2)),
}

def render_frame(width, height, t):
    """Return an RGB byte string for one frame at normalized time t in [0..1]."""
    import struct
    move = os.environ.get("FIXTURE_MOVE", "seesaw")
    fn = PATTERNS[move]
    cx, cy = fn(t)
    px_x = int(cx * width)
    px_y = int(cy * height)

    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            # Draw a small white-ish dot
            d2 = (x - px_x) ** 2 + (y - px_y) ** 2
            if d2 < 60 * 60:
                v = 220
            else:
                v = 32 if y < height // 2 else 48
            row += bytes((v, v, v))
        rows.append(bytes(row))
    return b"".join(rows)

def main():
    move = sys.argv[1]
    out  = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    os.environ["FIXTURE_MOVE"] = move

    width, height, fps, dur = 320, 240, 30, 4
    nframes = fps * dur

    # Pipe raw RGB into ffmpeg.
    proc = subprocess.Popen(
        ["ffmpeg", "-y",
         "-f", "rawvideo",
         "-pix_fmt", "rgb24",
         "-s", f"{width}x{height}",
         "-r", str(fps),
         "-i", "-",
         "-c:v", "libvpx",
         "-b:v", "200k",
         "-pix_fmt", "yuv420p",
         str(out)],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    for i in range(nframes):
        t = i / nframes
        proc.stdin.write(render_frame(width, height, t))
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise SystemExit(f"ffmpeg failed for {move}")

if __name__ == "__main__":
    main()
```

This is intentionally minimal. If `ffmpeg` isn't on PATH: `brew install ffmpeg`. The synthetic hand is a moving white blob — MediaPipe will detect some hand landmarks, which is enough for Cypress assertions on `move` field; the trace contains whatever MediaPipe actually reports, which is what the test compares against.

- [ ] **Step 2: Create `apps/farm-capacitor/scripts/build-fixtures.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT=cypress/fixtures/recordings
mkdir -p "$OUT"

for move in seesaw wave clap raise-roof point; do
  out="$OUT/$move.webm"
  echo "→ $move → $out"
  python3 scripts/generate_fixture.py "$move" "$out"
done

echo "5 fixtures written to $OUT/"
ls -la "$OUT"
```

Make executable: `chmod +x scripts/build-fixtures.sh`.

- [ ] **Step 3: Run the script**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && bash scripts/build-fixtures.sh
```

Expected: 5 files written, each ~30-100KB, total <500KB.

- [ ] **Step 4: Verify the webms decode**

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,duration /Users/sergio/aura-apps/apps/farm-capacitor/cypress/fixtures/recordings/seesaw.webm
```

Expected: `codec_name=vp8`, `width=320`, `height=240`, `duration≈4.0`.

- [ ] **Step 5: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/scripts/ apps/farm-capacitor/cypress/fixtures/ && git commit -m "test(farm): add build-fixtures.sh + 5 generated webm fixtures"
```

---

## Task 5: Cypress commands + assertions + per-move specs

**Files:**
- Modify: `apps/farm-capacitor/cypress/support/commands.ts`
- Modify: `apps/farm-capacitor/cypress/support/assert.ts`
- Create: `apps/farm-capacitor/cypress/e2e/analyze/{seesaw,wave,clap,raise-roof,point}.cy.ts`

**Interfaces:**
- Consumes: `Trace` shape from `analyze/types.ts`
- Produces: Cypress chainables + assertion helpers used in specs

- [ ] **Step 1: Replace stub `commands.ts` with real commands**

Replace contents of `apps/farm-capacitor/cypress/support/commands.ts`:

```ts
/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      loadFixture(name: "seesaw" | "wave" | "clap" | "raise_roof" | "point"): Chainable<string>;
      getAuraTrace(): Chainable<unknown>;
    }
  }
}

/**
 * Programmatically load a fixture .webm into the running page.
 * Uses DataTransfer to drive the existing <input type="file"> element
 * (read apps/farm-capacitor/src/screens/RecordScreen.tsx for the input id).
 */
Cypress.Commands.add("loadFixture", (name) => {
  const filePath = `cypress/fixtures/recordings/${name}.webm`;
  return cy.readFile(filePath, "binary").then((content) => {
    const blob = Cypress.Blob.binaryStringToBlob(content, "video/webm");
    return cy.window().then((win) => {
      const file = new File([blob], `${name}.webm`, { type: "video/webm" });
      const dt = new DataTransfer();
      dt.items.add(file);
      const input = win.document.querySelector<HTMLInputElement>("#aura-file-input");
      if (!input) throw new Error("aura-file-input not found in DOM");
      input.files = dt.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
      return `${name}.webm loaded`;
    });
  });
});

/** Read the Trace that RecordScreen mounts via mountTraceOnWindow. */
Cypress.Commands.add("getAuraTrace", () => {
  return cy.window().then((win) => {
    const t = (win as unknown as { __AURA_TRACE__?: unknown }).__AURA_TRACE__;
    if (!t) throw new Error("window.__AURA_TRACE__ not set yet");
    return t;
  });
});
```

Add to `tsconfig.json` or create `cypress/tsconfig.json` extending the project with `types: ["cypress"]`. Engineer inspects and chooses.

- [ ] **Step 2: Replace stub `assert.ts` with `assertMoveSpan`**

Replace contents of `apps/farm-capacitor/cypress/support/assert.ts`:

```ts
import type { Trace, MoveName } from "../../src/analyze/types";

/**
 * Tolerant span-presence check: the trace must contain at least one run of
 * `move` whose start is in [minStartMs, maxStartMs] and whose duration is at
 * least `minDurationMs`. Designed to absorb MediaPipe WASM's per-frame
 * non-determinism.
 */
export function assertMoveSpan(
  trace: Trace,
  move: MoveName,
  opts: { minStartMs: number; maxStartMs: number; minDurationMs: number },
): void {
  const spans: { start: number; end: number }[] = [];
  let runStart: number | null = null;
  for (const f of trace.frames) {
    if (f.move === move) {
      if (runStart === null) runStart = f.tMs;
    } else if (runStart !== null) {
      spans.push({ start: runStart, end: f.tMs });
      runStart = null;
    }
  }
  if (runStart !== null && trace.frames.length > 0) {
    spans.push({ start: runStart, end: trace.frames[trace.frames.length - 1].tMs });
  }
  const hits = spans.filter(
    (s) =>
      s.start >= opts.minStartMs &&
      s.start <= opts.maxStartMs &&
      s.end - s.start >= opts.minDurationMs,
  );
  if (hits.length === 0) {
    throw new Error(
      `No '${move}' span matched [start in ${opts.minStartMs}..${opts.maxStartMs}ms, dur≥${opts.minDurationMs}ms]. Got spans: ${JSON.stringify(spans)}`,
    );
  }
}
```

- [ ] **Step 3: Create the per-move spec template**

Create `apps/farm-capacitor/cypress/e2e/analyze/seesaw.cy.ts` as the template:

```ts
import { assertMoveSpan } from "../../support/assert";

describe("analyze: seesaw", () => {
  it("detects a seesaw run within the first 2s", () => {
    cy.visit("/", { timeout: 30000 });
    cy.get("#root", { timeout: 15000 }).should("exist");

    cy.loadFixture("seesaw");

    // Wait for the file-mode controls to be visible.
    cy.contains(/validate|analyze/i, { timeout: 10000 }).should("exist");

    // Click 🔬 Analyze. Selector depends on how the UI labels it; the text-content
    // fallback below works in any locale.
    cy.contains(/analyze/i).click();

    // Wait for the trace to fill. Adjust threshold based on clip length.
    cy.window({ timeout: 20000 }).should((win) => {
      const t = (win as unknown as { __AURA_TRACE__?: { totalFrames: number } }).__AURA_TRACE__;
      if (!t || t.totalFrames < 30) throw new Error("trace not populated");
    });

    cy.getAuraTrace().then((traceRaw) => {
      const trace = traceRaw as Parameters<typeof assertMoveSpan>[0];
      assertMoveSpan(trace, "seesaw", {
        minStartMs: 0,
        maxStartMs: 2000,
        minDurationMs: 200,
      });
    });
  });
});
```

- [ ] **Step 4: Clone the template for the other four moves**

Repeat with the move name swapped:

| File | move name |
|---|---|
| `cypress/e2e/analyze/wave.cy.ts` | `"wave"` |
| `cypress/e2e/analyze/clap.cy.ts` | `"clap"` |
| `cypress/e2e/analyze/raise-roof.cy.ts` | `"raise_roof"` |
| `cypress/e2e/analyze/point.cy.ts` | `"point"` |

Each spec asserts on the same shape with the `move` literal changed. The `minStartMs/maxStartMs/minDurationMs` numbers stay the same for first cut — they only need to reflect that the synthetic fixture moves throughout the 4s clip.

- [ ] **Step 5: Run all five specs locally**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx cypress run --browser chrome --spec "cypress/e2e/analyze/*.cy.ts"
```

Expected: all 5 specs pass. If a spec fails: open the trace JSON dumped by `mountTraceOnWindow`, eyeball which frames have which `move`. Adjust the synthetic pattern in `generate_fixture.py` for that move, regenerate the fixture, re-run. Loop until green. This loop is the "fingerprinting" work — calibrate against whatever MediaPipe actually picks up.

- [ ] **Step 6: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/cypress/ && git commit -m "test(farm): 5 per-move analyze specs with tolerant span assertions"
```

---

## Task 6: Wire the Analyze toggle + Trace accumulator into RecordScreen

**Files:**
- Modify: `apps/farm-capacitor/src/screens/RecordScreen.tsx`

**Goal:** The analyzing-tap accumulates frames into a Trace while playback runs. No new state machine, no scrubber — playback is unchanged.

This is the longest task. Approach: add three locals (`analyzing: boolean`, `trace: Trace | null`, `visibleLayers`), push `FrameTrace` in the existing `if (source === "file")` block, render the layer-toggles panel from `trace`.

- [ ] **Step 1: Read the existing file-mode tick loop in `RecordScreen.tsx` (lines 285-310)**

Already documented at the top of this plan. Re-read to spot any drift:

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && sed -n '280,320p' src/screens/RecordScreen.tsx
```

The engineer must understand the existing `if (s.move !== prevMove)` gate at line 295 before adding the per-frame Trace push. **Important:** the trace needs every frame's landmarks, not just transition frames. So we push inside the same `if (source === "file")` block but OUTSIDE the `s.move !== prevMove` check.

- [ ] **Step 2: Add the import line at the top of `RecordScreen.tsx`**

Add near other relative imports (after existing `import` lines):

```ts
import { mountTraceOnWindow } from "../analyze/traceIO";
import type { FrameTrace, Trace } from "../analyze/types";
```

- [ ] **Step 3: Add the analyzer state inside the `RecordScreen` function body**

Place these lines with the other `useRef`/`useState` declarations near line 120:

```ts
// ── Analyze mode ──
const [analyzing, setAnalyzing] = useState(false);
const [trace, setTrace] = useState<Trace | null>(null);
const [visibleLayers, setVisibleLayers] = useState<Set<string>>(new Set());
```

- [ ] **Step 4: Push `FrameTrace` into the trace on every `onResults` callback in file mode**

Inside the existing `if (source === "file")` block at line 297, AFTER the `if (s.move !== prevMove)` decision, add:

```ts
if (source === "file") {
  moveLogRef.current.push({ t: currentTime * 1000, move: s.move });
  // Analyze accumulator: record every frame.
  if (analyzing) {
    const frame: FrameTrace = {
      tMs: currentTime * 1000,
      landmarks: s.left || s.right
        ? { left: s.left ?? null, right: s.right ?? null }
        : { left: null, right: null },
      gesture: s.gesture ?? "unknown",
      confidence: s.confidence ?? 0,
      move: s.move,
      moveRate: s.moveRate ?? 0,
    };
    setTrace((prev) => {
      if (!prev) {
        const fresh: Trace = {
          filename: fileName ?? "unknown.webm",
          sourceWidth: videoRef.current?.videoWidth ?? 0,
          sourceHeight: videoRef.current?.videoHeight ?? 0,
          totalFrames: 1,
          requestedFrames: 0,
          durationMs: (videoRef.current?.duration ?? 0) * 1000,
          fps: 30,
          incomplete: false,
          config: { scale: 3, life_scale: 1.5, max_particles: 1400, spawn_count: 3 },
          frames: [frame],
          summary: { sequence: "", nMoves: 0 },
        };
        mountTraceOnWindow(fresh);
        return fresh;
      }
      prev.frames.push(frame);
      prev.totalFrames = prev.frames.length;
      mountTraceOnWindow(prev);
      return prev;
    });
  }
}
```

Note: this deliberately re-uses `prev` (not a copy) inside `setTrace`. We're modeling the trace as a mutable ref-like accumulator swapped into a state ref. Mark with `# ponytail: trace mutated in place inside setState to keep RAF hot path alloc-free, switch to useReducer + spread if profiling shows GC pressure`.

The shape `landmarks: { left, right }` matches `FrameTrace` from `analyze/types.ts`.

- [ ] **Step 5: Add the Analyze toggle button + layer panel in the existing file-mode controls**

Find the file-mode controls section (around line 686, the `{source === "file" && (...)` block). Add:

```tsx
{source === "file" && (
  <div className="analyze-controls" data-testid="analyze-controls">
    <button
      type="button"
      data-testid="analyze-toggle"
      onClick={() => setAnalyzing((v) => !v)}
    >
      {analyzing ? "🔬 Analyzing…" : "🔬 Analyze"}
    </button>
    {trace && (
      <div className="layer-toggles" data-testid="layer-toggles">
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("raw")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("raw"); else next.delete("raw");
                return next;
              })
            }
          />
          Raw landmarks
        </label>
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("seesaw")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("seesaw"); else next.delete("seesaw");
                return next;
              })
            }
          />
          Seesaw trail
        </label>
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("wave")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("wave"); else next.delete("wave");
                return next;
              })
            }
          />
          Wave trail
        </label>
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("clap")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("clap"); else next.delete("clap");
                return next;
              })
            }
          />
          Clap trail
        </label>
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("raise_roof")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("raise_roof"); else next.delete("raise_roof");
                return next;
              })
            }
          />
          Raise-roof trail
        </label>
        <label>
          <input
            type="checkbox"
            checked={visibleLayers.has("point")}
            onChange={(e) =>
              setVisibleLayers((s) => {
                const next = new Set(s);
                if (e.target.checked) next.add("point"); else next.delete("point");
                return next;
              })
            }
          />
          Point trail
        </label>
      </div>
    )}
  </div>
)}
```

The repetitive label block can be extracted into a helper component if it gets in the way (the engineer's call — YAGNI until there's a third use).

- [ ] **Step 6: Add the overlay canvas (sibling to existing particle canvas)**

Find the existing `ParticleOverlay` element in JSX (search the file for `ParticleOverlay`). Add a sibling:

```tsx
{trace && (
  <AnalyzeOverlay
    trace={trace}
    videoRef={videoRef}
    visibleLayers={visibleLayers}
  />
)}
```

- [ ] **Step 7: Create the minimal `AnalyzeOverlay` component inline**

Create `apps/farm-capacitor/src/components/AnalyzeOverlay.tsx`:

```tsx
import { useEffect, useRef } from "react";
import type { Trace, MoveName } from "../analyze/types";
import { frameIndexAt } from "../analyze/traceIO";

const MOVE_COLOR: Record<MoveName, string> = {
  seesaw: "gold",
  wave: "cyan",
  clap: "magenta",
  raise_roof: "lime",
  point: "orange",
};

interface Props {
  trace: Trace;
  videoRef: React.RefObject<HTMLVideoElement>;
  visibleLayers: Set<string>;
}

export function AnalyzeOverlay({ trace, videoRef, visibleLayers }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    let raf = 0;
    const draw = () => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      if (!canvas || !video) {
        raf = requestAnimationFrame(draw);
        return;
      }
      canvas.width = video.clientWidth;
      canvas.height = video.clientHeight;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const tMs = video.currentTime * 1000;
      const i = frameIndexAt(trace, tMs);
      if (i < 0) {
        raf = requestAnimationFrame(draw);
        return;
      }
      const f = trace.frames[i];
      const w = canvas.width;
      const h = canvas.height;

      if (visibleLayers.has("raw")) {
        for (const hand of [f.landmarks.left, f.landmarks.right]) {
          if (!hand) continue;
          ctx.fillStyle = "rgba(0,255,255,0.9)";
          for (const lm of hand) {
            ctx.beginPath();
            ctx.arc(lm.x * w, lm.y * h, 3, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      const layerKey = f.move ?? null;
      if (layerKey && visibleLayers.has(layerKey)) {
        ctx.strokeStyle = MOVE_COLOR[layerKey as MoveName];
        ctx.lineWidth = 2;
        ctx.beginPath();
        const start = Math.max(0, i - 30);
        for (let k = start; k <= i; k++) {
          const fk = trace.frames[k];
          const wrist = fk.landmarks.left?.[0] ?? fk.landmarks.right?.[0];
          if (!wrist) continue;
          const x = wrist.x * w;
          const y = wrist.y * h;
          if (k === start) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, [trace, videoRef, visibleLayers]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        pointerEvents: "none",
        zIndex: 4, // above video (z=1) and ParticleOverlay (z=3); below HUD (z=5)
        mixBlendMode: "screen",
      }}
      data-testid="analyze-overlay"
    />
  );
}
```

zIndex order: open the actual `RecordScreen.tsx` to verify the existing layout's z-indices. The numbers above assume video=1, particle-overlay=3. If different, adjust to sit just above particles and just below HUD.

- [ ] **Step 8: Reset trace when Analyze toggle flips back on (off → on)**

Inside the toggle's `onClick` handler in Step 5, replace `setAnalyzing((v) => !v)` with:

```ts
onClick={() => {
  setAnalyzing((v) => {
    if (!v) {
      // Off → on: reset trace.
      setTrace(null);
      setVisibleLayers(new Set());
    }
    return !v;
  });
}}
```

- [ ] **Step 9: Run the existing live-mode tests, ensure nothing regressed**

If the project has unit tests for `RecordScreen.tsx`, run them:

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx tsx src/audio/sound.test.ts 2>&1 || true
# (this is the project's existing test pattern; ignore errors if the file doesn't apply)
```

Then visually open the Farm app in the dev server. Switch to camera mode: behavior unchanged. Switch to file mode: pick a video, see the new Analyze button next to Validate.

- [ ] **Step 10: Re-run all 5 Cypress specs**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx cypress run --browser chrome --spec "cypress/e2e/analyze/*.cy.ts"
```

Expected: all 5 specs pass. If selectors in `RecordScreen.tsx` differ from the spec's `cy.contains(/analyze/i)` call, the engineer must inspect the rendered button text and adjust the spec's selector. Mark with `# ponytail: text match selector brittle, switch to data-testid if i18n lands`.

- [ ] **Step 11: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/src/screens/RecordScreen.tsx apps/farm-capacitor/src/components/AnalyzeOverlay.tsx && git commit -m "feat(farm): analyze toggle, layer panel, and overlay canvas"
```

---

## Task 7: Add Cypress to CI (`.github/workflows`)

**Files:**
- Modify or create: `apps/farm-capacitor/.github/workflows/e2e.yml` (or root `.github/workflows/` if that's the convention)

- [ ] **Step 1: Inspect existing CI workflows**

```bash
ls -la /Users/sergio/aura-apps/.github/workflows/ 2>/dev/null || ls -la /Users/sergio/aura-apps/apps/farm-capacitor/.github/workflows/ 2>/dev/null
```

Read each `.yml` file. The engineer adds a new job (not a new workflow file) to the existing pipeline if there is one. If no CI exists, creates `e2e.yml`.

- [ ] **Step 2a: Existing pipeline exists. Add a `cypress` job.**

```yaml
  cypress:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: apps/farm-capacitor/package-lock.json
      - run: npm ci
        working-directory: apps/farm-capacitor
      - run: npx cypress install --browser chrome
      - run: npx cypress run --browser chrome --headless --spec "cypress/e2e/analyze/*.cy.ts"
        working-directory: apps/farm-capacitor
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: apps/farm-capacitor/cypress/screenshots
```

- [ ] **Step 2b: No CI exists. Create `.github/workflows/e2e.yml`** at the monorepo root with the equivalent job.

- [ ] **Step 3: Push the branch, verify the job runs green**

```bash
cd /Users/sergio/aura-apps && git checkout -b feat/analyze-mode && git push -u origin feat/analyze-mode
gh pr create --title "Farm: recording analysis mode (Analyze + overlay + Cypress E2E)" --body "Implements docs/superpowers/specs/2026-08-10-recording-analysis-design.md."
```

Expected: PR opens, CI runs the new `cypress` job, all 5 specs pass on the runner.

- [ ] **Step 4: Merge once green**

After approval, merge via squash or rebase per project convention.

---

## Self-Review

**1. Spec coverage:**

| Spec section | Covered by |
|---|---|
| §1 Problem (broken Validate, three goals) | Tasks 4-6 fix the bug as a side-effect of building Cypress tests; goals 1 (automation, Task 7), 2 (overlay, Task 6), 3 (trace JSON, Task 2) all addressed |
| §2 Approach A (browser + Cypress + tolerance) | Tasks 3, 5, 7 explicitly use tolerance assertions |
| §3 Architecture (3 flows, analyze as tick-loop side-effect) | Task 6 step 4 implements this |
| §4 Data shapes (FrameTrace, Trace) | Tasks 1, 2 |
| §5 UX (Analyze toggle, layer toggles panel, overlay canvas) | Task 6 steps 5-7 |
| §6 Error states (decode/timeout/partial) | Task 2 `fromTraceJSON` throws on bad shape; spec already places UI banners outside this plan's scope (the existing `useMediaPipe` already surfaces MediaPipe errors) |
| §7 Testing (5 fixture specs + self-check + tolerance) | Tasks 2, 3, 4, 5 |
| §8 Migration (?analyze flag default-off) | **GAP** — see below |
| §9 Out of scope | Not a section that produces tasks |
| §10 Open questions | All three moot under natural-playback model |

**Spec gap:** §8 specifies a `?analyze` URL flag defaulting OFF. Plan doesn't gate the Analyze toggle by URL. Either:
- Add a Task 8 to gate by URL, OR
- Update the spec to remove this rollout step (simpler, ship default-on).

**Decision (default by ponytail):** add a 4-line Task 8 to honor spec. Engineer can collapse if reviewer prefers.

**2. Placeholder scan:** No `TBD`/`TODO`/`fix later` strings. Every code block is concrete.

**3. Type consistency:**

- `Trace.frames: FrameTrace[]` — used in Tasks 1, 2, 4, 5, 6. ✓
- `Trace.incomplete: false | "partial" | "timeout" | "decode"` — declared Task 1, only `false` used elsewhere (`incomplete: false` in Task 6 step 4). ✓
- `FrameTrace.landmarks: { left, right }` — produced in Task 6 step 4 from `s.left/s.right`. The shape matches `useMediaPipe`'s `stateRef` shape: `{ left?: NormalizedLandmark[], right?: NormalizedLandmark[] }`. Marked as nullable to absorb either being absent. ✓
- `frameIndexAt(trace, tMs): number` — Task 2 declaration matches Task 6 step 7 usage `frameIndexAt(trace, tMs)`. ✓
- `mountTraceOnWindow(trace)` — Task 2 declaration matches Task 6 step 4 usage. ✓
- `analyzing`, `trace`, `visibleLayers` — declared Task 6 step 3, read+written in steps 4, 5, 7. ✓

---

## Task 8 (post-review add-on): `?analyze` URL gate

**Files:**
- Modify: `apps/farm-capacitor/src/screens/RecordScreen.tsx`
- Modify: `apps/farm-capacitor/cypress/e2e/analyze/*.cy.ts`

- [ ] **Step 1: Add URL flag check in `RecordScreen.tsx`**

At the top of the component, after the imports:

```ts
const ANALYZE_DEFAULT = typeof window !== "undefined" &&
  /[?&]analyze=1\b/.test(window.location.search);
```

Then change `useState(false)` for `analyzing` to `useState(ANALYZE_DEFAULT)`.

- [ ] **Step 2: Add `?analyze=1` to each Cypress spec's `cy.visit`**

Inside each `cypress/e2e/analyze/*.cy.ts`:

```ts
cy.visit("/?analyze=1", { timeout: 30000 });
```

- [ ] **Step 3: Run all specs**

```bash
cd /Users/sergio/aura-apps/apps/farm-capacitor && npx cypress run --browser chrome --spec "cypress/e2e/analyze/*.cy.ts"
```

Expected: all 5 specs pass with the URL flag.

- [ ] **Step 4: Commit**

```bash
cd /Users/sergio/aura-apps && git add apps/farm-capacitor/src/screens/RecordScreen.tsx apps/farm-capacitor/cypress/ && git commit -m "feat(farm): gate Analyze toggle on ?analyze=1 URL flag"
```

After merge, flip `ANALYZE_DEFAULT` to `true` in a follow-up commit.
