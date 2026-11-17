# InIt CTF — India Tourist Map QR (IN PROGRESS — unsolved)

- **Category:** Misc / stego
- **Artifact:** `~/Downloads/india_tourist_map.png` (935×909, 8-bit RGB, ~1.1 MB)
- **Prompt:** "Scan the QR to enter the giveaway!" — banner text at the bottom,
  but **no QR is visible** anywhere in the image.
- **Status:** open. Work done so far documented below so it doesn't get repeated.

## Eliminated (do NOT retry these)

1. **Trailing data / file overlay** — IEND at offset 1158525 = file end − 8.
   Nothing after `IEND\xaeB`\x82``.
2. **PNG chunk analysis** — chunks are only `IHDR`, `iCCP` (389 B, standard
   GIMP "built-in sRGB" profile), 17× `IDAT`, `IEND`. No tEXt/zTXi/tIME/misc.
3. **IHDR height manipulation (hidden rows)** — IDAT decompresses to exactly
   `(1 + 935*3) × 909` bytes; zero extra rows. Height 909 is genuine.
4. **binwalk** — no embedded files.
5. **strings** — no flag-like strings.
6. **exiftool -a -u -g1** — metadata is stock GIMP sRGB; nothing custom.
7. **LSB bitplanes (zsteg + manual)** — b0/b1/b2 planes across RGB are art
   noise; zsteg reports nothing but random text fragments.
8. **OpenCV QRCodeDetector** — no detect on original, Otsu, inverted, or t128
   binarizations.
9. **Finder-pattern template scan** — horizontal profile 1:1:1:1:3:1:1:1:1
   for module sizes 2–6 across all rows: **zero hits**.
10. **Low-contrast hidden QR** — value histograms of near-white pixels
    (250–254) mapped and eyeballed per value: anti-aliasing noise, no blocky
    QR structure. (Watch out: `np.sum` on uint8 masks overflows — cast to int.)
11. **Local-variance QR hunt** — no large high-contrast square region anywhere.

## Observations / leads not yet exhausted

- The bottom banner "Scan the QR to enter the giveaway!" is rendered in a
  different font (monospace-ish) than the rest of the artwork — likely added
  in a second pass (image was GIMP-edited). The QR it promises may be:
  - **outside the image** (a URL to fetch, or encoded in the banner text itself),
  - hidden at a **sub-threshold contrast** that survived all binarizations,
  - or **not in this PNG at all** — maybe the visible "map" is the decoy and
    the real challenge is the *file provenance*.
- The very bottom edge (last ~20 px) shows small dark specks near center and
  right — unexamined at high zoom.
- Not tried yet: `zbarimg`, pyzbar; FFT magnitude inspection; exact-RGB
  value triplets (not just grayscale); pixel-difference vs a re-encoded copy;
  checking whether the banner text maps to a specific QR generation seed.

## Next steps

1. `zbarimg` + pyzbar pass (never actually run).
2. Zoom the bottom strip specks (`edge.png` regenerate at 8×, NEAREST).
3. Run the finder-pattern scan **per channel** at finer thresholds
   (e.g. `g < 253`, `g < 250`) instead of `< 128`.
4. Try `stegsolve` palette/gradient browsing.
