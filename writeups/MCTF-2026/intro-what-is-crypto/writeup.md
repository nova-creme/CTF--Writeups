---
title: "[INTRO] What Is Crypto?"
ctf: "MCTF 2026"
date: 2026-11-20
category: crypto
difficulty: easy
points: 1000
flag_format: "MCTF26{...}"
---

# [INTRO] What Is Crypto?

## Summary

Introductory cryptography lesson (Quill the owl / "New to cryptography? Start here,
apprentice!") — a browser-based cipher desk with four seals. Each seal hides a scroll
that must be decoded by recognizing an encoding, and every broken seal reveals the next
seal and a slice of the final flag.

**Flag: `MCTF26{3nc0d1ng_1s_n0t_3ncrypt10n_w1z4rd}`**

## Solution

### Recon

The lesson instance was served at `http://10.240.6.63:8080` ("Cipher Desk"). The frontend
fetched `/static/app.js`, which revealed three stage tools (cipher wheel, Vigenère
keyword wheel, XOR calculator) plus the API surface:

- `POST /api/reset` — start over from the first seal
- `GET /api/state` — current seal, scroll, hints, progress, done list, finale
- `POST /api/check` — submit the decoded answer (`{"answer": "..."}`)

### Seal 1 — Numbers

Scroll: `116 104 101 32 111 119 108 32 115 101 101 115 32 97 108 108` (decimal ASCII
codes). Decode with `chr()`:

```python
s = "116 104 101 32 111 119 108 32 115 101 101 115 32 97 108 108"
answer = "".join(chr(int(n)) for n in s.split())
print(answer)  # -> "the owl sees all"
```

Submitted via `curl -X POST http://10.240.6.63:8080/api/check -H 'Content-Type: application/json' -d '{"answer":"the owl sees all"}'` → `{"message":"The seal breaks!","ok":true}`

Flag fragment: `MCTF26{3nc0`

### Seal 2 — Hex

Scroll: `69 6e 6b 20 6f 66 20 73 69 78 74 65 65 6e 20 72 75 6e 65 73` (hex pairs).
Decode with `bytes.fromhex`:

```python
s = "696e6b206f66207369787465656e2072756e6573"
answer = bytes.fromhex(s).decode()
print(answer)  # -> "ink of sixteen runes"
```

Submitted via `/api/check` → `{"message":"The seal breaks!","ok":true}`

Flag fragment: `d1ng_1s_n0t`

### Seal 3 — Base64

Scroll: `cGFkZGluZyBpcyBhIHRlbGwsIGFwcHJlbnRpY2U=` (Base64, ends with padding `=`).

```python
import base64
answer = base64.b64decode("cGFkZGluZyBpcyBhIHRlbGwsIGFwcHJlbnRpY2U=").decode()
print(answer)  # -> "padding is a tell, apprentice"
```

Submitted via `/api/check` → `{"message":"The seal breaks!","ok":true}`

Flag fragment: `_3ncrypt10n`

### Seal 4 — Layers

Scroll was encoded **three times over** (Base64 → hex → Base64):

```python
import base64

scroll = "NWE1NzM1NmE2MjMyNTI3MDYyNmQ0MzY3NjE1ODRkNjc2MjZkMzkzMDQ5NDc1Njc1NTkzMzRhMzU2MzQ4NTI3MDYyMzIzNDNk"
layer1 = base64.b64decode(scroll).decode()          # -> hex string
layer2 = bytes.fromhex(layer1).decode()             # -> base64 string
answer = base64.b64decode(layer2).decode()         # -> plain text
print(answer)                                        # -> "encoding is not encryption"
```

Submitted via `/api/check` with `{"answer":"encoding is not encryption"}` →
`{"message":"The seal breaks!","ok":true}`

Flag fragment: `_w1z4rd}`

### Finale

All four seals broken; the finale assembles the flag:

```
MCTF26{3nc0d1ng_1s_n0t_3ncrypt10n_w1z4rd}
```

## Flag

```
MCTF26{3nc0d1ng_1s_n0t_3ncrypt10n_w1z4rd}
```
