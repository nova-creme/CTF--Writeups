# InIt CTF — The Midnight Key

- **Category:** Crypto (classical cipher)
- **Artifact:** forum message (text only)
- **Ciphertext:** `UvLg{d1m3u3k3_i4a_q0g_bn3_4uli3z}`
- **Hint:** "The key is the hour when everything goes quiet."
- **Flag format:** `InIt{...}`

## Flag

```
InIt{v1g3n3r3_w4s_n0t_th3_4nsw3r}
```

## Solution

The hint points to midnight — the Vigenère key is the word `midnight`
(values `12 8 3 13 8 6 7 19`), repeating across letters only. Digits and the
`{`, `}`, `_` characters pass through untouched.

Decryption: `P = C − K` per letter.

| Ciphertext | Key window | Plaintext |
|------------|------------|-----------|
| `UvLg` | `midn` | `InIt` |
| `d1m3u3k3` | `ightmi` | `v1g3n3r3` |
| `i4a` | `gh` | `w4s` |
| `q0g` | `dn` | `n0t` |
| `bn3` | `ig` | `th3` |
| `4uli3z` | `htmi` | `4nsw3r` |

Confirmation: `UvLg − midn = InIt` matches the flag format exactly — the key
was validated against a known plaintext prefix (4/4 letters, ~1/26⁴ odds).

The flag's punchline names the cipher itself: *vigenere was not the answer* —
well, it was, but the joke is that a "key = hour" riddle resolves to Vigenère.
