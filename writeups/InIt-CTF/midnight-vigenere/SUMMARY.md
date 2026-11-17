# The Midnight Key
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Crypto (classical cipher)
* **Difficulty:** Easy
* **Flag:** `InIt{v1g3n3r3_w4s_n0t_th3_4nsw3r}`

## Objective
Decrypt a forum ciphertext (`UvLg{d1m3u3k3_i4a_q0g_bn3_4uli3z}`) given the hint: "The key is the hour when everything goes quiet."

## Reconnaissance & Methodology
1. Identified the `InIt{...}` known-plaintext prefix in the ciphertext and noted that digits and `{`, `}`, `_` pass through unchanged.
2. Tools used: manual Vigenère analysis (or a simple one-liner script); no external tooling required.
3. "Hour when everything goes quiet" resolves to **midnight** → key `midnight` (letter values `12 8 3 13 8 6 7 19`), repeated across letters only.

## Solution & Exploitation
* Decrypt with `P = C − K` per letter: `UvLg − midn = InIt` (validated against the flag prefix, 4/4 letters).
* Key windows / plaintext: `d1m3u3k3|ightmi` → `v1g3n3r3`; `i4a|gh` → `w4s`; `q0g|dn` → `n0t`; `bn3|ig` → `th3`; `4uli3z|htmi` → `4nsw3r`.
* Final payload/deduction: key `midnight` → `InIt{v1g3n3r3_w4s_n0t_th3_4nsw3r}` (the flag jokes that "vigenere was not the answer" — it was).
