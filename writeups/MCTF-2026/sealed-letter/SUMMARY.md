# The Sealed Letter
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Crypto (repeating-key XOR)
* **Difficulty:** Easy
* **Flag:** `MCTF26{r3p34t1ng_k3ys_br34k_s34ls}`

## Objective
The Archmage's letter was sealed with a 6-byte random key via XOR
(`/home/novacreme/Downloads/galaxy/seal.py`), producing the hex ciphertext in
`/home/novacreme/Downloads/galaxy/sealed.hex`. The key was recovered and the seal was broken.

## Reconnaissance & Methodology
1. Step 1: Recover the key and unseal
2. Step 2: Extract the flag from the plaintext

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{r3p34t1ng_k3ys_br34k_s34ls}`
