# The Multi-Prime Seal
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Crypto (RSA reuse)
* **Difficulty:** Medium
* **Flag:** `MCTF26{R0ll1ng_my_0wn_crypt0_t0t13ns_fru5tr4_5un7}`

## Objective
`task.py` encrypts a flag with three related moduli — `n1 = a²·b²·c`, `n2 = a·c`, `n3 = b·a` —
using `e = 65537`, i.e. a common-prime (RSA reuse) setup.

## Reconnaissance & Methodology
1. Step 1: Factor via shared primes
2. Step 2: Decrypt

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{R0ll1ng_my_0wn_crypt0_t0t13ns_fru5tr4_5un7}`
