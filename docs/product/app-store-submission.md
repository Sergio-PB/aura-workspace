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

## App Store Metadata Needed

- [ ] App name: "The Farm by Aura"
- [ ] Short description (80 chars max)
- [ ] Full description
- [ ] Keywords
- [ ] Screenshots (6.7" iPhone + 12.9" iPad)
- [ ] App icon (1024x1024 PNG)
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Age rating questionnaire

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
5. **No app icon** — brand assets exist but no app icon generated
6. **No screenshots** — app needs to be running on device for screenshots

## Next Steps

1. Founder installs Xcode + Android Studio
2. Generate app icon from brand assets
3. Build and test on real devices
4. Prepare store metadata
5. Submit for review
