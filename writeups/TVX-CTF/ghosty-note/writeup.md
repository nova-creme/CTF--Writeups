# TVX CTF — Ghosty note (GhostNote)

- **Category:** Forensics / DFIR
- **Artifact:** `GhostNote.zip` (`sha256 8d4f5e1b676012e77e254576159f7759f290303df5094d1a7a6ab88eae0442c3`)
- **Scenario:** A senior employee's confidential meeting notes were appearing
  outside the organization, but no suspicious authentication activity was seen
  in the employee's cloud accounts. A triage package was pulled from the
  workstation.
- **Flag:** `Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}`

---

## 1. Triage package layout

```
GhostNote/
├── Evidence/Sysmon.xml                      EventID 1 (process) + 3 (network)
├── Timeline/ExecutionArtifacts.csv          Prefetch / Amcache / Registry
└── Users/john/
    ├── AppData/Local/NotionUpdate/NotionUpdate.exe   suspect binary (6656 B)
    ├── AppData/Roaming/Notion/vault.db               SQLite (notes + secrets)
    ├── Desktop/company-root-ca.pem                   decoy (hint in comment)
    ├── Desktop/vpn_backup.conf                       decoy
    └── NTUSER.DAT.reg                                registry export (UTF-16LE)
```

**Sysmon (the only execution/network evidence):**

```
EID 1  2026-08-18T21:39:44.172Z
  Image       C:\Users\john\AppData\Local\NotionUpdate\NotionUpdate.exe
  ParentImage C:\Program Files\Notion\Notion.exe
  CommandLine "...\NotionUpdate.exe" --silent-sync
  User        CORP\john
  SHA256      3D84616670CDBE3EABC870B5E732BF4EDE26966179BA39F874E67CF1EA2ACBDA

EID 3  2026-08-18T21:42:18.940Z
  Image C:\Users\john\AppData\Local\NotionUpdate\NotionUpdate.exe
  DestinationIp 104.21.52.117   DestinationPort 8443   Protocol tcp   Initiated true
```

A binary masquerading as a Notion updater (`--silent-sync`) is spawned by the
real `Notion.exe`, runs unsigned, and beacons outbound to `104.21.52.117:8443`.
Because it runs **as the user's own process with the user's token**, no anomalous
cloud login ever appears — the notes left through the *endpoint*, not the account.

## 2. The vault (`vault.db`)

```sql
CREATE TABLE identity (name TEXT PRIMARY KEY, secret TEXT NOT NULL);
CREATE TABLE config   (name TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE notes    (id INTEGER PRIMARY KEY, title TEXT, body TEXT, classification);

identity: deviceSecret | eiHYlLXXBMofKkmAhk5S3n+VjdOfjNMjIvfFaA/Y9L0=
config  : serverValidation | 2be46ca73aacd65f76539df5d2157357d44bf060736cc92e457642daad0be83c
notes   : "Q3 Board Meeting" (Confidential), "Budget Review", "Travel"
```

`base64 -d` of `deviceSecret` is exactly **32 bytes** — a hash key:

```
7a21d894b5d704ca1f2a4980864e52de7f958dd39f8cd32322f7c5680fd8f4bd
```

## 3. The registry profile (`NTUSER.DAT.reg`, UTF-16LE)

```
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo]
"LastSync"="2026-08-18T21:42:12Z"
"SyncProfile"="GNT-0926"
"ThemeState"="system"
```

The `SessionInfo` update at `21:42:12` (per `ExecutionArtifacts.csv`) lines up
with the implant's beacon window.

## 4. Decoys

* `vpn_backup.conf` → `Token = c29tZV9mYWtlX3Rva2Vu` = **`some_fake_token`**.
* `company-root-ca.pem` → trailing comment is Base64:
  `VEhFIElERU5USVRZIE9QRU5TIFRIRSBET09SLCBCVVQgVEhFIFBST0ZJTEUgTkFNRVMgVEhFIENBTFBBSUdOLg==`
  → **"THE IDENTITY OPENS THE DOOR, BUT THE PROFILE NAMES THE CALPAIGN."**
  (sic — "CALPAIGN" is a typo in the challenge). Meaning: the `deviceSecret`
  from the vault is the *key*, and the registry `SyncProfile` is a *flag input*.

## 5. Reversing `NotionUpdate.exe`

The PE has no `main` (its entry point is an infinite junk loop) but exports
twelve symbols that document the implant's crypto:

```
GhostNote_vaultPath          GhostNote_identityQuery     (SELECT secret FROM identity ...)
GhostNote_profilePath        GhostNote_validationQuery   (SELECT value FROM config ...)
GhostNote_decodeServer       GhostNote_getC2
GhostNote_extractHostLower   GhostNote_deriveSession
GhostNote_validationTag      GhostNote_validationDigest
GhostNote_profileValue       GhostNote_finalFlagDigest
```

`GhostNote_decodeServer` is `XOR 0x37`. Decoding the `.rdata` string groups
yields **three** candidate C2 URLs:

```
0  wss://notion-assets-cdn.com:9443/update
1  wss://SYNC-NOTES-SERVICE.CLOUD:8443/api/v2
2  wss://notes-edge-cache.net:443/sync
```

`GhostNote_extractHostLower` strips `scheme://`, port and path and lowercases,
so the candidate hosts are `notion-assets-cdn.com`,
`sync-notes-service.cloud`, `notes-edge-cache.net`.

### Crypto, confirmed from the disassembly

* `deriveSession(key32, str)` (`RVA 0x1110`): hashes the 32-byte key then `str`
  → `SHA256(key ‖ str)`.
* `validationDigest(key32)` (`RVA 0x1350`): hashes the 32-byte key then the
  9-byte constant at RVA `0x223a` (`"GHOSTNOTE"`) → `SHA256(key ‖ "GHOSTNOTE")`.
* `finalFlagDigest(key32, str1, str2)` (`RVA 0x1480`): hashes key, then `str1`,
  then `str2` → `SHA256(key ‖ str1 ‖ str2)`.

The vault's `serverValidation` is a **built-in oracle**: the session key derived
against the *correct* host, tagged with `GHOSTNOTE`, must reproduce it.

## 6. Solve

```python
import base64, hashlib, sqlite3

secret = base64.b64decode(open_secret_b64)              # 32 bytes
profile = "GNT-0926"                                    # NTUSER.DAT.reg
server_validation = "2be46ca7...0be83c"                 # vault.db config

candidates = [
    "notion-assets-cdn.com",
    "sync-notes-service.cloud",
    "notes-edge-cache.net",
]

for host in candidates:
    session = hashlib.sha256(secret + host.encode()).digest()
    if hashlib.sha256(session + b"GHOSTNOTE").hexdigest() == server_validation:
        # finalFlagDigest(session, host, profile)
        digest = hashlib.sha256(session + host.encode() + profile.encode()).hexdigest()
        print("Tvx{%s}" % digest[:40])
```

```
notion-assets-cdn.com     -> no match
sync-notes-service.cloud  -> MATCH  (== vault.db serverValidation)
notes-edge-cache.net      -> no match

final digest: 665504d169ef04e47fb9b8f7a9b5bfbe97277dc9050ff0284174f51f0e762efd
```

The flag is the first 40 hex characters (20 bytes) of the final digest:

```
Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}
```

## 7. What happened

A fake "Notion update" (`NotionUpdate.exe`, dropped in `%LOCALAPPDATA%`, parent
`Notion.exe`, unsigned) is a **GhostNote** sync implant. It pulls the device
identity from the local Notion vault and the campaign profile from
`HKCU\...\Explorer\SessionInfo`, derives a per-session key against its C2 host,
and exfiltrates the notes over WSS to `sync-notes-service.cloud:8443/api/v2`
(Sysmon EID 3 → `104.21.52.117:8443`). Reusing the victim's own process and
token is why no anomalous cloud authentication was logged.

## 8. Indicators of compromise

```
Host              : CORP workstation, user john
Implant           : C:\Users\john\AppData\Local\NotionUpdate\NotionUpdate.exe
Implant SHA-256   : 3d84616670cdbe3eabc870b5e732bf4ede26966179ba39f874e67cf1ea2acbda
Command line      : "NotionUpdate.exe" --silent-sync
Parent            : C:\Program Files\Notion\Notion.exe
C2 (validated)    : wss://sync-notes-service.cloud:8443/api/v2  (104.21.52.117:8443)
Decoy C2 hosts    : notion-assets-cdn.com:9443, notes-edge-cache.net:443
Looted source     : %APPDATA%\Notion\vault.db (notes) + HKCU SessionInfo profile
Registry artifact : HKCU\...\Explorer\SessionInfo\SyncProfile = GNT-0926
Key material      : vault.db identity.deviceSecret (32-byte hash key)
```
