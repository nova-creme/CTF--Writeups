# Ghosty note (GhostNote)
* **Platform/Event:** TVX CTF
* **Category:** Forensics / DFIR (endpoint exfiltration + PE reversing)
* **Difficulty:** Hard
* **Flag:** `Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}`

## Objective
Explain how a senior employee's confidential notes appeared outside the organisation **with no anomalous cloud logins**, and recover the exfiltration C2 and flag from the workstation triage package (`GhostNote.zip`).

## Reconnaissance & Methodology
1. Mapped the package: `Sysmon.xml` (EID 1 + 3), `ExecutionArtifacts.csv`, `NotionUpdate.exe` (6656 B, unsigned), `vault.db` (SQLite), `NTUSER.DAT.reg` (UTF-16LE), plus two decoys.
2. Tools used: `strings`, SQLite (`sqlite3`/Python), `base64`, a PE disassembler/decompiler, Python `hashlib`; `reproduce/solve.py` regenerates the flag end-to-end.
3. Sysmon EID 1 showed `Notion.exe` spawning `NotionUpdate.exe --silent-sync` under `CORP\john`; EID 3 showed outbound TCP to `104.21.52.117:8443`. Because the implant ran under the victim's own process/token, no cloud login anomaly appeared — exfil was via the **endpoint**.
4. `vault.db`: `identity.deviceSecret` base64-decodes to exactly **32 bytes** (the hash key); `config.serverValidation` is a built-in oracle; notes are ordinary.
5. Registry `HKCU\...\Explorer\SessionInfo\SyncProfile = GNT-0926` (timestamp 21:42:12 aligns with the beacon) supplies the campaign profile.
6. Reversed the 12 `GhostNote_*` PE exports: `decodeServer` = XOR `0x37` → 3 candidate C2 URLs; `deriveSession` = `SHA256(key ‖ host)`; `validationDigest` = `SHA256(key ‖ "GHOSTNOTE")`; `finalFlagDigest` = `SHA256(key ‖ host ‖ profile)`.

## Solution & Exploitation
* Decoys: `vpn_backup.conf` → `some_fake_token`; the root-CA comment is actually the intended hint — "THE IDENTITY OPENS THE DOOR, BUT THE PROFILE NAMES THE CALPAIGN" — i.e. key from the vault, profile from the registry.
* Validate each host: `SHA256(SHA256(secret ‖ host) ‖ "GHOSTNOTE") == serverValidation`. Only **`sync-notes-service.cloud`** matches (corroborated by Sysmon → `104.21.52.117:8443`); the other two hosts fail.
* Final deduction: `digest = SHA256(session ‖ host ‖ profile)`; flag = first **40 hex chars** of the digest → `Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}`.
* Reproduce with `reproduce/solve.py`; `reproduce/candidates.py` and the disassembly/source files document the reverse engineering.
