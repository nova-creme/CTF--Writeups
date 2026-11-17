# Careless Twins (RSA shared prime)
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Crypto (RSA key-generation failure)
* **Difficulty:** Medium
* **Flag:** `InIt{n3v3r_r3us3_pr1m3s_1n_rs4}`

## Objective
Recover the flag from two "military-grade" 2048-bit RSA public keys and one ciphertext, given `~/Downloads/careless.zip` (`encryption.py`, `output.txt`). "Their custom prime generator isn't as random as they think."

## Reconnaissance & Methodology
1. Tools used: Python `math.gcd` and modular inverse (`pow(e, -1, ...)`) — the `sympy`/`Crypto` libraries aren't even needed.
2. Code review of `encryption.py`: `n1 = p * q1` and `n2 = p * q2` — **both moduli reuse the same prime `p`**; `c1 = pow(m, e, n1)`.
3. Red herrings noted: `random.seed(1337)` ("static entropy") and an unused `base = random.getrandbits(1024)` push toward a PRNG-prediction attack that isn't needed.

## Solution & Exploitation
* Batch-GCD attack: `p = gcd(n1, n2)` (a 1024-bit hit) factors both moduli instantly; `q1 = n1 // p`.
* Final payload: `d = pow(e, -1, (p-1)*(q1-1)); m = pow(c1, d, n1)` → `InIt{n3v3r_r3us3_pr1m3s_1n_rs4}`.
* Lesson: a 2048-bit modulus sharing a prime is weaker than a 512-bit independent one — this is the real-world Lenstra/Debian weak-key class of failure.
