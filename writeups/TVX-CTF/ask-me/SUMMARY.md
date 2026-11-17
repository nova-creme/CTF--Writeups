# ASK ME
* **Platform/Event:** TVX CTF
* **Category:** OSINT / steganography (290 pts)
* **Difficulty:** Medium
* **Flag:** `TVX{45C11_C0D3_15_U53FU11}`

## Objective
Find the password to the encrypted `FLAG.7z` hidden "in plain sight" across eight Minecraft screenshots, then read the flag from `FLAG.png`.

## Reconnaissance & Methodology
1. Tools used: `unzip`, `file`, `py7zr`, Python `PIL` for crops/brightening; `exiftool`/`zsteg`/`binwalk`/`pngcheck` checked and ruled out.
2. Dead ends: PNG chunk/trailing data, zip comments/extra fields, 7z headers, LSB/bit-plane scans, brightened shots, high-pass overlays, near-white text outside the HUD.
3. The key: each hotbar has a stack of 64 diamonds plus a second stack with a varying count. Counts in screenshot order: `6, 0, 15, 53, 14, 36, 9, 20`; character = `chr(64 + count)` → `F @ O u N d I T` → password **F@OuNdIT** ("Found IT", `@` for the space; shot 2 has no second stack → 0 → `@`).
4. Cropped/enlarged all hotbars with PIL NEAREST to read the digits.

## Solution & Exploitation
* Final payload: password `F@OuNdIT` to `py7zr.SevenZipFile(...).extractall()` → `FLAG.png`; crop the sign and enlarge 4×.
* Sign reads `TVX{45C11_C0D3_15_U53FU11}` — leetspeak "ASCII code is useful" with the challenge's spelling "USEFULL"; braces look like parentheses and the `0` in `C0D3` is slashed.
* Gotcha: the password checker first used `readall()` (nonexistent in this py7zr) — calibrate against a known-password archive before trusting failures.
