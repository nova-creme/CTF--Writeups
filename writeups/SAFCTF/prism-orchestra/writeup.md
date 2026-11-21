# SAFCTF — Prism Orchestra

- **Category:** Binary side-channel (ltrace)
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `safctf{MVRKQ2APHL7WPM78}`

## Objective

Recover a 24-character receipt from a local binary whose length check rejects ordinary input.

## Solution path

1. Observed that direct execution failed an immediate length check.
2. Used a Python driver with `ltrace` to instrument the binary and map its internal permutation cipher.
3. Tracked `memcmp` output while mutating input bytes to learn which positions affected which compared bytes.
4. Reconstructed the exact 24-character receipt and submitted it to the challenge API for the flag.

## Result

`safctf{MVRKQ2APHL7WPM78}`

## Key lesson

A comparison oracle plus a deterministic permutation leaks the expected input byte-by-byte; `ltrace` is enough when source is unavailable.
