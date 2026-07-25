# Aura Architecture — Fact Index

> One fact per line. Updated as exploration progresses.

## Users & Identity
- Users have two modes: recorder (Farm) and subject (Card). Same person, different contexts.
- Identity = cryptographic keypair generated locally on first launch.
- Identity is tied to IP address — same person on different network = different identity until proven otherwise.

## Visual Input & Gesture Recognition
- Face tracking identifies who is in front of the camera — ties detected face to a Card identity.
- Hand tracking detects gestures and measures movement.
- Visual computing is open source — specific library not yet chosen.
- Move library: named gestures defined by hand movement patterns (e.g., "seesaw" = alternating up/down hands).
- Velocity vectors are measured from hand movement — speed and direction matter.
- Same visual foundation handles both face ID and gesture recognition — one pipeline, two outputs.

## Move Attribution
- A move is notable if it matches a named gesture in the move library.
- No match = no attribution. The library is the gate.

## Stack
- All software is written in TypeScript.
- pnpm is the package manager for all projects.
- E2E testing uses Playwright with natural-language scenario descriptions.
- Monorepo uses pnpm workspaces.
- E2E tests live in a top-level e2e/ directory with scenario-based specs.
