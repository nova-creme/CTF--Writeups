---
title: "[INTRO] The Apprentice's Cipher"
ctf: "MCTF26"
date: 2026-11-20
category: crypto
difficulty: easy
points: 1000
flag_format: "MCTF26{...}"
---

# [INTRO] The Apprentice's Cipher

## Summary

An interactive three-seal lesson: a Caesar shift (brute force), a Vigenère cipher
with a leaked keyword, and a single-byte XOR broken with the known plaintext prefix
`MCTF26{`. All three answers must be submitted in one cookie-based session.

## Solution

### Step 1: Caesar

Ciphertext: `DLSS ZWBU, HWWYLUAPJL. ...`. Brute-forcing the 26 shifts gives the
plaintext at shift 7:

```
WELL SPUN, APPRENTICE. THE ARCHMAGE LOCKS HIS NEXT SCROLL WITH THE NAME OF HIS FAMILIAR.
```

This reveals the Vigenère keyword: the Archmage's familiar is **QUILL** (also the
signature at the bottom of the notes).

### Step 2: Vigenère

With key `QUILL`, decrypting `JBM XTHLWC CKHM STTYA ...` gives:

```
THE MIRROR RUNE HIDES THE FLAG. REMEMBER, EVERY FLAG BEGINS THE SAME WAY.
```

### Step 3: XOR

The third scroll is hex bytes: `17 19 0e 1c 68 ...`. Since the flag starts with
`MCTF26{`, the key is:

```
key = 0x17 ^ ord('M') = 0x5a
```

XOR-ing every byte with `0x5a` yields `MCTF26{k3ys_m4tt3r_4ppr3nt1c3}`.

```python
import requests
B="http://10.240.19.13:8080"; s=requests.Session()
for answer in [
  "WELL SPUN, APPRENTICE. THE ARCHMAGE LOCKS HIS NEXT SCROLL WITH THE NAME OF HIS FAMILIAR.",
  "THE MIRROR RUNE HIDES THE FLAG. REMEMBER, EVERY FLAG BEGINS THE SAME WAY.",
  "MCTF26{k3ys_m4tt3r_4ppr3nt1c3}",
]:
    print(s.post(B+"/api/check",json={"answer":answer},timeout=10).json())
```

## Flag

```
MCTF26{k3ys_m4tt3r_4ppr3nt1c3}
```
