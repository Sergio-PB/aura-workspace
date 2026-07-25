# ADR-005: Identity Model

Date: 2026-07-25
Status: proposed

## Context

Aura's identity model underpins both products: The Farm attributes points to identities, and The Card lets users claim and carry those points. The identity must be:

- **Unique** — one person, one identity (or at least, one identity per device in MVP)
- **Verifiable** — others at an event can confirm "yes, that's the person I saw"
- **Portable** — reputation follows the user, not the device or platform
- **Privacy-respecting** — users control what's shared, telemetry stays on-device
- **Offline-capable** — identity works without a network (local-first principle)

Constraints:
- Solo founder + agent, no dedicated security team
- MVP ships on mobile (React Native per ADR-002)
- No cloud infrastructure yet
- Must work for single-user mode (P-3) before network features (P-5)

## Options Considered

### A: Self-Sovereign Keypairs (Ed25519)

Generate a cryptographic keypair on-device. The public key IS the identity. The private key proves ownership.

- **Pros:** No central authority, fully offline, privacy-preserving, portable (export/import key), aligns with "fair community" values, can't be deplatformed, no third-party dependency
- **Cons:** Key management UX is hard (users lose keys), no built-in recovery, Sybil resistance is harder (one person can generate many keys), unfamiliar to most users

### B: Email/Phone + Password

Traditional account system. Backend stores hashed credentials.

- **Pros:** Familiar UX, easy recovery flows, simple to implement, rate-limiting per email/phone reduces Sybils
- **Cons:** Requires backend (blocks P-3 offline-first), centralized, phone verification costs money, email verification needs SMTP infra, privacy concerns (backend knows who you are)

### C: OAuth (Google, Apple, GitHub)

Delegate identity to third-party providers.

- **Pros:** No password management, familiar UX, Apple Sign In is privacy-friendly, reduces auth code we write
- **Cons:** Depends on third parties, not offline-first, users can be deplatformed by provider, doesn't align with self-sovereign vision, requires backend for token verification

### D: Hybrid — Keypair Primary, Optional Recovery

Keypair as the root identity. Optional recovery methods (email, social recovery, seed phrase) layered on top.

- **Pros:** Offline-first with keypair, recovery when user opts in, portable, privacy-preserving by default
- **Cons:** Two identity systems to maintain, recovery adds complexity, still need backend for recovery methods

## Decision

**Option D: Hybrid — Ed25519 keypair as primary identity, with optional recovery methods.**

### Rationale

1. **Local-first demands keypairs.** P-3 (Farm core) must work offline. Options B and C require a backend from day one. Keypairs let us ship P-3 without any server.

2. **Privacy-by-design.** The keypair approach means the backend never needs to know who you are — only your public key. Telemetry stays on-device. This is the strongest privacy posture and aligns with Aura's values.

3. **Portable reputation.** Your reputation is tied to your keypair, not to an email address or OAuth provider. Export your key, import it on a new device, and your points follow you.

4. **Recovery is a P-8/P-10 concern.** For MVP (P-3 through P-6), we ship with keypair-only identity and a clear warning: "Lose your key, lose your reputation." Recovery methods (seed phrase, social recovery, optional email binding) are added when we have real users and real feedback.

5. **Sybil resistance is deferred.** One person can generate many keypairs. This is a real problem, but it's a P-8/P-10 problem (community validation, anti-gaming). For the founding community (N-1), we rely on trust and real-world presence. You can't fake being at an event when others are there confirming your identity.

### Implementation

```
Identity = {
  publicKey: Ed25519PublicKey (32 bytes, base58-encoded for display)
  privateKey: Ed25519PrivateKey (64 bytes, stored in device keychain/keystore)
  displayName: string (user-chosen, not unique)
  avatar: optional blob (local until upload)
  createdAt: ISO timestamp
}
```

- Keypair generated on first app launch (Farm or Card)
- Private key stored in platform keychain (iOS Keychain, Android Keystore) — never leaves device
- Public key is the user's visible identifier (e.g., `aura:3xK9...vP2m`)
- Display name is cosmetic only — identity is the public key
- For event attribution: Farm records `{targetPublicKey, points, note, timestamp, location, ip}`
- For claiming: Card presents public key to backend, backend matches attributions

### Recovery (Future)

When recovery is implemented (P-8+):
- **Seed phrase** (BIP-39, 12 words) — generated at key creation, user prompted to back up
- **Social recovery** — designate N trusted contacts who can collectively restore access
- **Optional email binding** — encrypt private key with email-derived key, store on backend

None of these are implemented in MVP. The MVP ships with a single warning screen: "This is your identity. Back up your recovery phrase. If you lose it, your reputation is gone forever."

## Consequences

### Positive
- P-3 (Farm core) can ship without any backend — fully offline
- Strongest privacy posture — backend never sees private keys
- Portable reputation — export/import keypair
- Aligns with self-sovereign, community-governed values
- No third-party dependency for core identity

### Negative
- Key loss = reputation loss (mitigated by recovery in P-8+)
- Sybil attacks possible (mitigated by community validation in P-8, anti-gaming in P-10)
- Unfamiliar UX — users expect "sign in with Google"
- No built-in way to prove "I am the person in this photo" (solved by community confirmation at events)
- Cross-device identity (same person, phone + tablet) requires key export/import or key derivation

### Neutral
- Backend stores only public keys — no PII by default
- Attribution validation uses public key + event metadata, not real-world identity
- Display names are not unique — identity collisions are cosmetic, not security issues

## Alternatives Not Chosen

- **Option A (pure keypairs):** Too risky for real users without any recovery path. The hybrid approach gives us keypairs now and recovery later.
- **Option B (email/phone):** Blocks offline-first. Requires backend infra we don't have. Centralized identity is antithetical to Aura's values.
- **Option C (OAuth):** Fastest to implement but cedes identity control to third parties. Users can be deplatformed. Doesn't work offline.

## References

- ADR-002: Farm Platform (React Native)
- ADR-003: Backend Stack (TypeScript/Hono)
- ADR-004: Database & Sync (SQLite local-first + PostgreSQL backend)
- [Ed25519](https://ed25519.cr.yp.to/) — fast, compact, widely implemented
- [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) — mnemonic seed phrases
- [Keychain Services (iOS)](https://developer.apple.com/documentation/security/keychain_services) / [Android Keystore](https://developer.android.com/training/articles/keystore)
