# Prism Orchestra
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Binary side-channel (ltrace)
* **Difficulty:** Not recorded
* **Flag:** `safctf{MVRKQ2APHL7WPM78}`

## Objective
Recover a 24-character receipt from a local binary whose length check rejects ordinary input.

## Reconnaissance & Methodology
1. Observed that direct execution failed an immediate length check.
2. Used a Python driver with `ltrace` to instrument the binary and map its internal permutation cipher.
3. Tracked `memcmp` output while mutating input bytes to learn which positions affected which compared bytes.
4. Reconstructed the exact 24-character receipt and submitted it to the challenge API for the flag.

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `safctf{MVRKQ2APHL7WPM78}`
