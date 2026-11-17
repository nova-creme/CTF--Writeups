# India Tourist Map QR (unsolved)
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Misc / stego
* **Difficulty:** Hard
* **Flag:** `Not recovered — challenge unsolved (work in progress)`

## Objective
The banner of `~/Downloads/india_tourist_map.png` says "Scan the QR to enter the giveaway!" but **no QR is visible** anywhere in the image. Find the hidden QR / flag. This is the one unsolved challenge from the session; full working notes are in `NOTES.md`.

## Reconnaissance & Methodology
1. Tools used: `binwalk`, `strings`, `exiftool`, `zsteg`, OpenCV `QRCodeDetector`, custom finder-pattern and low-contrast/local-variance scans, PNG chunk parsing.
2. Eliminated: trailing data/overlay (IEND at file end), PNG chunk anomalies (only IHDR/iCCP/17×IDAT/IEND), hidden rows via IHDR height (IDAT decompresses to exactly the expected size), binwalk, metadata, flag-like strings.
3. Stego eliminated: LSB bitplanes b0–b2 (art noise), OpenCV detection on original/Otsu/inverted/threshold binarizations, finder-pattern template scans (module sizes 2–6, zero hits), near-white low-contrast mapping, local-variance square hunt.
4. Lead: the bottom banner is rendered in a different font — likely added in a second GIMP pass — so the QR may be outside the image, sub-threshold, or the real puzzle may be file provenance.

## Solution & Exploitation
* No flag yet. Remaining next steps (from `NOTES.md`): `zbarimg`/pyzbar; 8× NEAREST zoom of the bottom-strip specks; per-channel finder scans at finer thresholds (`g < 253`, `g < 250`); `stegsolve` palette/gradient browsing.
* This SUMMARY documents the current state so the elimination work isn't repeated; see `NOTES.md` for the full detail.
