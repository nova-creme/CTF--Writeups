# Secure Notes (Android)
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Forensics (mobile / Android app data)
* **Difficulty:** Easy
* **Flag:** `InIt{s3cur3_n0t3s_n0t_s0_s3cur3}`

## Objective
Recover a hidden, "locked" note from a pulled data directory (`~/Downloads/securenotes_data.tar.gz`) of the Secure Notes Android app.

## Reconnaissance & Methodology
1. Extracted the tarball: `com.larkfield.securenotes/{shared_prefs,databases,files,cache}` plus `logcat.txt`.
2. Tools used: `tar`, `sqlite3`, Python `sqlite3` + `gzip`; `xxd`/magic-byte inspection.
3. `notes.db` table `notes` showed note #4 "Recovery Code" with `is_locked=1` and a garbled body — but the bytes begin with the gzip magic `1F 8B`.
4. The app only **compresses** locked-note content into the SQLite TEXT field — no encryption, no key anywhere on the device.

## Solution & Exploitation
* Final payload: `gzip.decompress(blob).decode()` on the note #4 body → `InIt{s3cur3_n0t3s_n0t_s0_s3cur3}`.
* Decoys: `shared_prefs` `last_backup_token` → `larkfield-session-not-the-flag`; note #3 Wi-Fi password; note #5 gym combo; random 256-byte `cache/image_cache.tmp`.
* The biometric/PIN "lock" was bypassed offline — the security was a gzip header away.
