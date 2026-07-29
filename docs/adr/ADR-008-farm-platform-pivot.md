# ADR-008: Farm Platform Pivot — Cross-Platform (Mobile + Web + VR)

Date: 2026-07-27
Status: accepted

## Context

ADR-002 chose React Native with Expo for The Farm. This was correct for a mobile-only Farm. New requirement: The Farm must also run on VR/AR glasses (Meta Quest, future Ray-Ban Meta streaming) and as a web SPA. React Native cannot do this — it has no VR support and no web target.

We need a single codebase that runs on: iOS, Android, web browsers, and VR headsets (via WebXR).

## Options Considered

### A: React Native + React Native Web + separate WebXR client

- **Pros:** Keeps existing Farm code, adds web via RN Web, VR as separate web app
- **Cons:** Three targets, RN Web has gaps (camera, native modules), VR is a separate codebase, defeats "works everywhere" goal

### B: Flutter

- **Pros:** Single codebase, web target, growing ecosystem
- **Cons:** No VR/WebXR support, Dart ecosystem smaller for camera/ML, agent less productive in Dart, would require full rewrite of existing Farm code

### C: Progressive Web App (PWA) with Web APIs

- **Pros:** Single codebase everywhere — phones (browser or installed PWA), desktop, VR headsets (Quest browser supports WebXR), glasses (stream via browser). TypeScript throughout. Agent highly productive. No app store dependency. Instant updates.
- **Cons:** Camera access is browser-mediated (no native frame processors), ML inference is WebAssembly/WebGPU-bound (slower than native), no local IP detection in browser, file system is IndexedDB (not real FS), PWA install friction on iOS

### D: Web SPA + Capacitor (hybrid)

- **Pros:** Web-first SPA that also ships as native app via Capacitor. Camera via Capacitor plugins (native access). WebXR for VR. One codebase, TypeScript. Capacitor bridges the web-native gap for camera, storage, geolocation.
- **Cons:** Capacitor adds build complexity, plugin ecosystem smaller than React Native, some native features require custom plugin work

## Decision

**Option D: Web SPA + Capacitor.**

The Farm becomes a web-first SPA (TypeScript, Vite, React or similar) that uses Capacitor to ship as a native mobile app with full camera/geolocation/storage access. On VR headsets, it runs as a WebXR-enabled web app in the browser. On desktop, it's a web app.

| Target | How |
|--------|-----|
| iOS / Android | Capacitor-wrapped SPA → App Store / Play Store |
| Web (desktop) | Same SPA, served at farm.ifarm.club |
| VR headsets (Quest) | Same SPA + WebXR, in Quest Browser |
| Glasses (Ray-Ban Meta) | Stream camera to SPA via WebRTC (glasses as camera source) |

### Key Dependencies

| Capability | Library |
|-----------|---------|
| Framework | React (or Preact for smaller bundle) |
| Build | Vite |
| Native bridge | Capacitor |
| Camera (native) | `@capacitor/camera` or custom plugin |
| Camera (web) | `getUserMedia` / MediaStream API |
| Face detection | MediaPipe Face Detection (WebAssembly) or face-api.js (TensorFlow.js) |
| Hand tracking | MediaPipe Hands (WebAssembly) |
| Geolocation | `@capacitor/geolocation` (native) / Geolocation API (web) |
| Local storage | IndexedDB (via idb or Dexie.js) |
| VR/AR | WebXR Device API + Three.js (A-Frame or react-three-fiber) |
| Game engine (particles) | Canvas 2D or WebGL via PixiJS / Three.js |
| State management | Zustand (already in use, works on web) |
| E2E testing | Playwright (already chosen, works natively with web) |

## Rationale

1. **Truly everywhere.** One codebase. Phones get native camera via Capacitor. VR gets WebXR. Desktop gets web. Glasses stream in. No separate clients.

2. **TypeScript throughout.** Agent (OpenCode) is most productive in TS. No new language. Existing shared packages (`@aura/shared`) are already TS — zero migration.

3. **Playwright is native.** E2E tests work directly against the web app — no device emulators, no Expo, no React Native testing friction.

4. **Web APIs are catching up.** WebGPU, WebAssembly, MediaStreamTrackProcessor, and WebCodecs now enable frame-level camera processing in the browser. MediaPipe runs at near-native speed via WASM.

5. **VR is web-native.** WebXR is the standard for browser-based VR. Quest Browser supports it fully. No Unity/Unreal needed.

6. **Capacitor fills the native gap.** Camera, geolocation, file system, and local IP detection (via custom plugin) are available through Capacitor's plugin system. We get native access where the web falls short.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| MediaPipe WASM performance on mobile | Capacitor native camera plugin as fallback for face/hand detection on low-end devices |
| Capacitor plugin gaps | Capacitor's plugin API is straightforward; custom plugins are minimal TypeScript + native stubs |
| WebXR adoption on Quest | Quest Browser has solid WebXR support; test early |
| Ray-Ban Meta has no display | Glasses act as camera source only — Farm UI runs on paired phone or web. Acceptable for v1 |
| PWA install friction on iOS | Capacitor handles App Store distribution; PWA is bonus, not primary |
| Existing React Native Farm code | ~15 commits of Farm code. Rewrite is manageable. Shared packages (`@aura/shared`) are unaffected |

## Consequences

- **Farm codebase rewritten** from React Native to web SPA + Capacitor
- **Card** can also be a web SPA (or share the same SPA with role-based routing) — simplifies the monorepo
- **No Expo, no React Native** — removes native build complexity, Xcode/Android Studio only needed for Capacitor builds
- **Playwright E2E tests** become the primary testing strategy — faster, simpler, no device emulators
- **VR development** becomes a first-class concern — WebXR + Three.js in the same codebase
- **Backend and shared packages** are unaffected — this is a frontend-only pivot

## Migration Path

1. Scaffold new `apps/farm` as Vite + React + Capacitor project
2. Port shared types and state management (Zustand stores) — these are framework-agnostic
3. Implement camera pipeline: Capacitor (native) + MediaStream (web) + MediaPipe (face/hand)
4. Port existing UI components from React Native to React DOM
5. Add WebXR + Three.js for VR particle rendering
6. Remove old React Native Farm code
7. Update CI/CD for web build + Capacitor native builds
