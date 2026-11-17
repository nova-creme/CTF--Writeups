# TVX CTF — Summer Is Over (Reverse Engineering, 240 pts)

**Prompt:** "When something fades away, something else comes to light."
**File:** `SummerIsOver.exe`
**Flag:** `TVX{4nd_S0_7h3_5un_Sh1n35}`

## Approach

Same shape as challenge 1: a small .NET assembly with `blob` (26 bytes) and
`schedule` (8 bytes) static arrays, a `Reveal` method and a `Main` that compares
input to `Reveal()`. Disassembled with the same `cildis.py` script.

```bash
mkdir -p /home/claude/summer && cp /mnt/user-data/uploads/bfce3917-1794568441547_SummerIsOver.exe /home/claude/summer/s.exe && cd /home/claude/summer && file s.exe && ls -l s.exe && strings -a -n 4 s.exe | head -60; echo ---UTF16---; strings -a -e l -n 3 s.exe | head -60

python3 -I /home/claude/scripts/cildis.py s.exe 2>&1 | head -300
python3 -I - <<'EOF'
import dnfile
pe=dnfile.dnPE('s.exe')
t=pe.net.mdtables
for i,f in enumerate(t.Field): print('field',i+1,f.Name)
for r in t.FieldRva: print('fieldrva', hex(r.Rva))
EOF
```

## Reveal logic

For each `i` in `0..25`:

1. Read `blob[(i*5+1) % 26]`
2. XOR with `(51 + 11*i) & 0xFF`
3. XOR with `schedule[i % 8]`
4. Subtract `(3*i*i + 25) & 0xFF`
5. Rotate right by `i%5 + 1`
6. XOR with `(33 + 7*i) & 0xFF`

Then each group of 4 bytes is reversed in place (the last group has 2 bytes and
is reversed too).

```python
python3 -I - <<'EOF'
import dnfile
pe=dnfile.dnPE('s.exe')
rvas=[r.Rva for r in pe.net.mdtables.FieldRva]
blob=pe.get_data(rvas[0],26); sched=pe.get_data(rvas[1],8)
n=len(blob)
def ror(x,k): return ((x>>(k&31)) | (x<<((8-k)&31))) & 0xff
out=bytearray(n)
for i in range(n):
    j=(i*5+1)%n
    v=blob[j]
    v=(v ^ ((51+11*i)&255))&255
    v=(v ^ sched[i%len(sched)])&255
    v=(v - ((i*i*3+25)&255))&255
    v=ror(v, i%5+1)
    out[i]=(v ^ ((33+7*i)&255))&255
res=bytearray(n)
for i in range(n):
    g=i//4*4; l=min(4,n-g)
    res[g+l-1-(i-g)]=out[i]
print(res.decode('ascii','replace'))
EOF
```
