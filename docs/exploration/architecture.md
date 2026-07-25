# Aura Architecture — Exploration

> Q&A format. New facts marked `<new fact>..</new fact>`. Each section ends with a question.

---

## 1. Users & Identity

**Q: Who are the users?**

A: Two roles — people recording moments (Farm users) and people receiving points (Card holders). Same person can be both.

<new fact>Users have two modes: recorder (Farm) and subject (Card). Same person, different contexts.</new fact>

**Q: How does a user prove who they are?**

A: The Card is an identification beacon. It uniquely identifies a user + their IP. Cryptographic keypair generated on-device.

<new fact>Identity = cryptographic keypair generated locally on first launch.</new fact>
<new fact>Identity is tied to IP address — same person on different network = different identity until proven otherwise.</new fact>

**Q: Can one person have multiple devices?**

A: Not yet answered.

**Q: Is identity portable across devices?**

A: Not yet answered.

**Q: What happens when IP changes (mobile, travel, VPN)?**

A: Not yet answered.

---

**→ Next question:** How does a Farm instance know which Card holder is in front of the camera?

---

## 2. Visual Input & Gesture Recognition

**Q: How does a Farm instance know which Card holder is in front of the camera?**

A: Visual computing — face and hand tracking. Open source library, specific choice TBD. Same foundation reads hand movement and matches it against a "move" library (e.g., "seesaw" = alternating up/down hands), measuring velocity vectors.

<new fact>Face tracking identifies who is in front of the camera — ties detected face to a Card identity.</new fact>
<new fact>Hand tracking detects gestures and measures movement.</new fact>
<new fact>Visual computing is open source — specific library not yet chosen.</new fact>
<new fact>Move library: named gestures defined by hand movement patterns (e.g., "seesaw" = alternating up/down hands).</new fact>
<new fact>Velocity vectors are measured from hand movement — speed and direction matter.</new fact>
<new fact>Same visual foundation handles both face ID and gesture recognition — one pipeline, two outputs.</new fact>

**Q: How does a detected face map to a specific Card identity?**

A: Not yet answered.

**Q: Is the move library pre-defined (shipped with the app) or user-created?**

A: Not yet answered.

---

**→ Next question:** How does the Farm decide which move is "notable" enough to attribute aura points?

---

## 3. Move Attribution

**Q: How does the Farm decide which move is "notable" enough to attribute aura points?**

A: If the detected gesture pattern matches an entry in the move library, it's notable.

<new fact>A move is notable if it matches a named gesture in the move library.</new fact>
<new fact>No match = no attribution. The library is the gate.</new fact>

**Q: Who defines the move library? Shipped with the app, or user-created?**

A: Not yet answered.

**Q: Can users create custom moves?**

A: Not yet answered.

---

**→ Next question:** What happens after a move is detected — how does the Farm attribute aura points to a specific Card holder?

---

## 4. Particle Generation & UI

**Q: What happens after a move is detected — how does the Farm attribute aura points to a specific Card holder?**

A: Moves act like a particle generator — a "spell" that stays active as long as the move is detected. Each particle generated is attributed to the user performing the move. Example: Bob swings his hands in a seesaw pattern and earns 2 aura per second. The UI renders particles on top of the camera feed using a game engine.

<new fact>Move = particle generator ("spell"). Active while the gesture is continuously detected.</new fact>
<new fact>Each particle = aura points attributed to the user performing the move.</new fact>
<new fact>Points are earned per time unit while the move is active (e.g., 2 aura/second for seesaw).</new fact>
<new fact>UI renders particles as a visual overlay on the camera feed using a game engine.</new fact>
<new fact>The game engine is responsible for particle rendering — not the visual computing pipeline.</new fact>
<new fact>All UI is mobile-first.</new fact>
<new fact>All UI supports light/dark theme via a configurable flag.</new fact>

**Q: What game engine? 2D canvas, WebGL, something else?**

A: Not yet answered.

**Q: Are particles purely visual, or do they carry data (point value, move type, timestamp)?**

A: Not yet answered.

---

**→ Next question:** After particles are generated locally, how do they become recorded aura points — what's the upload flow from Farm to backend?
