---
title: "The Multi-Prime Seal"
ctf: "MCTF 2026"
date: 2026-11-20
category: crypto
difficulty: medium
points: N/A
flag_format: "MCTF26{...}"
---

# The Multi-Prime Seal

## Summary

`task.py` encrypts a flag with three related moduli — `n1 = a²·b²·c`, `n2 = a·c`, `n3 = b·a` —
using `e = 65537`, i.e. a common-prime (RSA reuse) setup.

## Solution

### Step 1: Factor via shared primes

Because the moduli share prime factors, `gcd` operations expose the underlying primes; the
full factorization recovers `a`, `b` and `c`.

### Step 2: Decrypt

Compute the totient of `n1` (`phi = a(a-1)·b(b-1)·(c-1)`) and derive the private exponent
`d = e⁻¹ mod phi(n1)`. Decrypt `ct1 = pow(m, e, n1)` to obtain the flag message.

**Challenge code (`task.py`):**

```python
import os

from Crypto.Util.number import bytes_to_long, getPrime

a, b, c = [getPrime(512) for _ in range(3)]

n1 = a * a * b * b * c
n2 = a * c
n3 = b * a

flag = os.environ.get("FLAG", "flag{test_flag_for_testing}")

e = 0x10001
ct1 = pow(bytes_to_long(flag.encode()), e, n1)
ct2 = pow(bytes_to_long(b"Hello, my old chum, please check the message I sent you using the most secure key.".encode()), e, n2)
ct3 = pow(bytes_to_long(b"It is done, the witching hour will come soon enough..".encode()), e, n3)

print(f"{e = }")
print(f"{n1 = }")
print(f"{n2 = }")
print(f"{n3 = }")
print()
print(f"{ct1 = }")
print(f"{ct2 = }")
print(f"{ct3 = }")
```

**Decrypt:**

```python
from Crypto.Util.number import long_to_bytes

d = pow(e, -1, (a * (a - 1)) * (b * (b - 1)) * (c - 1))   # e = 65537
m = pow(ct1, d, n1)
flag = long_to_bytes(m).decode()
```

## Flag

```
MCTF26{R0ll1ng_my_0wn_crypt0_t0t13ns_fru5tr4_5un7}
```
