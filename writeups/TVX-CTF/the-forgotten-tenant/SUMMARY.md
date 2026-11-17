# The Forgotten Tenant
* **Platform/Event:** TVX CTF
* **Category:** Cloud (AWS / CloudTrail forensics, Stage 3)
* **Difficulty:** Medium
* **Flag:** `TVX{Cl0ud_s3cur1ty}`

## Objective
A Q4-2024 migration left an AWS tenant alive (account `400875701859`, `us-east-1`). Given two static CloudTrail day-exports and a handoff note, reconstruct the original responders' access path, work out the exact S3 key of `evidence.json`, and retrieve the flag from the live environment.

## Reconnaissance & Methodology
1. Unpacked `forgotten-tenant-stage3-bundle.zip`: `cloudtrail-2026-03-14.json`, `cloudtrail-2026-03-15.json`, `incident-handoff-note.txt`, `README.txt`.
2. Tools used: `jq`/text search on CloudTrail JSON, AWS CLI (`aws s3 ls`, `aws sts assume-role`, `aws s3 cp`), plus the one-shot bash repro in the detailed writeup §6.
3. Two buckets: migration archive (contains the `sts:ExternalId`) and the private forensics bucket (holds `evidence.json`). Two roles: `legacy-migration-role` and `incident-response-role`.
4. Day 1: a failed `unknown-caller` `AssumeRole` leaked the trust condition `sts:ExternalId`; the player then assumed the legacy role and chained to the IR role; `s3:CreateMultipartUpload` fixed the case folder as **`case-ab5396cd`**. A `GetObject` of `evidence.json` at the bucket root returned `NoSuchKey`.
5. Day 2: the trail was mid-migration and recorded keys **relative to the upload sub-path only** — `handoff-RYII91T48V/evidence.json`. A repeat read without the case folder returned `AccessDenied` (object exists, key wrong).
6. Handoff note: "stitch the 03-14 case folder together with the 03-15 handoff sub-path."

## Solution & Exploitation
* Stitch the key: `case-ab5396cd` + `/` + `handoff-RYII91T48V/evidence.json` → `s3://tvx-forgotten-tenant-forensics-pro0hid4/case-ab5396cd/handoff-RYII91T48V/evidence.json`.
* Role chain: player user → enumerate archive for `ExternalId` → `sts:AssumeRole legacy-migration-role --external-id <id>` → `sts:AssumeRole incident-response-role` → `s3:GetObject` on the stitched key.
* `NoSuchKey` vs `AccessDenied` is the discriminator between "wrong path" and "wrong prefix, object exists"; the failed external attempt is an oracle revealing the ExternalId trust condition.
* Final payload: the one-shot script in `writeup.md` §6; `evidence.json` yields `TVX{Cl0ud_s3cur1ty}`.
