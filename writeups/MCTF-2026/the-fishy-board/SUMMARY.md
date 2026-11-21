# The Fishy Board
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Stego (hidden chess AI oracle)
* **Difficulty:** Medium
* **Flag:** `MCTF26{S0M3_CH3K3R5}`

## Objective
A wizard chess service hides the flag in a `/ai` endpoint that leaks one octal digit per `turn` when probed with a crafted list of packed moves.

## Reconnaissance & Methodology
1. Found the hidden `/ai` endpoint on the chess service (`ahaz://fishy-board`, port 8000).
2. Reversed the move format: each move is a 16-bit little-endian value with 1-based source/target file and rank in four nibbles.
3. Sent eight moves targeting files `a`–`h`; the endpoint returned one octal digit per `turn` value.
4. Collected 60 turns and decoded each group of three octal digits into an ASCII character.

## Solution & Exploitation
* The leaked stream is the flag encoded as octal triplets, repeating every 60 digits (20 characters).
* `1,1,5 → 0o115 → 'M'`, `1,0,3 → 0o103 → 'C'`, `1,2,4 → 0o124 → 'T'` ...
* Final flag: `MCTF26{S0M3_CH3K3R5}` (verified `correct` via CTFd submission).
