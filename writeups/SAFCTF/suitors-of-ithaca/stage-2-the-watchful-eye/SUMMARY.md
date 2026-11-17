# The Watchful Eye (Stage 2)
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT / Forensics (EXIF) (150 pts)
* **Difficulty:** Easy
* **Flag:** `safctf{watchful_eye_b2}`

## Objective
Extract the second flag and follow-up leads from a photo posted by `outis-k`.

## Reconnaissance & Methodology
1. Tools used: `curl`, `exiftool`, `xxd`.
2. `/agora/u/outis-k/photos` showed only "Usual spot" (a cafe photo) with a "Download original upload" link.
3. Downloaded `original_cafe.jpg`; `exiftool` revealed `User Comment: safctf{watchful_eye_b2}`, camera `Serial Number: 6021743`, and GPS `38 deg 30' 24.58" N, 40 deg 29' 31.07" W`.
4. Verified byte-exactness with `exiftool -b -UserComment original_cafe.jpg | xxd` (no hidden characters).

## Solution & Exploitation
* Flag = `safctf{watchful_eye_b2}` from the EXIF `User Comment` field.
* The GPS coordinates feed Stage 3; the camera serial number feeds Stage 5 (Drachma Market listing).
