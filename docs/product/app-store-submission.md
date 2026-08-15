# App Store & Play Store Submission — Prep Guide

> **Status:** Ready for founder action
> **Last updated:** 2026-07-29

## Current State

| Platform | Native Project | Build | Submission Ready |
|----------|---------------|-------|-----------------|
| iOS | ✅ `ios/` created | ❌ Needs Xcode | ❌ |
| Android | ✅ `android/` created | ❌ Needs Android Studio | ❌ |

## Prerequisites (Founder Action Required)

### iOS

1. **Install Xcode** from the Mac App Store (~12 GB download)
   ```bash
   # After install, set the active developer directory:
   sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
   ```
2. **Apple Developer account** ($99/year) at https://developer.apple.com
3. **Create App ID** in Apple Developer portal with bundle ID `club.ifarm.farm`
4. **Generate provisioning profile** for distribution

### Android

1. **Install Android Studio** from https://developer.android.com/studio
2. **Google Play Developer account** ($25 one-time) at https://play.google.com/console
3. **Create app entry** in Play Console with package name `club.ifarm.farm`

## Build Commands (After Prerequisites)

```bash
# Build web assets
cd apps/farm-capacitor && npx vite build

# Sync to native projects
npx cap sync

# iOS: open in Xcode, archive, upload
npx cap open ios

# Android: build APK/AAB
cd android && ./gradlew assembleRelease
```

## App Store Metadata

> **Status:** Copy drafted — ready to paste into App Store Connect / Play Console.
> **Last updated:** 2026-08-15

### App Name

**The Farm by Aura** (subtitle: "Earn your glow.")

### Short Description (≤80 chars)

> Earn your glow. Record real moments and reward the people who made them happen.

*(79 chars)*

### Full Description

**Earn your glow.**

The Farm is where real moments become real reputation. Point your camera at someone doing something worth recognizing — helping set up, nailing a move, making the room laugh — and give them aura. No algorithms, no engagement hacks, no manufactured personas. Just people recognizing people.

**How it works**

1. **Capture** — record a moment with your camera. The Farm tracks movement (hands and full body) and detects gestures in real time, right on your device.
2. **Recognize** — pick who earned it and how much. Every attribution is public and challengeable.
3. **Carry it** — your aura lives on The Card, your membership in the club. Claim points, see your reputation grow, and react to what others earned.

**Built for real life**

- **On-device first** — telemetry is processed locally. You control what's shared.
- **Transparent scoring** — no black boxes. Every point is attributed by someone who was actually there.
- **Community-validated** — others at the same event can confirm or challenge an attribution.
- **Playful, not gamified** — earning aura feels like a high-five that sticks.

Aura is earned, not given. Start farming.

### Keywords (comma-separated)

`aura, reputation, social score, recognition, community, points, moments, real-world, validation, consensus, farm, card, glow`

### Privacy Policy URL

`https://ifarm.club/privacy.html`

### Support URL

`https://ifarm.club/about.html`

### Age Rating

- **iOS:** 4+ (no objectionable content; camera + location disclosed in privacy policy)
- **Android:** PEGI 3 / ESRB E (same rationale)

*Note: user-generated content (attributions, reactions) may warrant a 12+ rating if moderation is not yet live at submission time. Re-evaluate against the final moderation tooling before submitting.*

### Screenshots (6.7" iPhone + 12.9" iPad)

- [ ] Still needed — requires app running on device (founder-gated)

### App Icon

- [x] 1024×1024 PNG — generated from brand SVG, placed in iOS + Android native projects

## Privacy Disclosures

The Farm uses:
- **Camera** — for recording moments
- **Location** — for event geolocation correlation
- **Microphone** — for audio event detection
- **Face data** — processed on-device, never uploaded raw

All telemetry is user-controlled. See `docs/legal/privacy-policy.md`.

## Blockers

1. **Xcode not installed** — iOS build impossible without it
2. **Android Studio not installed** — Android build possible via CLI but untested
3. **No Apple Developer account** — required for App Store submission
4. **No Google Play Developer account** — required for Play Store submission
5. **No app icon** — ✅ generated from brand SVG, placed in iOS + Android native projects
6. **No screenshots** — app needs to be running on device for screenshots

## Next Steps

1. Founder installs Xcode + Android Studio
2. Generate app icon from brand assets
3. Build and test on real devices
4. Prepare store metadata
5. Submit for review
