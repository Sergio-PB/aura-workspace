# Aura — Data Retention & Deletion Policy

> **Version:** 1.0
> **Status:** Draft — pending legal review
> **Author:** Aura Agent (autonomous operator)
> **Last updated:** 2026-07-29
>
> This document defines what data Aura retains, for how long, and how deletion works — both user-initiated and automatic. It is the implementation reference for Section 7 of the Privacy Policy.

---

## 1. Data Classification

| Class | Description | Examples |
|-------|-------------|----------|
| **Reputation** | Public, permanent record of a user's actions | Point attributions (claimed), aura score, feed items |
| **Content** | User-generated media and metadata | Recording metadata, face embeddings, geolocation |
| **Identity** | What ties a user to their reputation | Public key, display name, avatar |
| **Operational** | System data needed to run the service | Server logs, rate-limit counters, audit trails |
| **Derived** | Anonymized, aggregated data | Analytics, usage statistics |

---

## 2. Retention Periods

### 2.1 Reputation Data — Indefinite

Point attributions that have been **claimed** by the target user are permanent. This is the user's reputation — the core product. Deleting it would undermine the integrity of the network.

**What's retained:**
- `attributions` rows where `claimed = true`
- Associated `validations` (confirm/challenge records)
- Associated `reactions`

**Rationale:** If Alice earns 500 points and Bob's feed shows Alice at 500, deleting the underlying attribution breaks Bob's view of reality. Reputation is a shared social construct — it can't be unilaterally erased without breaking the network's consistency.

### 2.2 Content Data — User-Controlled + Automatic Fallback

| Data | User-Initiated Deletion | Automatic Deletion |
|------|------------------------|-------------------|
| Recording metadata (unclaimed attributions) | Anytime via "Delete Recording" | 2 years of inactivity |
| Face embeddings | On recording deletion | On recording auto-deletion |
| Geolocation (per-recording) | On recording deletion | On recording auto-deletion |
| IP hash (per-recording) | On recording deletion | On recording auto-deletion |
| Uploaded media (thumbnails, if any) | On recording deletion | On recording auto-deletion |

**Inactivity definition:** No API requests signed by the user's keypair for 730 consecutive days. The user receives an email warning at 30 days and 7 days before auto-deletion (if email is provided).

### 2.3 Identity Data — Until Account Deletion

| Data | Retention |
|------|-----------|
| Public key | Until account deletion |
| Display name | Until account deletion or change |
| Avatar URL | Until account deletion or change |
| Keypair metadata (created_at) | Until account deletion |

### 2.4 Operational Data — Fixed Windows

| Data | Retention | Rationale |
|------|-----------|-----------|
| Server access logs | 90 days | Debugging, security incidents |
| Rate-limit counters | 1 hour (sliding window) | Prevent abuse |
| Audit trail (admin actions) | 1 year | Security, compliance |
| Failed upload queue | 7 days | Give users time to retry |
| SSE connection logs | 24 hours | Debug connection issues |

### 2.5 Derived Data — Indefinite (Anonymized)

Aggregated, anonymized statistics have no retention limit. They contain no personal data and cannot be tied back to individual users.

**Examples:** "42 attributions were created in July 2026," "average points per event: 127."

---

## 3. Deletion Procedures

### 3.1 User-Initiated: Delete Recording

**Trigger:** User taps "Delete" on a recording in The Farm.

**What happens:**
1. Farm sends `DELETE /v1/recordings/:id` signed by the user's keypair
2. Backend verifies the signature matches `recorder_key` on the recording
3. Backend soft-deletes the recording row (`deleted_at = now()`)
4. Associated face embeddings, geolocation, and IP hash rows are soft-deleted
5. Any **unclaimed** attributions from this recording are soft-deleted
6. Any **claimed** attributions are NOT deleted (they're part of the target's reputation)
7. Media files (thumbnails) in object storage are permanently deleted (not soft-deleted)
8. Within 30 days, a background job hard-deletes soft-deleted rows

**Edge case — claimed attributions:** If a recording produced attributions that the target already claimed, those attributions survive. The recording metadata is deleted, but the attribution record remains (with `recording_id` set to null). The target's points are unaffected.

### 3.2 User-Initiated: Delete Account

**Trigger:** User requests account deletion via The Card settings.

**What happens:**
1. User signs a `DELETE /v1/account` request with their private key
2. Backend verifies the signature
3. **Immediate (synchronous):**
   - Display name, avatar URL set to null
   - Public key marked as `deleted` (not removed — needed to verify past signatures)
   - All pending (unclaimed) attributions where user is `target_key` are deleted
   - All pending (unclaimed) attributions where user is `recorder_key` are deleted
   - All validations by this user are anonymized (`validator_key` set to null)
   - All reactions by this user are anonymized (`reactor_key` set to null)
4. **Within 30 days (async job):**
   - All recording metadata where user is `recorder_key` is deleted
   - All face embeddings associated with user's recordings are deleted
   - Media files in object storage are permanently deleted
   - Server logs containing the user's public key are purged (or rotated out naturally within 90 days)
5. **What remains:**
   - Claimed attributions where user is `target_key` — these are part of the network's shared history
   - Claimed attributions where user is `recorder_key` — these are part of the targets' reputations
   - Both are disassociated from the deleted account (display name removed, public key remains as an opaque identifier)

**Rationale for keeping claimed attributions:** If Bob earned 500 points from Alice's recording, and Alice deletes her account, Bob shouldn't lose his reputation. The attribution is part of Bob's record, not Alice's. This is consistent with how social networks handle content — if you delete your account, your comments on others' posts may be anonymized but the posts themselves remain.

### 3.3 Automatic: Inactivity Cleanup

**Trigger:** Cron job runs weekly, checks for users with no API activity in 730 days.

**What happens:**
1. 30 days before deletion: email warning (if email on file)
2. 7 days before deletion: final email warning
3. On deletion day:
   - Same procedure as user-initiated account deletion (Section 3.2)
   - Audit log entry: `AUTO_DELETE_INACTIVITY user=<public_key>`

### 3.4 Automatic: Operational Data Rotation

| Data | Mechanism | Schedule |
|------|-----------|----------|
| Server logs | Log rotation (logrotate or equivalent) | Daily, keep 90 files |
| Rate-limit counters | In-memory, TTL-based | Automatic expiry |
| Audit trail | Partitioned table, drop old partitions | Monthly, keep 12 months |
| Failed upload queue | Database TTL index | Hourly sweep |

---

## 4. Technical Implementation

### 4.1 Soft-Delete Pattern

All user-facing tables use soft-delete:

```sql
ALTER TABLE recordings ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE attributions ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE face_embeddings ADD COLUMN deleted_at TIMESTAMP;
```

Queries filter `WHERE deleted_at IS NULL`. A background job (`cron: hard-delete-sweep`) runs daily and permanently removes rows where `deleted_at < NOW() - INTERVAL '30 days'`.

### 4.2 Anonymization Pattern

For data that must survive but be disassociated:

```sql
-- On account deletion
UPDATE validations SET validator_key = NULL WHERE validator_key = $1;
UPDATE reactions SET reactor_key = NULL WHERE reactor_key = $1;
UPDATE attributions SET recorder_display_name = NULL WHERE recorder_key = $1;
```

The `_key` column is set to null; the row remains for integrity but can't be tied to a user.

### 4.3 Media Deletion

Object storage (Tigris/S3) doesn't support soft-delete. Media files are permanently deleted immediately on recording deletion. A lifecycle policy on the bucket can serve as a safety net:

- **Bucket lifecycle rule:** Delete objects older than 30 days in the `trash/` prefix
- **Implementation:** On recording delete, move objects to `trash/` prefix instead of immediate delete
- **Recovery window:** 30 days to recover accidentally deleted media

### 4.4 Backup Considerations

Database backups (daily, retained 30 days) will contain soft-deleted data. This is acceptable because:

1. Backups are encrypted at rest
2. Backups are for disaster recovery, not operational access
3. After 30 days, hard-deleted data cycles out of backups naturally

If a user exercises their GDPR right to erasure, we must also delete their data from backups. This is handled by:

1. Hard-delete the data immediately (skip the 30-day soft-delete window)
2. Log a `GDPR_ERASURE` audit entry
3. The next backup will not contain the data
4. Previous backups containing the data are not retroactively modified (GDPR allows this — backups are not "filing systems" under Article 2)

---

## 5. GDPR Compliance

### 5.1 Right to Erasure (Article 17)

Users can request full erasure by:
1. Using the in-app "Delete Account" flow (Section 3.2), OR
2. Emailing privacy@ifarm.club with their public key

**Response time:** Within 30 days (GDPR requirement).

**What's different from standard account deletion:** Under GDPR erasure, claimed attributions where the user is `target_key` are ALSO deleted. This goes beyond the standard account deletion flow. The user's reputation is removed from the network.

**Network impact:** Other users' feeds may show inconsistencies (e.g., "Bob had 500 points yesterday, now he has 0"). This is an accepted consequence of GDPR compliance. The alternative — refusing erasure — is not legally viable.

### 5.2 Data Portability (Article 20)

Users can export their data via `GET /v1/account/export`:
- All attributions where user is `recorder_key` or `target_key`
- All validations and reactions
- Account metadata
- Format: JSON (machine-readable, per Article 20)

### 5.3 Data Protection Officer

To be appointed before serving EU users. Contact: dpo@ifarm.club (reserved).

---

## 6. Implementation Checklist

- [ ] Add `deleted_at` columns to: `recordings`, `attributions`, `face_embeddings`
- [ ] Add `anonymize_account(publicKey)` stored procedure
- [ ] Add `DELETE /v1/recordings/:id` endpoint
- [ ] Add `DELETE /v1/account` endpoint
- [ ] Add `GET /v1/account/export` endpoint
- [ ] Add `cron: hard-delete-sweep` (daily)
- [ ] Add `cron: inactivity-check` (weekly)
- [ ] Add `cron: log-rotation` (daily)
- [ ] Add S3 lifecycle policy for `trash/` prefix
- [ ] Add GDPR erasure flow (skip soft-delete window)
- [ ] Add audit log table and write entries for all deletion events
- [ ] Add email notifications for inactivity warnings
- [ ] Update Privacy Policy Section 7 to reference this document

---

## 7. Open Questions

| Question | Status |
|----------|--------|
| Should claimed attributions survive account deletion? | **Decided: Yes** — they're part of the target's reputation, not the recorder's |
| Should GDPR erasure delete claimed attributions? | **Decided: Yes** — Article 17 requires it |
| How long should the soft-delete window be? | **Decided: 30 days** — balances recovery vs. storage |
| Should we notify users when their data is auto-deleted? | **Decided: Yes** — 30-day and 7-day email warnings |
| What happens to attributions from a deleted recording that were already claimed? | **Decided: Survive** — `recording_id` set to null, attribution remains |

---

*This document is version 1.0, prepared for legal review. It has not been reviewed by a privacy lawyer and should not be treated as legal advice. All changes tracked in git.*
