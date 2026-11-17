# Double-encoded string
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Misc / Crypto
* **Difficulty:** Easy
* **Flag:** `InIt{r0t_th3n_b64_1s_n0t_s3cur1ty}`

## Objective
Decode an intercepted string from an admin who "double-encoded it for safety" and recover the `InIt{...}` flag.

## Reconnaissance & Methodology
1. `VmFWZ3tlMGdfZ3UzYV9vNjRfMWZfYTBnX2YzcGhlMWdsfQ==` — the `==` padding and A-Z/a-z/0-9 character set identify **Base64**.
2. Tools used: Python `base64` + `codecs` (ROT13), or CyberChef's `Magic` operation which solves it instantly.
3. Base64 decode yields `VaVg{e0g_gu3a_o64_1f_a0g_f3phe1gl}` — braces, underscores and digits are untouched; only letters are scrambled → a letter substitution.
4. Known-plaintext check: `VaVg` vs `InIt` gives V→I, a→n, V→I, g→t — a uniform shift of 13 → **ROT13**.

## Solution & Exploitation
* Final payload: `codecs.decode(base64.b64decode(s).decode(), "rot13")` → `InIt{r0t_th3n_b64_1s_n0t_s3cur1ty}`.
* Takeaway: encodings aren't encryption; stacking two keyless encodings adds no security.
