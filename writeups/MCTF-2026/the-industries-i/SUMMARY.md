# The Industries (I)
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Web (cookie forgery)
* **Difficulty:** Easy
* **Flag:** `MCTF26{w3Lc0m3_t0_Th3_Gu1ld}`

## Objective
The Flask site put the user's role in a plain base64 cookie. Setting the cookie to
base64("admin") unlocked `/admin`, and the flag was split across two HTML comments:
the prefix in `/history` and the suffix in `/admin`.

## Reconnaissance & Methodology
1. Step 1: Forge the role cookie
2. Step 2: Combine the two comment halves

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{w3Lc0m3_t0_Th3_Gu1ld}`
