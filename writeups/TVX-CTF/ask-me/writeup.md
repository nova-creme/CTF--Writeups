# TVX CTF — ASK ME (OSINT, 290 pts)

**Prompt:** A batch of Minecraft screenshots; the flag is in a password-protected file and the key was left "in plain sight". Hint: "ASK ME".
**File:** `ASK_ME.zip`
**Flag:** `TVX{45C11_C0D3_15_U53FU11}`

## Contents

Eight screenshots (`1.png` to `8.png`) and `FLAG.7z` (encrypted; it contains `FLAG.png`).

```bash
mkdir -p /home/claude/askme/x && cd /home/claude/askme && cp /mnt/user-data/uploads/54536b12-1794569411900_ASK_ME.zip a.zip && unzip -l a.zip; unzip -o -q a.zip -d x; find x -type f | head -50
```

## Dead ends (all clean, kept so you know what was ruled out)

PNG chunk and trailing-data scan, zip comments and extra fields, 7z header and
filename listing, bit-plane/LSB scans across channels and orders for magic bytes
and printable text, brightened versions of the dark screenshots, a high-pass
filter looking for faint overlays, and a hunt for near-white text clusters
outside the HUD.

```bash
cd "/home/claude/askme/x/ASK ME" && which 7z 7za 7zr exiftool zsteg binwalk pngcheck 2>/dev/null; file *
pip install --break-system-packages -q py7zr
cd /home/claude/askme && python3 -I - <<'EOF'
import zipfile
z=zipfile.ZipFile('a.zip')
print('zip comment:',z.comment)
for i in z.infolist(): print(i.filename, i.date_time, i.comment, i.extra[:60])
EOF
# brighten dark shots (gamma)
mkdir -p br && python3 -I - <<'EOF'
import numpy as np
from PIL import Image
for n in [3,5,6,7,8]:
    im=np.array(Image.open(f'x/ASK ME/{n}.png').convert('RGB')).astype(float)/255
    Image.fromarray((np.clip(im**0.35,0,1)*255).astype(np.uint8)).save(f'br/{n}.png')
EOF
```

## The key

Every screenshot's hotbar holds a stack of 64 diamonds plus a second diamond
stack with a varying count. Zooming in on the hotbars gave the counts in
screenshot order: `6, (none), 15, 53, 14, 36, 9, 20`. The character is
`chr(64 + count)`, where 64 is the other stack:

| Shot | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|------|---|---|---|---|---|---|---|---|
| Count | 6 | 0 | 15 | 53 | 14 | 36 | 9 | 20 |
| Char | F | @ | O | u | N | d | I | T |

So the password is **F@OuNdIT** ("Found IT", with `@` for the space). Screenshot 2
has no second stack, so its count is 0 and the character is `@`.

```python
# crop and enlarge all hotbars (and count labels) to read the digits
python3 -I - <<'EOF'
from PIL import Image
tiles=[]
for n in range(1,9):
    im=Image.open(f'x/ASK ME/{n}.png').convert('RGB'); W,H=im.size
    c=im.crop((585,H-90,1335,H)); tiles.append(c.resize((c.width*2,c.height*2),Image.NEAREST))
out=Image.new('RGB',(tiles[0].width,sum(t.height for t in tiles)))
y=0
for t in tiles: out.paste(t,(0,y)); y+=t.height
out.save('hotbars.png')
EOF
```

## Password check script (`try7z.py`)

The first attempt used `readall()`, which does not exist in this py7zr version,
so early guesses (including ASK ME, askme, FOUNDIT variants) produced meaningless
failures. I calibrated against a known-good encrypted archive first and then used
`extractall`:

```python
import py7zr, sys, tempfile, os
def attempt(path, pw):
    d=tempfile.mkdtemp(prefix='x7z_')
    try:
        with py7zr.SevenZipFile(path,password=pw) as z: z.extractall(d)
        files=[os.path.join(r,f) for r,_,fs in os.walk(d) for f in fs]
        return d, files
    except Exception as e:
        return None, f'{type(e).__name__}: {str(e)[:60]}'
if __name__=='__main__':
    path=sys.argv[1]
    for pw in sys.argv[2:]:
        d,f=attempt(path,pw); print(repr(pw),'->',('OK '+str(f)+' in '+d) if d else f)

# calibration: known right vs wrong password on a test archive
cd /home/claude/test7z && python3 -I /home/claude/scripts/try7z.py /home/claude/test7z/t.7z right wrong

# brute force the one unknown character (and a trailing char) over all printable ASCII
cd /home/claude/test7z && python3 -I /home/claude/scripts/brute.py
```

`brute.py` tried `F` + every printable character + `OuNdIT`, and `FOuNdIT` + every
printable character, in parallel with `ProcessPoolExecutor`. It hit `F@OuNdIT` in
about three seconds.

```bash
# view the extracted image, then enlarge the sign
python3 -I -c "
from PIL import Image
im=Image.open('/tmp/x7z_arm6uib4/FLAG.png').convert('RGB').crop((775,445,1135,630))
im.resize((im.width*4,im.height*4),Image.NEAREST).save('sign.png')"
```

`FLAG.png` shows a sign reading `TVX{` / `45C11_` / `C0D3_15` / `U53FU11}`:
leetspeak for "ASCII code is useful", keeping the challenge's own spelling
"USEFULL". The font draws the braces like parentheses, and the `0` in `C0D3` has
a slash through it, so it is a zero.
