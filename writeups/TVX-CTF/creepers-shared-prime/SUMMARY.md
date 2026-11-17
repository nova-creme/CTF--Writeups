# Creeper's Shared Prime
* **Platform/Event:** TVX CTF
* **Category:** Crypto (RSA shared prime, 100 pts)
* **Difficulty:** Easy
* **Flag:** `TVXCTF{the_creeper_reused_a_prime}`

## Objective
Decrypt a message encrypted for Vault A given two public keys that were built from the same crafting table.

## Reconnaissance & Methodology
1. Tools used: Python `math.gcd`, `pow(e, -1, ...)`.
2. `public_keys.txt` gives two moduli with `e = 65537`; `ciphertext.txt` gives `c`.
3. The moduli share a prime factor — the "same crafting table" hint.

## Solution & Exploitation
* `p = gcd(nA, nB) = 1393796574908163946345982392040522705234977`; `q = nA // p`; `d = pow(e, -1, (p-1)*(q-1))`; `m = pow(c, d, nA)`.
* Final payload: the full script in `writeup.md` → `TVXCTF{the_creeper_reused_a_prime}`.
