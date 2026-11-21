---
title: "The Fishy Board"
ctf: "MCTF 2026"
date: 2026-11-21
category: forensics
difficulty: medium
points: 937
flag_format: "MCTF26{...}"
---

# The Fishy Board

## Summary

A steganography challenge disguised as a wizard chess service (`ahaz://fishy-board`, port 8000). A hidden `/ai` endpoint takes a base64 list of packed 16-bit chess moves and, for each `turn`, leaks one octal digit of the flag. Grouping three digits per character reveals `MCTF26{S0M3_CH3K3R5}`.

## Solution

### Step 1: Understand the move encoding and find the oracle

Each move is packed as a 16-bit little-endian value:

```
bits 0-3   source file   (fx + 1)
bits 4-7   source rank   (fy + 1)
bits 8-11  target file   (tx + 1)
bits 12-15 target rank   (ty + 1)
```

The list of moves is base64-encoded and sent to `GET /ai?moves=...&turn=t`. Probing with eight moves whose target files are `a`–`h` (arbitrary sources) makes the endpoint return a small integer — one octal digit of the hidden data — for each requested `turn`.

### Step 2: Extract and decode the octal stream

Every three leaked digits form one ASCII character in octal. Sixty turns cover the full 20-character flag; the pattern then repeats.

```python
import base64, struct, requests

BASE = "http://10.240.3.242:8000/ai"

def probe():
    # 8 moves: source (a,1), targets a..h on rank 1
    packed = b"".join(
        struct.pack("<H", 1 | (1 << 4) | ((i + 1) << 8) | (1 << 12))
        for i in range(8)
    )
    return base64.b64encode(packed).decode()

moves = probe()
digits = [
    int(requests.get(BASE, params={"moves": moves, "turn": t}, timeout=8).text.strip())
    for t in range(60)
]
flag = "".join(
    chr(int("".join(map(str, digits[i:i + 3])), 8))
    for i in range(0, len(digits), 3)
)
print(flag)
```

The first triples decode as `1,1,5 → 0o115 → 'M'`, `1,0,3 → 0o103 → 'C'`, `1,2,4 → 0o124 → 'T'`, and so on.

### Step 3: Submit

Submitted via `POST /api/v1/challenges/attempt` for challenge 17; CTFd returned `{"status": "correct"}`.

## Flag

```
MCTF26{S0M3_CH3K3R5}
```
