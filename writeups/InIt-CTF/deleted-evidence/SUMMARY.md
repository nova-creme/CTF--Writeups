# Tanvoro Deleted Evidence
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Forensics (NTFS deleted-file recovery)
* **Difficulty:** Easy
* **Flag:** `InIt{d3l3t3d_but_n0t_g0n3}`

## Objective
Recover an exfiltrated recovery code from `~/Downloads/evidence.img` (12 MB MBR image, one NTFS volume "RECOVERY") after the attacker deleted the files. "Delete doesn't mean erased — it just means forgotten."

## Reconnaissance & Methodology
1. `mmls evidence.img` located the NTFS partition at sector 2048.
2. Tools used: Sleuth Kit (`mmls`, `fls`, `icat`), `gzip`/`zcat`, ROT13 decoding.
3. `fls -r -p -o 2048 evidence.img` listed one deleted entry (`*`): `Users/j.morris/Documents/recovery_code.gz` at MFT inode 75 — the deleted gzip survived intact in unallocated space.
4. `icat -o 2048 evidence.img 75 > recovery_code.gz; zcat` revealed `VaVg{q3y3g3q_ohg_a0g_t0a3}`.

## Solution & Exploitation
* `VaVg` → `InIt` confirmed ROT13-on-letters (digits untouched) against the known flag prefix.
* ROT13 mapping: `q3y3g3q`→`d3l3t3d`, `ohg`→`but`, `a0g`→`n0t`, `t0a3`→`g0n3`.
* Decoys skipped: live `todo.txt`, `wifi_backup.txt` (`bXktd2lmaS1wYXNzd29yZA==` → `my-wifi-password`), `report_q3.txt`.
* Final payload: `InIt{d3l3t3d_but_n0t_g0n3}`.
