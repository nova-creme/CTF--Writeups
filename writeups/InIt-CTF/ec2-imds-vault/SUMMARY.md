# EC2 IMDS Vault
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Forensics (cloud IR / key derivation)
* **Difficulty:** Medium
* **Flag:** `InIt{imds_k3y3d_s3cr3t_v4ult}`

## Objective
Decrypt `vault.bin` from an unauthorised cron script on a compromised EC2 instance. The AES key isn't on disk — it's derived at runtime from the instance's own identity.

## Reconnaissance & Methodology
1. Unpacked `~/Downloads/incident_ec2.zip`: `INCIDENT.txt`, `agent/vault.py`, `agent/vault.bin`, `artifacts/` logs.
2. Tools used: Python `hashlib` + `pycryptodome` (`Crypto.Cipher.AES`), CloudTrail/cloud-init log review.
3. Code review of `vault.py`: `key = sha256("s4lt_" + instance_id)`, AES-256-CBC with the IV prepended to the ciphertext, PKCS#7 padding stripped manually. The IMDS cache `instance-id.cache` was missing — the identity had to come from logs.
4. `artifacts/cloud-init-output.log` printed `instance-id: i-0a1b2c3d4e5f67890` at boot.
5. Timeline corroboration: 02:14:07 SSH login from `203.0.113.44`; 02:15:51 `sudo mkdir -p /opt/agent`; 02:16:03 vault loaded (v2), cron `*/5 * * * *`.

## Solution & Exploitation
* Derive `key = SHA256("s4lt_" + "i-0a1b2c3d4e5f67890")`; decrypt `blob[16:]` with `iv = blob[:16]`; strip PKCS#7.
* Final payload: decrypted JSON `{"config_version":2,...,"operator_note":"InIt{imds_k3y3d_s3cr3t_v4ult}"}`.
* Lesson: a key "derived from instance identity" is only as secret as the boot logs that print that identity — cloud-init output is an IR goldmine.
