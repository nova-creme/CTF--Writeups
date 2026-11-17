# Steve's Lost Book
* **Platform/Event:** TVX CTF
* **Category:** Crypto (encoding)
* **Difficulty:** Easy
* **Flag:** `TVXCTF{steve_found_the_hidden_chest}`

## Objective
Decode a page that an Enderman encoded "into a travel-safe alphabet".

## Reconnaissance & Methodology
1. Tools used: `base64 -d`.
2. File `Steves_Lost_Book.txt` held `VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9` — the character set and `=`-free body suggest Base64; "travel-safe alphabet" is the hint.
3. Both `TVXCTF{...}` and `TVX{...}` were accepted by the challenge page.

## Solution & Exploitation
* Final payload: `echo 'VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9' | base64 -d` → `TVXCTF{steve_found_the_hidden_chest}`.
