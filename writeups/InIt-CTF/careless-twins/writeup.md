# InIt CTF — Careless Twins (RSA shared prime)

- **Category:** Crypto (RSA keygen failure)
- **Artifact:** `~/Downloads/careless.zip` → `encryption.py`, `output.txt`
- **Scenario:** Two syndicate servers with "military-grade" 2048-bit RSA.
  Both public keys + one encrypted message captured. "Their custom prime
  generator isn't as random as they think." Challenge name: *Careless Twins*.

## Flag

```
InIt{n3v3r_r3us3_pr1m3s_1n_rs4}
```

## Solution

**1. Code review** (`encryption.py`) — the smoking gun:

```python
def get_secure_prime():
    random.seed(1337)                      # "static entropy" — red herring
    base = random.getrandbits(1024)
    return getPrime(1024)                  # base never actually used

# Server A
p  = getPrime(1024); q1 = getPrime(1024); n1 = p * q1

# Server B — "They generated a new q, but reused the same session state for p!"
q2 = getPrime(1024); n2 = p * q2

m = bytes_to_long(flag)
c1 = pow(m, e, n1)
```

Both moduli share the prime `p`. The seeded "extra entropy" is a decoy —
the actual bug is prime reuse across the two keypairs.

**2. Batch-GCD attack:**

```python
from math import gcd
p = gcd(n1, n2)            # 1024-bit hit — both keys fall instantly
q1 = n1 // p
d1 = pow(e, -1, (p-1)*(q1-1))
m = pow(c1, d1, n1)
# InIt{n3v3r_r3us3_pr1m3s_1n_rs4}
```

No 2048-bit factoring required — a single GCD factors both moduli.

## Lessons

- **Shared primes are fatal.** Any two RSA moduli that share a factor are
  broken by `gcd(n1, n2)` — this is the batch-GCD attack that hit real-world
  RSA keys in 2012 (Debian weak keys, Lenstra et al.).
- Crypto strength comes from **independent entropy per key**, not from key
  size alone. A 2048-bit modulus sharing a prime is weaker than a 512-bit one.
- Red herrings: the hardcoded `random.seed(1337)` and unused `base` variable
  push you toward a PRNG-prediction attack; the real bug is simpler.
