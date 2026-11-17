# InIt CTF — Tanvoro Deleted Evidence

- **Category:** Forensics (NTFS deleted-file recovery)
- **Artifact:** `~/Downloads/evidence.img` (12 MB, MBR, one NTFS partition)
- **Scenario:** Exfiltration from a developer workstation at 02:14 Sunday;
  attacker deleted files afterwards. "Delete doesn't mean erased — it just
  means forgotten."

## Flag

```
InIt{d3l3t3d_but_n0t_g0n3}
```

## Solution

```bash
mmls evidence.img                        # partition at sector 2048, volume "RECOVERY"
fls -r -p -o 2048 evidence.img           # one deleted entry marked '*':
#   -/r * 75-128-2: Users/j.morris/Documents/recovery_code.gz
icat -o 2048 evidence.img 75 > recovery_code.gz
zcat recovery_code.gz                    # VaVg{q3y3g3q_ohg_a0g_t0a3}
```

The recovered string is ROT13 on letters (digits untouched): `VaVg` → `InIt`
confirmed the encoding against the known flag prefix.

| Cipher | Plain |
|--------|-------|
| `q3y3g3q` | `d3l3t3d` |
| `ohg` | `but` |
| `a0g` | `n0t` |
| `t0a3` | `g0n3` |

## Notes

- Live files were decoys: `todo.txt` (shopping list), `wifi_backup.txt`
  (`bXktd2lmaS1wYXNzd29yZA==` → `my-wifi-password`), `report_q3.txt`.
- The `rm`'d gzip survived intact in unallocated space — MFT entry 75 still
  pointed at its clusters.
