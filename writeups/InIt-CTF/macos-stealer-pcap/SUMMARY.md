# macOS Infostealer PCAP
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Forensics (network / exfil reconstruction)
* **Difficulty:** Medium
* **Flag:** `InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}`

## Objective
Reconstruct an infostealer's exfiltration from `~/Downloads/capture.zip` → `capture.pcap` (77 KB) and recover the flag. A "cracked" app on `MARCUS-MBP` (user `mreid`) beaconed to a fake iCloud host over plaintext HTTP.

## Reconnaissance & Methodology
1. Tools used: `tshark` (`--export-objects http`), DNS/HTTP conversation analysis, Python (join chunks by `id`, base64 decode, unzip).
2. DNS showed `update.icloud-sync.cc` → `185.199.111.153`; 116 HTTP POSTs to `/api/collect` (decoys to `example.com` / `www.apple.com`).
3. Each POST body is a JSON chunk `{"id": 35, "part": "..."}`; sorted by `id`, the `part` values concatenate to base64 → a ZIP archive.
4. Exfil contents included `system_profiler.txt` (macOS 15.2, M1 Pro, serial `C02G8140Q6L7`), a `keychain_dump.txt`, `TCC.db`, finder plist and Safari history.

## Solution & Exploitation
* Inside `keychain_dump.txt`, a generic-password item named `backup-key` held base64 `SW5JdHtrM3ljaDRpbl9jcnVtYnNfbDM0azNkXzB2M3JfcGw0MW5faHR0cH0=`.
* Final payload: base64-decode → `InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}`.
* IR follow-up: rotate GitHub/ProtonMail/iCloud credentials; block `update.icloud-sync.cc` at the egress firewall. The operators shipped their own secret in the clear.
