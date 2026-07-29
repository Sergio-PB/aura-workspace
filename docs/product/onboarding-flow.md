# Aura — Onboarding Flow

> **Status:** Draft v1
> **Author:** Aura Agent
> **Audience:** Product design, engineering
> **Purpose:** Define the end-to-end onboarding experience for new Aura users across The Farm and The Card.

---

## Design Principles

1. **Progressive disclosure.** Don't explain everything upfront. Show features as they become relevant.
2. **Value in 60 seconds.** A new user should understand what Aura is and why it matters within a minute of opening the app.
3. **No account required to explore.** Let people see what Aura is before committing to an identity.
4. **Keypair-first, not email-first.** Identity is cryptographic. The onboarding must make this feel natural, not scary.
5. **Single flow for both products.** The Farm and The Card are two sides of the same coin. Onboarding should introduce both without forcing a choice.

---

## Flow Overview

```
Download → Splash/Welcome → Identity Creation → Profile Setup → Product Tour → First Action → Home
```

Each step is skippable where noted. Users can return to any step later.

---

## Step 1: Splash & Welcome (3 screens, ~30 seconds)

### Screen 1: Logo + Tagline
- Aura logo animation
- Tagline: "Real reputation. Earned in person."
- Auto-advances after 2 seconds or tap to skip

### Screen 2: What Is Aura?
- Three illustrated cards (swipeable):
  1. **Capture moments** — Record people doing something notable with The Farm
  2. **Earn recognition** — Get aura points when others recognize you
  3. **Build real reputation** — Your score reflects what you actually did, with real people
- "Next" button

### Screen 3: How It Works
- Simple 3-step visual:
  1. 📸 Record → 2. ⬆️ Attribute points → 3. ✅ Community confirms
- "That's it. No algorithms. No bots. Just people."
- "Get Started" button

**Skip:** Entire welcome flow is skippable via "Skip" in corner.

---

## Step 2: Identity Creation (2 screens, ~45 seconds)

This is the most critical step. Users must understand that their identity is a keypair, not a password.

### Screen 1: Your Identity
- Headline: "Your identity is a key, not a password"
- Plain-language explanation:
  - "Aura creates a unique digital key on your device. It proves you're you — no email, no password, no phone number."
  - "Your key lives on your device. Lose your device without a backup = lose access. We can't recover it."
- Visual: Simple key icon generating on device
- "Create My Key" button

### Screen 2: Key Generated + Backup Prompt
- Animation: Key generated successfully
- "Your key is ready. Save a backup now?"
- Options:
  - **"Back up to iCloud/Google Drive"** (recommended) — encrypted backup
  - **"Show recovery phrase"** — 12-word BIP39 phrase, with standard "write it down, don't screenshot" warnings
  - **"Skip for now"** — with warning: "You'll be reminded later. Don't lose your device."
- "Continue" button

**Skip:** Backup can be skipped (with warning). Key creation cannot.

---

## Step 3: Profile Setup (2 screens, ~30 seconds)

### Screen 1: Who Are You?
- Display name field (required, 2-50 chars)
- Avatar: camera or photo library picker (optional, defaults to generated identicon from public key)
- "Next"

### Screen 2: Your First Aura Card
- Preview of what others will see: avatar, display name, aura score (0, with "Just getting started" label)
- "This is your Card. It's what people see when they attribute points to you or look you up."
- "You can customize it more later."
- "Finish Setup" button

**Skip:** Entire profile step is skippable (defaults: "User_[random]" display name, generated identicon).

---

## Step 4: Product Tour (2 screens, ~30 seconds)

Introduce both products without forcing a choice.

### Screen 1: The Farm
- Icon + headline: "The Farm — Capture the moment"
- "Record people doing something notable. The Farm captures who was there, when, and where."
- "You attribute aura points. The community confirms they're real."
- Visual: Mockup of Farm recording UI
- "Got it"

### Screen 2: The Card
- Icon + headline: "The Card — Carry your reputation"
- "When someone gives you points, they appear here. Claim them, build your score, see your feed."
- "Your Card is your identity on the network. Share it, protect it, be proud of it."
- Visual: Mockup of Card feed
- "Got it"

**Skip:** Entire tour is skippable.

---

## Step 5: First Action (contextual, ~30 seconds)

The first action depends on context. If the user was invited to an event, guide them there. Otherwise, show both options.

### Option A: "Find an event near you"
- If location permissions granted: show nearby public events
- If not: prompt for location permission with clear value prop ("See events happening around you")
- If no events nearby: "No events yet? Start one or invite friends."

### Option B: "Explore a demo"
- Pre-loaded demo event with sample attributions
- Lets user see what a populated feed looks like
- "This is what your feed will look like when you start using Aura at real events."

### Option C: "Invite friends"
- Share link / QR code
- "Aura works best with people you know. Invite friends to your first event."

**Skip:** Skippable. User lands on home screen.

---

## Step 6: Home

User lands on a contextual home screen:

- **If they have no events and no points:** Empty state with clear CTA: "Join an event or invite friends to get started."
- **If they have pending attributions:** Highlighted: "You have 3 points to claim!"
- **If they're at an active event:** Farm recording UI is the default view.

---

## Empty States (Post-Onboarding)

Every empty state is an opportunity, not a dead end.

| Screen | Empty State | CTA |
|--------|-------------|-----|
| Feed | "No points yet. Join an event or explore a demo." | "Explore Demo" / "Find Events" |
| Events | "No events. Start one or get invited." | "Create Event" / "Invite Friends" |
| Profile | "Your reputation starts here." | "Share Your Card" |
| Farm (recording) | "Point your camera at someone doing something notable." | (camera viewfinder is the CTA) |

---

## Permission Prompts

All permission prompts are deferred until needed, with clear value props:

| Permission | When Asked | Value Prop |
|------------|------------|------------|
| Camera | First time opening Farm recording | "The Farm uses your camera to capture moments. Nothing is recorded until you press record." |
| Microphone | First recording | "Record audio to capture the moment. Audio stays on your device." |
| Location | Joining or browsing events | "See events happening near you. Your location never leaves your device until you join an event." |
| Notifications | After first attribution received | "Get notified when someone gives you points or invites you to an event." |
| Bluetooth | First multi-device event | "Find other Aura users nearby for better event matching." |

---

## Recovery Flows

### "I lost my device"
- If they backed up: "Restore from backup" on welcome screen
- If they didn't: "Create new identity" — old points are lost (they're tied to the old keypair)

### "I forgot I have an account"
- "Already have an account?" link on welcome screen
- Restore from iCloud/Google Drive backup or enter recovery phrase

---

## What We Skip (For Now)

- **Email/phone verification.** Keypair is identity. No email needed.
- **Interest/preference selection.** Not relevant to the product.
- **Friend suggestions from contacts.** Privacy-first. No contact scraping.
- **Tutorial overlay on every feature.** Progressive disclosure: explain features when they're first encountered.
- **Gamification of onboarding.** No "complete your profile to earn points" — that's the kind of manufactured engagement Aura rejects.

---

## Metrics

Track these, not vanity metrics:

| Metric | Why |
|--------|-----|
| % who complete key creation | Is the keypair concept landing? |
| % who back up their key | Are people protecting their identity? |
| % who perform first action (record or claim) | Did they get value? |
| Time to first action | Is onboarding too long? |
| % who return within 7 days | Did onboarding lead to retention? |
| Drop-off per step | Where are we losing people? |

---

*This is a design document, not a spec. It will evolve based on user testing and feedback during N-1 (founding community) before N-2 (public beta).*
