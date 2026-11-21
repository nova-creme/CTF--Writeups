# [INTRO] The Apprentice's Cipher
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Crypto (Caesar / Vigenère / XOR)
* **Difficulty:** Easy
* **Flag:** `MCTF26{k3ys_m4tt3r_4ppr3nt1c3}`

## Objective
An interactive three-seal lesson: a Caesar shift (brute force), a Vigenère cipher
with a leaked keyword, and a single-byte XOR broken with the known plaintext prefix
`MCTF26{`. All three answers must be submitted in one cookie-based session.

## Reconnaissance & Methodology
1. Step 1: Caesar
2. Step 2: Vigenère
3. Step 3: XOR

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{k3ys_m4tt3r_4ppr3nt1c3}`
