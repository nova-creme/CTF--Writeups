# TVX CTF — Chest, "DO NOT SORT" (Crypto)

**Prompt:** A chest of 1,437 items in one row, nine per line. "Every item stands for a letter, but not every letter has just one item." Find the warning someone wrote inside. Flag format `TVX{...}`.
**File:** `chest.txt`.
**Flag:** `TVX{never_dig_straight_down}`

## Approach

A homophonic substitution cipher: 39 distinct item names for 26 letters, with
the common letters spread over several items. The item frequencies were nearly
flat, so plain frequency analysis was useless. I solved it with simulated
annealing against an English quadgram model, then fixed the rare letters by hand
from context.

### Step 1: count items

```bash
mkdir -p /home/claude/chest && cp /mnt/user-data/uploads/577ba34a-1794568757107_chest.txt /home/claude/chest/chest.txt && cd /home/claude/chest && python3 -I - <<'EOF'
from collections import Counter
t=open('chest.txt').read().split()
print(len(t)); c=Counter(t); print(len(c))
for k,v in c.most_common(): print(f'{k:14}{v}')
EOF
```

### Step 2: get an English corpus

No corpus ships on the box, so I installed NLTK and pulled Brown and Gutenberg
through the proxy.

```bash
pip install --break-system-packages -q wordfreq nltk
python3 -I -c 'import wordfreq;print(1)'; ls /usr/share/dict 2>/dev/null
find / -xdev \( -name '*.txt' -o -name '*.rst' \) -size +200k 2>/dev/null | head
cd /home/claude/chest && NLTK_ALLOW_PROXIED_URLOPEN=1 timeout 200 python3 -I -c "
import nltk, nltk.pathsec
nltk.pathsec.ALLOW_PROXIED_FETCH=True
print(nltk.download('gutenberg', quiet=True), nltk.download('brown', quiet=True))
"
```

### Step 3: build the quadgram table (`solve.py`, writes `lp.npy`, about 13.7M letters)

```python
import numpy as np, re
from nltk.corpus import brown, gutenberg
txt=' '.join(brown.words())+' '+' '.join(gutenberg.words())
s=re.sub(r'[^a-z]','',txt.lower())
a=np.frombuffer(s.encode(),dtype=np.uint8)-97
q=((a[:-3].astype(np.int64)*26+a[1:-2])*26+a[2:-1])*26+a[3:]
cnt=np.bincount(q,minlength=26**4).astype(np.float64)
LP=np.log((cnt+0.1)/(cnt.sum()+0.1*26**4)).astype(np.float32)
np.save('/home/claude/chest/lp.npy',LP)
```

### Step 4: anneal

The first version collapsed into degenerate e/t/s output because a many-to-one
mapping can cheat the quadgram score. Adding a chi-square penalty that forces the
output letter distribution toward English fixed it. Final `anneal.py`:

```python
import numpy as np, random, math, sys, re, os
from nltk.corpus import brown
LP=np.load('/home/claude/chest/lp.npy')
t=open('/home/claude/chest/chest.txt').read().split()
items=sorted(set(t)); idx={k:i for i,k in enumerate(items)}
X=np.array([idx[w] for w in t]); N=len(X); K=len(items)
_s=re.sub(r'[^a-z]','',' '.join(brown.words()).lower())
_c=np.bincount(np.frombuffer(_s.encode(),dtype=np.uint8)-97,minlength=26).astype(float); FR=_c/_c.sum()
EXP=FR*N
W=float(os.environ.get('W','1.5'))
def score(m):
    p=m[X].astype(np.int64)
    obs=np.bincount(p,minlength=26)
    pen=W*(((obs-EXP)**2)/EXP).sum()
    q=((p[:-3]*26+p[1:-2])*26+p[2:-1])*26+p[3:]
    return LP[q].sum()-pen
def run(seed,iters=60000):
    rng=random.Random(seed)
    m=np.array([rng.randrange(26) for _ in range(K)])
    cur=score(m); best=cur; bm=m.copy()
    T0=8.0
    for it in range(iters):
        T=T0*(1-it/iters)+0.05
        i=rng.randrange(K); old=m[i]
        if rng.random()<0.8:
            m[i]=rng.randrange(26)
            if m[i]==old: continue
            new=score(m)
            if new>cur or rng.random()<math.exp((new-cur)/T): cur=new
            else: m[i]=old
        else:
            j=rng.randrange(K)
            if m[i]==m[j]: continue
            m[i],m[j]=m[j],m[i]
            new=score(m)
            if new>cur or rng.random()<math.exp((new-cur)/T): cur=new
            else: m[i],m[j]=m[j],m[i]
        if cur>best: best=cur; bm=m.copy()
    return best,bm
if __name__=='__main__':
    seed=int(sys.argv[1])
    b,m=run(seed)
    print(seed,round(b,1),''.join(chr(97+x) for x in m[X])[:200],flush=True)
    np.save(f'/home/claude/chest/m{seed}.npy',m)
```

```bash
cd /home/claude/chest && for s in 1 2 3 4 5 6; do (python3 -I /home/claude/scripts/anneal.py $s > out$s.txt 2>&1 &); done; sleep 120; cat out*.txt
```

Seeds 2, 3 and 4 converged on the same readable text ("it began the way every
world begins with a single tree..."). A few rare letters were still wrong (for
example "traftedatable" should be "crafted a table"), because items of different
rare letters had been merged into one group.

### Step 5: fix rare letters from context

| Item | Letter | Evidence |
|------|--------|----------|
| `arrow` | k | "oak", "knuckles", "week" |
| `lapis_lazuli` | c | "cold air", "careful", "cave" |
| `cobblestone` | p | "punched", "pickaxe", "across the plains" |
| `coal` | x | "next week", "pickaxe", "tag TVX" |
| `bookshelf` | z | "zombies", "blazes", "haze" |
| `emerald` | j | "joined with underscores" |

```python
python3 -I - <<'EOF'
import numpy as np, textwrap
t=open('chest.txt').read().split()
items=sorted(set(t)); idx={k:i for i,k in enumerate(items)}
m=np.load('m2.npy')
mp={k:chr(97+m[idx[k]]) for k in items}
mp.update({'arrow':'k','lapis_lazuli':'c','cobblestone':'p','coal':'x','bookshelf':'z','emerald':'j'})
pt=''.join(mp[w] for w in t)
print(chr(10).join(textwrap.wrap(pt,100)))
EOF
```

The fully corrected plaintext is clean English. The warning near the end says
the phrase is "never dig straight down", to be wrapped in braces behind the tag
`TVX`, all lowercase, joined with underscores.
