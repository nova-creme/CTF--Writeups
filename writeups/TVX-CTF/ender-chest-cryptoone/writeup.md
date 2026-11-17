# TVX CTF — Ender chest / cryptoone (Crypto)

**Prompt (from `chall.py`):** "You found a world seed nobody could guess and used it as the key to his chests. Elliptic curves are unbreakable, so the curve the server admin picked must be fine, right?... RIGHT???"
**Files:** `chall.py`, `output.txt` (inside `cryptoone.7z`).
**Flag:** `TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}` (decoy `TVX{tNt_g035_B00m_C0ngr4t5}` was rejected).

## Setup

`chall.py` encrypts two messages with AES-CBC, key `SHA256(str(...))`:

- `ender_chest = chest(FLAG, str(d))` — opens with the private scalar `d`
- `shulker_box = chest(REALFLAG, str(Q[0]))` — opens with the x-coordinate of the public point `Q = d*G`

`output.txt` gives `p, a, b, G, Q` and both ciphertexts.

```bash
mkdir -p /home/claude/cryptoone/x && cd /home/claude/cryptoone && cp /mnt/user-data/uploads/163fc6b3-1794571143994_cryptoone.7z c.7z && file c.7z && python3 -I - <<'EOF'
import py7zr
z=py7zr.SevenZipFile('c.7z')
print('needs_pw:',z.needs_password())
for f in z.list(): print(f.filename,f.uncompressed)
EOF
python3 -I -c "import py7zr; py7zr.SevenZipFile('c.7z').extractall('x')" && cat x/TVXCTFCRYPTO1/chall.py; echo; echo ------; cat x/TVXCTFCRYPTO1/output.txt
```

## The decoy

`Q` is public, so the shulker box can be opened immediately. It decrypts to
`TVX{tNt_g035_B00m_C0ngr4t5}`, which the platform rejected. That is the troll
flag; the real one is in the ender chest.

```bash
pip install --break-system-packages -q pycryptodome
python3 -I - <<'EOF'
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
def dec(h,key_src):
    raw=bytes.fromhex(h); key=hashlib.sha256(key_src).digest()
    return unpad(AES.new(key,AES.MODE_CBC,raw[:16]).decrypt(raw[16:]),16)
Q=(3869418175838450319054504785525959, 1429060253338888234770668216689896)
sb='db755bc9df9ca0eb13611170fceaf940a9395f71ac25050188701bf0b7c7fcb4954519578e377ed12f027388d3d63c8f'
print(dec(sb,str(Q[0]).encode()))
EOF
```

## The real target

The ender chest needs `d`, the discrete log of `Q` to base `G`.

```python
# both points are on the curve; curve is not singular
python3 -I - <<'EOF'
p=4724861355973759862466485852137759; a=927566916496059264792326746507264; b=4715968330470840770745781630703560
G=(3675942204092047283238136253093045, 3544727085494657603430718404172845)
Q=(3869418175838450319054504785525959, 1429060253338888234770668216689896)
print((G[1]**2-(G[0]**3+a*G[0]+b))%p==0, (Q[1]**2-(Q[0]**3+a*Q[0]+b))%p==0)
print((4*a**3+27*b**2)%p)
EOF

# count points with PARI (needs a bigger stack)
pip install --break-system-packages -q cypari
python3 -I - <<'EOF'
from cypari import pari
pari.allocatemem(2*10**9)
p=4724861355973759862466485852137759; a=927566916496059264792326746507264; b=4715968330470840770745781630703560
E=pari.ellinit([a,b],p)
n=pari.ellcard(E)
print('order',n); print('factor',pari.factor(n)); print('anomalous?', n==p)
EOF
```

Curve order: `4724861355973759917094976238449899 = 11 * 367 * 13399 * 58453 * 484079 * 40128631 * 76927309`. It is smooth (largest prime factor about 2^26) and not anomalous, so Pohlig-Hellman breaks the discrete log into tiny pieces. PARI's `elllog` does this directly:

```python
python3 -I - <<'EOF'
from cypari import pari
pari.allocatemem(2*10**9)
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
p=4724861355973759862466485852137759; a=927566916496059264792326746507264; b=4715968330470840770745781630703560
Gp=(3675942204092047283238136253093045, 3544727085494657603430718404172845)
Qp=(3869418175838450319054504785525959, 1429060253338888234770668216689896)
E=pari.ellinit([a,b],p)
G=pari(f'[Mod({Gp[0]},{p}),Mod({Gp[1]},{p})]'); Q=pari(f'[Mod({Qp[0]},{p}),Mod({Qp[1]},{p})]')
gord=pari.ellorder(E,G)
d=int(pari.elllog(E,Q,G,gord)); print('d =',d)
chk=pari.ellmul(E,G,d); print('verify:',int(chk[0].lift())==Qp[0] and int(chk[1].lift())==Qp[1])
def dec(h,key_src):
    raw=bytes.fromhex(h); key=hashlib.sha256(key_src).digest()
    return unpad(AES.new(key,AES.MODE_CBC,raw[:16]).decrypt(raw[16:]),16)
ec='46e14511e959705d1fe179ab3a4c2c40f5db5273f61faa0e319096122ccc59f812a0f0591c193aab914bda09c9f609413398a9c3e8c8e602fc356ff3ea5a7583'
print(dec(ec,str(d).encode()))
EOF
```

Result: `d = 2327569722739447708246377569803395` (verified: `d*G == Q`), and the
ender chest decrypts to clean text.
