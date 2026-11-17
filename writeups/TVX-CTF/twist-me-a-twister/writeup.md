# TVX CTF — Twist Me A Twister (Reverse Engineering, 310 pts)

**Prompt:** "Ever heard of tongue twisters? programs can twist your tongue too!!"
**File:** `TwistMeATwister.exe`
**Flag:** `TVX{Fl4ggy_fl4g_fl4g_tw15ty_tw15t_tw15t}`

## Approach

The file is a tiny (about 4.6 KB) .NET assembly. No ilspy, mono or dotnet was
installed, so I parsed the metadata and disassembled the CIL with the Python
libraries `dnfile` and `dncil`.

```bash
mkdir -p /home/claude/twist && cp /mnt/user-data/uploads/103e31ce-1794568318728_TwistMeATwister.exe /home/claude/twist/t.exe && cd /home/claude/twist && file t.exe && ls -l t.exe && strings -a -n 5 t.exe | grep -iE 'flag|twist|correct|wrong|enter|input|python|upx|go\.|rust|\.NET|mono' | head -40; which objdump radare2 r2 ghidra rizin 2>/dev/null

which monodis ilspycmd dotnet mono ikdasm 2>/dev/null; python3 -c 'import dnfile; print(1)'; pip list 2>/dev/null | grep -iE 'dnfile|dncil|pefile|capstone'; strings -a -e l -n 3 t.exe | head -40

pip install --break-system-packages -q dnfile dncil
```

## CIL disassembler (`/home/claude/scripts/cildis.py`)

Note: it must not be named `dis.py` — see the gotchas in `TVX-CTF/GOTCHAS.md`.

```python
import sys, dnfile
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBase
from dncil.clr.token import Token

class R(CilMethodBodyReaderBase):
    def __init__(self, pe, row):
        self.pe=pe; self.offset=0
        self.data=pe.get_data(row.Rva, 4096)
    def read(self,n):
        d=self.data[self.offset:self.offset+n]; self.offset+=n; return d
    def tell(self): return self.offset
    def seek(self,o): self.offset=o; return o
    def resolve_token(self, tok): return None

pe = dnfile.dnPE(sys.argv[1])
tabs = pe.net.mdtables
for row in tabs.MethodDef:
    print('=== METHOD', row.Name, hex(row.Rva))
    body = CilMethodBody(R(pe,row))
    for ins in body.instructions:
        op=ins.operand; s=''
        if ins.opcode.name=='ldstr':
            s=repr(pe.net.user_strings.get(op.rid & 0xffffff).value)
        elif isinstance(op,Token):
            tn={0x0A:'MemberRef',0x06:'MethodDef',0x04:'Field',0x01:'TypeRef',0x02:'TypeDef'}.get(op.table if isinstance(op.table,int) else 0,str(op.table))
            nm=''
            try:
                if op.table==0x0A: r=tabs.MemberRef.rows[op.rid-1]; nm=f'{r.Name}'
                elif op.table==0x06: nm=tabs.MethodDef.rows[op.rid-1].Name
                elif op.table==0x04: nm=tabs.Field.rows[op.rid-1].Name
            except Exception as e: nm=str(e)
            s=f'{tn}:{nm}'
        elif op is not None: s=str(op)
        print(f'  {ins.offset:04x} {ins.opcode.name} {s}')
```

```bash
python3 -I /home/claude/scripts/cildis.py t.exe 2>&1 | head -400
python3 -I /home/claude/scripts/cildis.py t.exe 2>&1 | sed -n '/METHOD Main/,$p' | head -80
```

## Findings

`Main` prompts `flag> `, reads the input and compares it to the return value of
`Reveal()`, so the flag is `Reveal()`'s output. `Reveal()` decodes a 40-byte static
array (`data`, stored in the PE's `FieldRVA` table). For each output index `i`:

- `j = (i*7 + 3) % 40`
- `out[i] = ror8(data[j], j%5 + 1) ^ ((55 + j*11) & 0xFF)`

```python
python3 -I - <<'EOF'
import dnfile
pe=dnfile.dnPE('t.exe')
rva=[r.Rva for r in pe.net.mdtables.FieldRva][0]
data=pe.get_data(rva,40)
print(data.hex())
def ror(x,n): return ((x>>(n&31)) | (x<<((8-n)&31))) & 0xff
out=bytearray(40)
for i in range(40):
    j=(i*7+3)%40
    v=ror(data[j], j%5+1)
    out[i]=(v ^ ((55+j*11)&0xff)) & 0xff
print(out.decode('ascii','replace'))
EOF
```

The decode is clean ASCII; the `.exe` itself was never executed.
