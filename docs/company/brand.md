# Aura — Brand Identity

> **Status:** Draft v1
> **Author:** Aura Agent (autonomous operator)
> **Purpose:** Define the visual and verbal identity of Aura before any product code is written. This document unblocks P-1 architecture decisions by providing brand context.

---

## Brand Essence

**Aura is earned, not given.** Reputation comes from real actions witnessed by real people — not algorithms, not engagement hacks, not manufactured personas. Aura is the glow of genuine recognition.

### Core Values

| Value | What It Means |
|-------|---------------|
| **Authentic** | Points come from real-world actions, not online performance |
| **Transparent** | Every attribution is public and challengeable — no black boxes |
| **Community-driven** | Validation by consensus, not central authority |
| **Privacy-first** | Telemetry processed on-device; users control what's shared |
| **Playful** | Earning aura should feel fun, not gamified — like a high-five that sticks |

### Tone of Voice

- **Warm, not corporate.** We're building community, not enterprise SaaS.
- **Direct, not vague.** "You earned +5 aura for helping set up" — not "Your social capital has increased."
- **Inclusive, not exclusive.** Everyone can earn aura. No clout-chasing.
- **Playful, not silly.** Lighthearted moments (reactions, emoji, quick gestures) but the reputation is real.
- **Confident, not arrogant.** We know what we're building. We don't need to shout about it.

---

## Name & Domain

- **Company:** Aura
- **Domain:** `ifarm.club`
- **Tagline:** "Earn your glow." (working — alternatives: "Real recognition." / "Points that matter.")

The `.club` TLD is intentional — every user is a club member. The Card is their membership. The Farm is where moments are captured.

---

## Visual Identity

### Color Palette

| Role | Hex | Name | Usage |
|------|-----|------|-------|
| **Primary** | `#6C5CE7` | Aura Purple | Brand color, CTAs, active states |
| **Primary Dark** | `#4834D4` | Deep Purple | Hover states, headers |
| **Accent** | `#00D2A0` | Glow Green | Positive actions, earned points, success |
| **Accent Warm** | `#FFA502` | Warm Amber | Highlights, reactions, warmth |
| **Neutral Dark** | `#1E1E2E` | Midnight | Text, dark mode backgrounds |
| **Neutral Mid** | `#6B7280` | Stone | Secondary text, borders |
| **Neutral Light** | `#F3F4F6` | Cloud | Light mode backgrounds, cards |
| **Neutral White** | `#FFFFFF` | White | Surfaces, text on dark |

**Rationale:** Purple conveys creativity, wisdom, and community — not the corporate blue of LinkedIn or the aggressive red of competitive apps. Green signals growth and earned value. Amber adds warmth and human touch.

### Typography

| Role | Font | Style |
|------|------|-------|
| **Display / Logo** | Space Grotesk | Bold, geometric, modern |
| **Headings** | Inter | Semi-bold (600) |
| **Body** | Inter | Regular (400) |
| **Code / Data** | JetBrains Mono | Regular |

**Rationale:** Inter is the most readable UI font, open-source, and works across platforms. Space Grotesk gives the brand a distinctive, slightly playful edge without being unserious. JetBrains Mono for any technical surfaces (admin, telemetry views).

### Logo Concept

**The Aura Mark:** A stylized "A" formed by two overlapping circles — one solid (the individual), one glowing/radiating (their aura). The overlap creates a lens/flare shape suggesting capture and recognition.

```
Concept sketch (ASCII):

     ◯     ← The individual (solid)
   ◌       ← Their aura (radiating, gradient)
    ╲ ╱
     A     ← The overlap forms the letter A
```

**Variations:**
- **Full logo:** Aura Mark + "Aura" wordmark in Space Grotesk Bold
- **Mark only:** For app icons, favicons, Card beacon
- **Wordmark only:** For horizontal layouts, headers

**Colors on mark:**
- Primary: Aura Purple (`#6C5CE7`) for the solid circle
- Gradient: Purple → Glow Green for the radiating circle
- Monochrome versions for dark/light backgrounds

---

## Product Naming

| Product | Name | Metaphor |
|---------|------|----------|
| Media capture app | **The Farm** | Where moments are cultivated and harvested |
| Identity beacon | **The Card** | Your membership — carry your reputation |
| Combined experience | **Aura** | The glow of earned recognition |

---

## Applications

### App Icon (The Farm)
- The Aura Mark on a dark gradient background (Midnight → Deep Purple)
- Subtle glow/radiance effect around the mark
- Rounded square (iOS) / adaptive (Android)

### App Icon (The Card)
- The Aura Mark inverted (light on dark)
- Card-like border treatment
- Smaller, beacon-like presence

### Landing Page (`ifarm.club`)
- Dark theme by default (Midnight background)
- Hero: "Earn your glow." with the Aura Mark
- Two-column: The Farm (capture) + The Card (carry)
- Gradient accents (Purple → Green)
- Minimal, confident, no stock photos

### Social / Sharing
- Share cards: "Sergio earned +5 aura at [event]"
- Purple gradient background, white text, Aura Mark watermark
- Designed for dark mode feeds

---

## Design Principles

1. **Dark-first.** Aura is about real-world moments — the UI should recede, not compete. Dark mode by default.
2. **Glow as feedback.** Positive actions (earning points, confirming attributions) use subtle glow/radiance effects — the "aura" made visible.
3. **Minimal chrome.** The interface is a frame for content, not a dashboard. Less UI, more moments.
4. **Motion with meaning.** Animations signal state changes (point earned, validation confirmed). No decorative motion.
5. **Accessible contrast.** All text meets WCAG AA minimum. Purple on dark passes; green on dark is used sparingly for emphasis.

---

## Competitor Positioning

| | Aura | LinkedIn | BeReal | Strava |
|---|------|----------|--------|--------|
| **Reputation source** | Real-world actions, witnessed | Professional history, self-reported | Unfiltered moments | Athletic performance, GPS data |
| **Validation** | Community consensus | Endorsements (low signal) | Friends only | Verified by GPS |
| **Tone** | Warm, playful, earned | Corporate, aspirational | Raw, unfiltered | Competitive, achievement |
| **Privacy** | On-device first, user-controlled | Data-hungry | Ephemeral | Public by default |

Aura sits at the intersection of **social recognition** (LinkedIn endorsements, but real) and **verified action** (Strava segments, but social). The `.club` TLD and Card identity make it feel like membership, not another profile to maintain.

---

## Next Steps

- [ ] Founder review and approval of brand direction
- [ ] Commission or generate final logo assets (SVG, PNG, app icon sizes)
- [ ] Create Figma/design token file with the color palette and typography
- [ ] Apply brand to landing page at `ifarm.club`
- [ ] Create brand guidelines one-pager for future contributors

---

*This document is a living artifact. As Aura evolves, the brand evolves with it. All changes tracked in git.*
