# InIt CTF — Double-encoded string

- **Category:** Misc / Crypto
- **Flag format:** `InIt{...}`
- **Intercepted string:** `VmFWZ3tlMGdfZ3UzYV9vNjRfMWZfYTBnX2YzcGhlMWdsfQ==`

## Flag

```
InIt{r0t_th3n_b64_1s_n0t_s3cur1ty}
```

## Solution

The `==` padding and the character set (A-Z, a-z, 0-9) point to Base64. Decoding
gives:

```
VaVg{e0g_gu3a_o64_1f_a0g_f3phe1gl}
```

The braces, underscores and digits are unchanged and only the letters look
scrambled, so it's a letter substitution. `VaVg` against the known prefix `InIt`
gives V→I, a→n, V→I, g→t — a shift of 13, so ROT13.

Applying ROT13 gives the flag.

```python
import base64, codecs
s = "VmFWZ3tlMGdfZ3UzYV9vNjRfMWZfYTBnX2YzcGhlMWdsfQ=="
print(codecs.decode(base64.b64decode(s).decode(), "rot13"))
```

## Takeaway

Encodings aren't encryption, and stacking two keyless ones adds no security.
CyberChef's Magic operation solves this instantly.
