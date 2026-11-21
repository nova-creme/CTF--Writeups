# PwnIntro
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Pwn (ret2win)
* **Difficulty:** Easy
* **Flag:** `MCTF26{tH4t_was_4actU4lLy_v3rY_s1mpl3}`

## Objective
The challenge binary (`/home/novacreme/Downloads/galaxy/pwnintro`) comes from `main.c`, which
declares `char buf[32]` but the service reads `0x100` bytes into it via `read(STDIN, buf, 0x100)`,
before calling `cast_spell()`. The exploit is a plain stack buffer overflow / ret2win style
overwrite.

## Reconnaissance & Methodology
1. Step 1: Trigger the overflow
2. Step 2: Land the flag

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{tH4t_was_4actU4lLy_v3rY_s1mpl3}`
