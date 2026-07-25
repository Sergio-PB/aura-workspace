# Aura — Privacy Policy (Draft v1)

> **Status:** Draft — not yet legally reviewed
> **Author:** Aura Agent (autonomous operator)
> **Purpose:** Define how Aura handles user data. This is a working draft to be reviewed by a privacy lawyer before going live.

---

## 1. Our Privacy Philosophy

Aura is built on the principle that **your data is yours**. We process telemetry on your device, not on our servers. You control what's shared, with whom, and for how long. We don't sell data. We don't build advertising profiles. We don't optimize for engagement.

This policy explains what data we collect, why we collect it, and what control you have over it.

---

## 2. What Data We Collect

### 2.1 Data That Stays On Your Device (Not Sent to Aura)

| Data Type | Purpose | Shared? |
|-----------|---------|---------|
| Camera feed / media recordings | Capturing moments for aura attribution | Only if you explicitly upload |
| Face detection data | Identifying people in recordings for point attribution | Only if you explicitly upload |
| Geolocation (GPS) | Correlating recordings with events and other attendees | Only if you explicitly upload |
| IP address (local) | Device identification within local network | Only if you explicitly upload |
| Bluetooth proximity | Same-room detection for multi-device correlation | Only if you explicitly enable |

**Key point:** The Farm processes all telemetry on-device. Nothing leaves your device until you choose to upload a recording for aura point attribution.

### 2.2 Data Sent to Aura Servers (When You Upload)

| Data Type | Purpose | Retention |
|-----------|---------|-----------|
| Recording metadata (timestamp, geolocation, IP) | Validating attributions, correlating with other attendees | Until you delete the recording or your account |
| Face recognition embeddings (not raw images) | Matching faces across recordings for attribution | Until you delete the recording or your account |
| Aura point attributions (who, what, how many points) | Building your reputation score and feed | Indefinitely (this is your public reputation) |
| Your identity (public key, display name, avatar) | Identifying you on the network | Until account deletion |

### 2.3 Data We Never Collect

- Raw video/audio recordings (processed on-device; only metadata and embeddings are uploaded)
- Contacts or address book
- Browsing history
- Messages or DMs (Aura doesn't have DMs)
- Health data
- Financial information (except for payment processing, handled by a third-party processor)

---

## 3. How We Use Your Data

| Purpose | Data Used | Legal Basis |
|---------|-----------|-------------|
| Attributing aura points to the right person | Face embeddings, geolocation, timestamps | Legitimate interest (core service functionality) |
| Validating attributions via community consensus | Recording metadata, validator identities | Legitimate interest (core service functionality) |
| Displaying your reputation (aura score, feed) | Point attributions, display name, avatar | Consent (you choose what to upload and claim) |
| Improving the service (analytics, debugging) | Anonymized usage patterns | Legitimate interest |
| Legal compliance | Any data, as required by law | Legal obligation |

**We do not:**
- Sell your data to third parties
- Use your data for advertising
- Build shadow profiles or infer interests
- Share your data with data brokers

---

## 4. Your Control & Rights

### 4.1 Before Upload
- You choose which recordings to upload
- You choose which telemetry fields to include (geolocation, face data, etc.)
- You can preview and edit attributions before they're sent

### 4.2 After Upload
- **Delete:** You can delete any recording you've uploaded. Associated metadata and embeddings are removed.
- **Correct:** You can challenge or correct attributions made about you.
- **Export:** You can export your full aura history (all points earned, all recordings you uploaded).
- **Portability:** Your reputation data is portable. You can export your keypair and point history.
- **Account deletion:** Deleting your account removes your profile, display name, and avatar. Point attributions you made about others remain (they're part of *their* reputation), but are anonymized.

### 4.3 GDPR Rights (EU/UK Users)

You have the right to:
- Access your data
- Rectify inaccurate data
- Erase your data ("right to be forgotten")
- Restrict processing
- Data portability
- Object to processing

To exercise any of these rights, contact privacy@ifarm.club. We respond within 30 days.

---

## 5. Data Sharing & Third Parties

| Recipient | What | Why |
|-----------|------|-----|
| Other Aura users | Your display name, avatar, aura score, and feed items you've claimed | This is the product — your reputation is visible to the community |
| Event attendees | Recording metadata (for validation) | Community consensus requires transparency about who attributed what |
| Payment processor (TBD) | Payment details | If Aura ever processes payments |
| Law enforcement | As required by valid legal process | Legal obligation |

**No other sharing.** Period.

---

## 6. Data Security

- **Encryption in transit:** All communication between Farm/Card and Aura servers uses TLS 1.3+.
- **Encryption at rest:** Server-side data is encrypted at rest.
- **On-device security:** Telemetry is processed locally. Raw media never leaves your device.
- **Key-based identity:** Your identity is a cryptographic keypair, not an email/password. No password database to leak.
- **Access control:** Minimal server-side access. Automated systems process data; humans access only for debugging with audit logging.

---

## 7. Data Retention

| Data | Retention Period |
|------|-----------------|
| Recordings (metadata + embeddings) | Until you delete, or 2 years of inactivity |
| Point attributions (your reputation) | Indefinitely (this is your permanent record) |
| Account data (profile, keypair) | Until account deletion |
| Anonymized analytics | Indefinitely |
| Server logs | 90 days |

---

## 8. Children's Privacy

Aura is not intended for users under 13 (or the applicable age of digital consent in your jurisdiction). We do not knowingly collect data from children. If you believe a child has provided data, contact us immediately.

---

## 9. International Data Transfers

Aura servers may be located in the United States or other jurisdictions. By using Aura, you consent to data transfer to these locations. We ensure appropriate safeguards (Standard Contractual Clauses or equivalent) for transfers from the EU/UK.

---

## 10. Changes to This Policy

We will notify users of material changes via:
- In-app notification (The Farm / The Card)
- Email (if provided)
- 30-day notice before changes take effect

Continued use after changes constitutes acceptance.

---

## 11. Contact

- **Email:** privacy@ifarm.club
- **Data Protection Officer:** To be appointed before public launch
- **EU Representative:** To be appointed before serving EU users

---

## Appendix A: Biometric Data Notice

Aura processes face recognition embeddings, which may be considered biometric data under some laws (e.g., Illinois BIPA, GDPR). Key facts:

1. **On-device processing:** Face detection and embedding generation happen entirely on your device. Raw face images are never uploaded.
2. **Consent:** You must explicitly enable face recognition. It is off by default.
3. **Purpose-limited:** Embeddings are used solely for matching faces across recordings to attribute aura points. They are not used for identification, surveillance, or any other purpose.
4. **Deletion:** Deleting a recording deletes its associated embeddings.
5. **No sale:** Biometric data is never sold, leased, or traded.

---

*This document is a draft. It has not been reviewed by a privacy lawyer and should not be considered final legal advice. All changes tracked in git.*
