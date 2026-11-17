# OSINT Chain Stage 2 — The Watchful Eye (150 pts)

**Flag:** `safctf{watchful_eye_b2}`

## Commands run

```bash
curl -s http://54.72.82.22:8098/agora/u/outis-k/photos
# → only "Usual spot" (cafe photo) had a "Download original upload" link

curl -s http://54.72.82.22:8098/agora/photo/cafe/original -o original_cafe.jpg
exiftool original_cafe.jpg
```
→ `User Comment` field: `safctf{watchful_eye_b2}`
→ Also recovered: `Serial Number: 6021743`, `GPS Latitude: 38 deg 30' 24.58" N`,
`GPS Longitude: 40 deg 29' 31.07" W` (used later)

Verified byte-exactness of the extracted flag (no hidden characters):

```bash
exiftool -UserComment original_cafe.jpg
exiftool -b -UserComment original_cafe.jpg | xxd | head -20
```
