# Ender chest (cryptoone)
* **Platform/Event:** TVX CTF
* **Category:** Crypto (ECDLP / smooth-order curve, AES-CBC)
* **Difficulty:** Hard
* **Flag:** `TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}` (not confirmed by platform; the easy decoy `TVX{tNt_g035_B00m_C0ngr4t5}` was rejected)

## Objective
Two AES-CBC ciphertexts: the shulker box keyed with `str(Q[0])` (public) and the ender chest keyed with `str(d)` where `Q = d*G`. Recover the real flag from the ender chest.

## Reconnaissance & Methodology
1. Tools used: `py7zr`, `pycryptodome`, `cypari` (PARI/GP via Python), `hashlib.sha256`, PKCS#7 `unpad`.
2. Decoy first: `Q` is public, so `chest(REALFLAG, str(Q[0]))` decrypts immediately to `TVX{tNt_g035_B00m_C0ngr4t5}` — **rejected**, it's the troll.
3. Verified both points lie on the curve and it's non-singular (`4a³+27b² ≠ 0 mod p`).
4. `pari.ellcard` → group order `4724861355973759917094976238449899 = 11 · 367 · 13399 · 58453 · 484079 · 40128631 · 76927309` — smooth (largest factor ~2^26), not anomalous → Pohlig-Hellman applicable.
5. `pari.elllog(E, Q, G, ellorder(E,G))` → `d = 2327569722739447708246377569803395`; verified `d*G == Q`.

## Solution & Exploitation
* Final payload: key = `sha256(str(d))`, decrypt the ender-chest ciphertext with AES-CBC (`IV = ct[:16]`) → `TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}`.
* Lesson: a flag that decrypts too easily may be a decoy — here the public-key-keyed ciphertext was the troll and the hard ECDLP one was real. Smooth group order breaks ECC regardless of key size.
