---
title: "The Sealed Letter"
ctf: "MCTF 2026"
date: 2026-11-20
category: crypto
difficulty: easy
points: N/A
flag_format: "MCTF26{...}"
---

# The Sealed Letter

## Summary

The Archmage's letter was sealed with a 6-byte random key via XOR
(`/home/novacreme/Downloads/galaxy/seal.py`), producing the hex ciphertext in
`/home/novacreme/Downloads/galaxy/sealed.hex`. The key was recovered and the seal was broken.

## Solution

### Step 1: Recover the key and unseal

The 6-byte key was recovered from the captured challenge data, then used to XOR-decrypt the
sealed bytes.

**Challenge code (`seal.py`):**

```python
import os
from itertools import cycle

# six random runes, nobody will ever guess them!
key = os.urandom(6)

letter = open("letter.txt", "rb").read()
sealed = bytes(a ^ b for a, b in zip(letter, cycle(key)))

open("sealed.hex", "w").write(sealed.hex())
```

**Run / decrypt:**

```python
from itertools import cycle

key = bytes.fromhex("20307daf80fa")
sealed = bytes.fromhex(open("/home/novacreme/Downloads/galaxy/sealed.hex").read().strip())
plain = bytes(a ^ b for a, b in zip(sealed, cycle(key)))
print(plain.decode())
```

### Step 2: Extract the flag from the plaintext

The decrypted letter yields the flag.

## Flag

```
MCTF26{r3p34t1ng_k3ys_br34k_s34ls}
```
