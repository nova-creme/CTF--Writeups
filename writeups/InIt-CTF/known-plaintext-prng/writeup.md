# InIt CTF — Known Plaintext PRNG

- **Category:** Crypto
- **Flag format:** `InIt{...}`
- **Files:** `encrypt.py`, `flag.enc`

## Flag

```
InIt{kn0wn_pl41nt3xt_4tt4cks_4r3_c00l}
```

## Analysis

- The key starts as 4 random bytes (`os.urandom(4)`), so its search space is only 2^32.
- The update is `key = (key * 1103515245 + 12345) & 0xFFFFFFFF`, with public, fixed constants.
- The last block is truncated rather than padded in the output, so the ciphertext is the same length as the flag.

## Solution

The flag format means the first plaintext block is `InIt`. XOR is its own inverse,
so `key0 = cipher_block0 XOR "InIt"`. Run the LCG forward from `key0` and XOR each
ciphertext block with the current key.

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

## Takeaway

A known plaintext prefix leaks the key stream's seed. The LCG is also linear and
invertible, so it was never a secure key generator.
