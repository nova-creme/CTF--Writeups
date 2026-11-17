# Known Plaintext PRNG
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Crypto (XOR stream + LCG)
* **Difficulty:** Medium
* **Flag:** `InIt{kn0wn_pl41nt3xt_4tt4cks_4r3_c00l}`

## Objective
Decrypt `flag.enc`: the flag is XORed in 4-byte blocks with a 32-bit key that advances via an LCG after every block. Recover the plaintext from `encrypt.py` and the ciphertext alone.

## Reconnaissance & Methodology
1. Reviewed `encrypt.py`: `key = os.urandom(4)` (only 2^32 search space); `key = (key * 1103515245 + 12345) & 0xFFFFFFFF` after each block — public fixed LCG constants.
2. Tools used: Python `int.from_bytes` / `to_bytes`, XOR (`^`), the known-plaintext `InIt` prefix.
3. The final block is truncated (not padded), so ciphertext length equals flag length.
4. Because XOR is its own inverse, the known first plaintext block `InIt` directly reveals the initial key: `key0 = int.from_bytes(ct[:4],"big") ^ int.from_bytes(b"InIt","big")`.

## Solution & Exploitation
* Run the LCG forward from the recovered `key0`, XOR each 4-byte ciphertext block with the current key, and slice the last (short) block to its original length.
* Final payload:
  ```python
  d = open("flag.enc", "rb").read()
  k = int.from_bytes(d[:4], "big") ^ int.from_bytes(b"InIt", "big")
  out = b""
  for i in range(0, len(d), 4):
      c = d[i:i+4]
      out += (int.from_bytes(c.ljust(4, b"\0"), "big") ^ k).to_bytes(4, "big")[:len(c)]
      k = (k * 1103515245 + 12345) & 0xFFFFFFFF
  print(out.decode())
  ```
* Result: `InIt{kn0wn_pl41nt3xt_4tt4cks_4r3_c00l}`.
* Takeaway: a known-plaintext prefix leaks the keystream seed; an LCG is linear and invertible, never a secure key generator.
