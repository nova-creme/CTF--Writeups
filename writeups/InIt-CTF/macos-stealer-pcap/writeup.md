# InIt CTF — macOS Infostealer PCAP

- **Category:** Forensics (network / exfil reconstruction)
- **Artifact:** `~/Downloads/capture.zip` → `capture.pcap` (77 KB)
- **Scenario:** "Cracked" app installed from an unofficial mirror → infostealer
  on a MacBook (user `mreid`, MARCUS-MBP) beaconing to a host posing as iCloud.
  Everything tunneled over plaintext HTTP.

## Flag

```
InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}
```

## Solution

**1. C2 identification** — DNS shows `update.icloud-sync.cc` → `185.199.111.153`;
116 HTTP POSTs to `/api/collect`. Decoy traffic to `example.com` / `www.apple.com`.

**2. Exfil protocol** — each POST body is a JSON chunk:

```json
{"id": 35, "part": "HpBYkpGUWBQvIB7vFgEWyC/OrACJeuaFZJbkpC5i477EzsHJ"}
```

Reassemble:

```bash
tshark -r capture.pcap --export-objects http,httpobjs
python3 - # join parts by "id" order → base64 → ZIP
unzip exfil.bin
```

**3. Exfiltrated contents** (`exfil/`):

| Item | Contents |
|------|----------|
| `system_profiler.txt` | macOS 15.2 (24C101), MacBookPro18,3 / M1 Pro, serial `C02G8140Q6L7`, MARCUS-MBP, user `mreid` |
| `Library/Keychains/keychain_dump.txt` | GitHub `mreid`/`hunter2!`, ProtonMail `m.reid`/`Tr0ub4dour&3`, iCloud recovery phrase, backup-key, Wi-Fi |
| `TCC.db` | privacy permissions DB |
| `com.apple.finder.plist`, `Safari/browsing_data.json` | prefs + history |

**4. The leaked secret** — inside `keychain_dump.txt`, a generic-password item
named `backup-key` holds a base64 string:

```
SW5JdHtrM3ljaDRpbl9jcnVtYnNfbDM0azNkXzB2M3JfcGw0MW5faHR0cH0=
→ InIt{k3ych4in_crumbs_l34k3d_0v3r_pl41n_http}
```

The stealer harvested credentials, then shipped the operators' own secret
over plaintext HTTP — nobody vetted the stash in transit.

**IR follow-up:** rotate GitHub, ProtonMail, iCloud credentials; hunt for
`update.icloud-sync.cc` at the egress firewall.
