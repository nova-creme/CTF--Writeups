# TVX CTF — Creeper's Shared Prime (Crypto, 100 pts)

**Prompt:** Two RSA vaults built with parts from the same crafting table; the message is encrypted for Vault A.
**Files:** `public_keys.txt` (two moduli, `e = 65537`) and `ciphertext.txt`.
**Flag:** `TVXCTF{the_creeper_reused_a_prime}`

## Approach

The two moduli share a prime factor. `gcd(nA, nB)` returns it, which factors
`nA`, and then it is ordinary RSA decryption.

```python
python3 -I - <<'EOF'
from math import gcd
nA=1942668892225729070919461906823520455305416829490420089422957436437580309796491507761
nB=1942668892225729070919461906823519371241578281403951004079222153957205455266330293941
e=65537
c=1574928985319013777436289945491687612751672976588545303342361399014858100334313795739
p=gcd(nA,nB); print('p',p)
assert 1<p<nA
q=nA//p; assert p*q==nA
d=pow(e,-1,(p-1)*(q-1))
m=pow(c,d,nA)
print(m.to_bytes((m.bit_length()+7)//8,'big'))
EOF
```

Shared prime: `p = 1393796574908163946345982392040522705234977`.
