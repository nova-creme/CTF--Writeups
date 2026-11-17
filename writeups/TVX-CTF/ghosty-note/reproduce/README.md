# TVX CTF — Ghosty note

**Category:** Forensics / DFIR
**Flag:** `Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}`

## Scenario

A senior employee's confidential meeting notes (`vault.db` notes table) started
showing up outside the org. No suspicious cloud logins — the workstation triage
package (`GhostNote.zip`) contains the answer.

## Evidence

```
Evidence/Sysmon.xml                 EventID 1 + 3: NotionUpdate.exe run by Notion.exe
                                    (--silent-sync), then TCP 104.21.52.117:8443
Timeline/ExecutionArtifacts.csv     Prefetch/Amcache: unsigned, first run 21:39:44Z
Users/john/AppData/Local/NotionUpdate/NotionUpdate.exe
Users/john/AppData/Roaming/Notion/vault.db
Users/john/NTUSER.DAT.reg           (UTF-16LE)
Users/john/Desktop/vpn_backup.conf  decoy
Users/john/Desktop/company-root-ca.pem  decoy (comment = hint)
```

Decoys first:

* `vpn_backup.conf` → `Token = c29tZV9mYWtlX3Rva2Vu` = `some_fake_token`.
* `company-root-ca.pem` trailing comment is Base64:
  `VEhFIElERU5USVRZIE9QRU5TIFRIRSBET09SLCBCVVQgVEhFIFBST0ZJTEUgTkFNRVMgVEhFIENBTFBBSUdOLg==`
  → **"THE IDENTITY OPENS THE DOOR, BUT THE PROFILE NAMES THE CALPAIGN."**
  (sic — "CALPAIGN" is a typo in the challenge itself)
  i.e. the device secret is the key, the registry `SyncProfile` is a flag input.

## 1. Vault secrets

```sql
sqlite> .schema
CREATE TABLE identity (name TEXT PRIMARY KEY, secret TEXT NOT NULL);
CREATE TABLE config (name TEXT PRIMARY KEY, value TEXT NOT NULL);
...
sqlite> select * from identity;
deviceSecret|eiHYlLXXBMofKkmAhk5S3n+VjdOfjNMjIvfFaA/Y9L0=
sqlite> select * from config;
serverValidation|2be46ca73aacd65f76539df5d2157357d44bf060736cc92e457642daad0be83c
```

`base64 -d` of the device secret is exactly **32 bytes** — a hash key.

## 2. Registry profile

`NTUSER.DAT.reg` (decode as UTF-16LE) holds:

```
[HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo]
"SyncProfile"="GNT-0926"
```

## 3. NotionUpdate.exe

The PE has no `main` (entry point is an infinite junk loop) but exports 12
symbols, and the `--silent-sync` binary is really a helper library:

| Export | Behaviour |
| --- | --- |
| `GhostNote_decodeServer` | XOR each byte with `0x37` |
| `GhostNote_getC2` | returns one of **three** embedded URL strings |
| `GhostNote_extractHostLower` | strips `scheme://`, port, path; lowercases |
| `GhostNote_deriveSession` | `SHA256(key[32] ‖ string)` |
| `GhostNote_validationDigest` | `SHA256(key[32] ‖ "GHOSTNOTE")` |
| `GhostNote_finalFlagDigest` | `SHA256(key[32] ‖ str1 ‖ str2)` |

Decoding the three `.rdata` blob groups (`0x2000`, `0x2030`, `0x2060`) with
XOR 0x37:

```
0  wss://notion-assets-cdn.com:9443/update
1  wss://SYNC-NOTES-SERVICE.CLOUD:8443/api/v2
2  wss://notes-edge-cache.net:443/sync
```

Only one is the real C2. `deriveSession` + `validationDigest` is a built-in
oracle: the session key derived with the correct host, tagged with the
`GHOSTNOTE` validation tag, must reproduce the `serverValidation` value in
`vault.db`.

```python
session = sha256(secret_raw + host).digest()
sha256(session + b"GHOSTNOTE").hexdigest()
# host = sync-notes-service.cloud
# -> 2be46ca73aacd65f76539df5d2157357d44bf060736cc92e457642daad0be83c  == vault.db
```

`notion-assets-cdn.com` and `notes-edge-cache.net` do **not** validate, so the
exfil channel is `wss://sync-notes-service.cloud:8443/api/v2`.

## 4. Flag

The last exported routine hashes the session key plus the two campaign strings —
the validated C2 host and the registry profile — and the flag is the first
40 hex characters (20 bytes) of that digest:

```python
session = sha256(secret + b"sync-notes-service.cloud").digest()
digest  = sha256(session + b"sync-notes-service.cloud" + b"GNT-0926").hexdigest()
# 665504d169ef04e47fb9b8f7a9b5bfbe97277dc9050ff0284174f51f0e762efd
flag = "Tvx{" + digest[:40] + "}"
```

```
Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}
```

## What happened

A fake "Notion update" (`NotionUpdate.exe`, dropped in `%LOCALAPPDATA%`,
parent `Notion.exe`, unsigned, observed by Prefetch/Amcache) is a GhostNote
sync implant. It pulls the device identity + campaign profile from the local
Notion vault and `HKCU\...\SessionInfo`, derives a per-session key against its
C2 host, and beacons over WSS to `sync-notes-service.cloud:8443/api/v2`
(Sysmon EID 3 to 104.21.52.117:8443). Because it reuses the victim's own
process and token there is no anomalous cloud authentication — the notes left
through the endpoint, not through the account.

Reproduce with `python3 solve.py`.
