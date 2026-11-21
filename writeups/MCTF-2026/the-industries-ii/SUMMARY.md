# The Industries (II)
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Web (Flask auth)
* **Difficulty:** Easy
* **Flag:** `MCTF26{p5ycH1c_d3S7R0y3d}`

## Objective
The rebuilt site replaced the base64 role cookie with a Flask signed session and a
login form. The administrator credentials were still `admin:admin`, and the "psychic"
defense is only a client-side popup — after logging in, the flag is in `/admin`.

## Reconnaissance & Methodology
1. Step 1: Log in
2. Step 2: Read the flag

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{p5ycH1c_d3S7R0y3d}`
