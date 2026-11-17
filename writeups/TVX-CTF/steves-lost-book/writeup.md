# TVX CTF — Steve's Lost Book (Crypto)

**Prompt:** A page encoded by an Enderman "into a travel-safe alphabet". The challenge page says both `TVXCTF{...}` and `TVX{...}` are accepted.
**File:** `Steves_Lost_Book.txt`, containing `VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9`.
**Flag:** `TVXCTF{steve_found_the_hidden_chest}`

## Approach

"Travel-safe alphabet" points to Base64.

```bash
echo 'VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9' | base64 -d; echo
```
