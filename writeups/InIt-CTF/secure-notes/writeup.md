# InIt CTF — Secure Notes (Android)

- **Category:** Forensics (mobile app data)
- **Artifact:** `~/Downloads/securenotes_data.tar.gz`
- **Scenario:** "Secure Notes" app locked on the device; data folder pulled
  cleanly. Recover the hidden note.

## Flag

```
InIt{s3cur3_n0t3s_n0t_s0_s3cur3}
```

## Solution

```bash
tar xzf securenotes_data.tar.gz
# com.larkfield.securenotes/{shared_prefs,databases,files,cache} + logcat.txt
sqlite3 com.larkfield.securenotes/databases/notes.db "SELECT * FROM notes;"
```

Note #4 **"Recovery Code"** is `is_locked=1` with a garbled body — but the body
bytes start with the gzip magic `1F 8B`. The app "locks" notes by storing the
content as a gzip blob in the TEXT field. No encryption, no key anywhere.

```python
import sqlite3, gzip
con = sqlite3.connect('notes.db')
blob = con.execute("SELECT body FROM notes WHERE _id=4").fetchone()[0]
print(gzip.decompress(blob).decode())
# InIt{s3cur3_n0t3s_n0t_s0_s3cur3}
```

## Decoys

- `shared_prefs` `last_backup_token` → base64 `larkfield-session-not-the-flag`
- Note #3 Wi-Fi password (`welcome2larkfield`), note #5 gym locker combo
- 256-byte `cache/image_cache.tmp` — random bytes, no magic

The biometric/PIN "lock" was bypassed without ever touching the device —
the security was a gzip header away.
