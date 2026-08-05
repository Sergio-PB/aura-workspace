# Aura Tracking System

> **Living document.** Update whenever tracking capabilities change.
> **Owner:** Farm app (`apps/farm-capacitor`)
> **Last updated:** 2026-08-05

---

## Architecture

```
Camera (getUserMedia)  OR  File Video (<input type="file">)
  → MediaPipe Hands WASM (21 landmarks/hand, 2 hands max)
    → Gesture Detector (static: open, fist, point, peace, thumbs_up)
    → Move Detector (temporal: seesaw, wave, clap, raise_roof, point)
      → Particle Overlay (canvas, burst on gesture/move)
      → Telemetry Debug Panel (real-time data dump)
      → Export (MediaRecorder: video + particles composited)
```

---

## Components

### 1. Camera / File Input

| Property | Value |
|----------|-------|
| Source | `navigator.mediaDevices.getUserMedia` (camera) or `<input type="file">` (pre-recorded video) |
| Resolution | 320×240 (reduced for memory) |
| Mirror | `scaleX(-1)` on video element |
| Transport | HTTPS required (secure context for getUserMedia on non-localhost) |
| File mode | RAF frame pump, playback controls (play/pause/seek), export via MediaRecorder |

**File:** `src/hooks/useMediaPipe.ts` (camera init + file pump in `useEffect`), `src/screens/RecordScreen.tsx` (file input + playback + export)

### 2. MediaPipe Hands

| Property | Value |
|----------|-------|
| Library | `@mediapipe/hands` v0.4 |
| Model | Lite (`modelComplexity: 0`, ~10 MB WASM) |
| Max hands | 2 |
| Detection confidence | 0.7 |
| Tracking confidence | 0.5 |
| Landmarks | 21 per hand (0=wrist, 4=thumb tip, 8=index tip, 12=middle tip, 16=ring tip, 20=pinky tip) |
| WASM source | `cdn.jsdelivr.net/npm/@mediapipe/hands/` |

**File:** `src/hooks/useMediaPipe.ts`

### 3. Hand Classification

MediaPipe returns hands in arbitrary order. We classify by wrist x-position:

| Wrist x | Classification |
|---------|---------------|
| > 0.5 | Left hand (right side of mirrored image) |
| ≤ 0.5 | Right hand (left side of mirrored image) |

**File:** `src/hooks/useMediaPipe.ts` (in `onResults` callback)

### 4. Gesture Detector

Static per-frame classification based on finger extension (tip-to-wrist distance > pip-to-wrist × 1.15).

| Gesture | Fingers extended | Confidence |
|---------|-----------------|------------|
| `open` | All 5 | 0.9 |
| `fist` | None | 0.9 |
| `point` | Index only | 0.85 |
| `peace` | Index + middle | 0.85 |
| `thumbs_up` | Thumb only | 0.8 |
| `unknown` | Any other pattern | 0.5 |

**File:** `src/engine/gestures.ts`

### 5. Move Detector (Seesaw)

Temporal pattern detection over a sliding window.

| Property | Value |
|----------|-------|
| Window | 30 frames (~1s at 30fps) |
| Trigger | 4+ sign changes in (leftWristY - rightWristY) |
| Rate | `min(amplitude / 0.5, 1.0)` — normalized intensity |
| Threshold | 0.05 minimum amplitude |

**File:** `src/engine/moves.ts`

### 6. Particle Overlay

Canvas layer on top of video. Particles burst at wrist positions.

| Property | Value |
|----------|-------|
| Max particles | 200 |
| Spawn per burst | 4 (gesture) / 8 (move) per hand |
| Physics | Random velocity, gravity (0.02), fade over lifetime |
| Lifetime | 40–70 frames |
| Color | HSL cycling hue, 80% saturation, 60% lightness |
| Coordinate system | Normalized (0..1), mirrored x (`1 - wrist.x`) |

**File:** `src/engine/particles.ts`

### 7. Telemetry Debug Panel

Real-time overlay showing what would be sent to backend.

| Field | Source |
|-------|--------|
| FPS | Frame counter / elapsed |
| Gesture | Gesture detector |
| Confidence | Gesture detector |
| Move | Move detector |
| Aura rate | Move detector |
| Hands | Count of tracked hands (0/1/2) |
| L wrist / R wrist | Normalized coordinates |
| Particles | Particle count |
| Geo | Geolocation API (lat, lng) |
| IP | `local (browser)` placeholder |
| Face | `N/A (P-9)` placeholder |
| Time | ISO timestamp |

**File:** `src/screens/RecordScreen.tsx`

---

## State Shape

```typescript
interface HandState {
  left: Landmark[] | null;   // 21 landmarks for left hand
  right: Landmark[] | null;  // 21 landmarks for right hand
  gesture: Gesture;          // current static gesture
  confidence: number;        // gesture confidence
  move: Move;                // current temporal move
  moveRate: number;          // move intensity 0..1
  fps: number;               // frames per second
}
```

---

## Known Limitations

| Issue | Mitigation |
|-------|-----------|
| SIGKILL on 16 GB RAM | modelComplexity=0, 320×240 resolution |
| MediaPipe hand order arbitrary | Classify by wrist x > 0.5 |
| getUserMedia requires HTTPS | `@vitejs/plugin-basic-ssl` for dev |
| iOS front camera mirrors | `scaleX(-1)` on video, `1 - x` on particles |
| No face tracking yet | Planned for P-9 |
| File export is WebM only | MediaRecorder browser support; add MP4 via ffmpeg.wasm if needed |

---

## Adding a New Move

1. Create detector class in `src/engine/moves.ts` (follow `SeesawDetector` pattern)
2. Add to `Move` type union
3. Instantiate in `useMediaPipe.ts`
4. Call `.update()` in `onResults` with relevant landmarks
5. Add to debug panel in `RecordScreen.tsx`

## Adding a New Gesture

1. Add to `Gesture` type union in `src/engine/gestures.ts`
2. Add detection rule in `detectGesture()` (finger extension pattern)
3. No other changes needed — flows through existing state

---

## Performance Budget

| Metric | Target | Current |
|--------|--------|---------|
| WASM size | < 15 MB | ~10 MB (lite) |
| Frame resolution | ≤ 640×480 | 320×240 |
| FPS | ≥ 15 | Varies by device |
| Memory (process) | < 200 MB | ~80 MB (Vite + MediaPipe) |
