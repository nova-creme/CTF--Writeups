# TVX CTF — OSINT, employee story — NOT SOLVED

**Prompt:** An employee on sick leave posted a story at an establishment; identify his name, the establishment, the device used and the number of people with him. Format `TVX{Ans1,Ans2,Ans3,Ans4}`.
**Only artifact:** a Street View-style photo of a landscaped corporate campus.

## What was done

Checked the photo for EXIF or GPS (none — it is a stripped export), ran a text
search on the scenery (inconclusive), and produced crops for Google Lens, Bing
Visual Search and Yandex Images. The establishment was not identified. I did not
help trace the person's social accounts, since that means profiling a specific
individual, and I cannot log into social platforms from the sandbox in any case.

```bash
mkdir -p /home/claude/osint && cp /mnt/user-data/uploads/9a732bf4-image.jpg /home/claude/osint/img.jpg && cd /home/claude/osint && python3 -I - <<'EOF'
from PIL import Image
from PIL.ExifTags import TAGS
im=Image.open('img.jpg'); print(im.size, im.format)
ex=im.getexif(); print('exif:',{TAGS.get(k,k):v for k,v in ex.items()})
print('gps:',ex.get_ifd(0x8825))
EOF
python3 -I - <<'EOF'
from PIL import Image
im=Image.open('img.jpg').convert('RGB')
crops={'building':(0,340,140,550),'bins_path':(540,700,720,830),'cars_lot':(380,610,760,720),'wide_scene':(0,330,935,960)}
for k,b in crops.items():
    c=im.crop(b); s=max(1,int(900/c.width)) if c.width<600 else 1
    c.resize((c.width*s,c.height*s),Image.LANCZOS).save(f'crop_{k}.png')
EOF
```

**Next step:** reverse image search on the crops, then Street View matching.
