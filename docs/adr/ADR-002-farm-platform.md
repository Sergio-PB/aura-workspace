# ADR-002: Farm Platform

Date: 2026-07-25
Status: proposed

## Context

The Farm is a local media studio app that captures telemetry (IP, geolocation, face detection) from the device camera and lets users attribute "aura points" to people in recordings. It must work offline-first, process data on-device for privacy, and run on both iOS and Android.

Key requirements:
- Real-time camera with frame-level access (for face detection ML)
- GPS/geolocation capture
- Local network IP detection
- Smooth video recording and playback UI
- Local persistent storage for recordings and attributions
- Dark-first UI with glow effects and meaningful motion (per brand identity)
- Offline-first — fully functional without network

Constraints:
- Single developer (founder Sergio) + autonomous agent (Aura Agent via OpenCode)
- No dedicated iOS or Android engineers
- Must ship on both platforms from day one
- Agent-driven development: the coding agent (OpenCode with Caveman model) must be productive in the stack

## Options Considered

### A: Native (Swift + Kotlin)

- **Pros:** Best performance, full API access, best ML integration (CoreML/Vision on iOS, ML Kit on Android), platform-idiomatic UI
- **Cons:** Two completely separate codebases, doubles development and maintenance effort, requires expertise in two languages and ecosystems, agent less productive in Swift/Kotlin than TypeScript

### B: Flutter

- **Pros:** Single codebase, good rendering performance, growing ecosystem
- **Cons:** Dart ecosystem smaller for camera/ML, fewer production-grade camera frame plugins, agent less familiar with Dart, smaller community for troubleshooting

### C: React Native (with Expo)

- **Pros:** Single TypeScript codebase, large ecosystem, production-grade camera (react-native-vision-camera with frame processors), Expo managed workflow reduces build complexity, agent highly productive in TypeScript, large community, shared types with backend (if Node/TS), good ML integration via frame processors + Google ML Kit
- **Cons:** Bridge overhead (mitigated by JSI/Fabric in new architecture), some native modules still require Xcode/Android Studio for custom work, Expo has limitations on very custom native code (ejectable if needed)

### D: Progressive Web App (PWA)

- **Pros:** No app store dependency, instant updates, single web codebase, works everywhere
- **Cons:** Limited camera access (no frame-level processing), no background ML inference, no local IP detection, limited file system, poor offline storage, cannot meet core Farm requirements

## Decision

**React Native with Expo (managed workflow, ejectable if needed).**

The Farm will be built as a React Native app using the Expo framework, with the following key dependencies:

| Capability | Library |
|-----------|---------|
| Camera + frame access | `react-native-vision-camera` v4+ |
| Face detection | `@react-native-ml-kit/face-detection` (via vision-camera frame processor) |
| Geolocation | `expo-location` |
| Local IP | `react-native-network-info` or native module |
| Video recording | `react-native-vision-camera` (built-in) |
| Local storage | `expo-sqlite` (recordings metadata) + file system (video files) |
| UI framework | React Native core + `react-native-reanimated` (glow/motion) |
| Navigation | `expo-router` (file-based routing) |
| State management | Zustand (lightweight, agent-friendly) |

## Rationale

1. **Single codebase, both platforms.** One TypeScript codebase for iOS and Android. Critical for a solo-developer + agent team.

2. **Camera capabilities are sufficient.** `react-native-vision-camera` v4 provides frame-level access via frame processors, enabling on-device face detection without sending data off-device. This satisfies the privacy-by-design requirement.

3. **Agent productivity.** OpenCode (and coding agents generally) are most productive in TypeScript/JavaScript. The ecosystem is well-documented, patterns are well-known, and the agent can generate, test, and iterate quickly.

4. **Shared types with backend.** If the backend is also TypeScript (likely, per future ADR), API contracts, telemetry models, and validation logic can be shared as a monorepo package — reducing duplication and drift.

5. **Expo reduces build friction.** Managed workflow handles signing, builds, and OTA updates. Ejecting to bare workflow is always available if we need custom native modules beyond what Expo supports.

6. **Dark-first UI is natural.** React Native's StyleSheet and `react-native-reanimated` make dark themes, glow effects, and meaningful motion straightforward to implement.

7. **Offline-first is built-in.** SQLite for structured data, file system for media, no network dependency for core flows.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Frame processor performance on older devices | Target ML Kit's face detection (optimized for mobile); fall back to no detection on unsupported devices |
| Expo limitations on custom native code | Start managed, eject if needed; most Farm requirements are covered by existing Expo/RN libraries |
| React Native new architecture instability | Use stable releases; vision-camera v4 already supports Fabric/JSI |
| App Store rejection (camera + ML) | Clear privacy disclosures; on-device processing means no data leaves the device without user action |

## Consequences

- The Farm codebase will live in `aura-apps/apps/farm/` within the monorepo
- All Farm code is TypeScript
- CI/CD must build for both iOS and Android (Expo EAS Build)
- Native module development (if needed) requires Xcode and Android Studio on the dev machine
- The agent can begin P-3 (Farm Core) immediately after P-2 (Dev Infrastructure) is complete
