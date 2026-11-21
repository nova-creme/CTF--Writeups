# All Your Base Are Belong To Us
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Crypto (base encoding)
* **Difficulty:** Easy
* **Flag:** `MCTF26{v3Ry_b453D_t45k_w45Nt_1t}`

## Objective
The challenge file `/home/novacreme/Downloads/galaxy/flag.txt` stores the flag encoded
character-by-character across lines: line 1 is a unary count, and each following line is
that character's ASCII value written in the base equal to its 1-based line number.

## Reconnaissance & Methodology
1. Step 1: Decode the unary line
2. Step 2: Decode the base lines
3. Step 3: Reassemble

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{v3Ry_b453D_t45k_w45Nt_1t}`
