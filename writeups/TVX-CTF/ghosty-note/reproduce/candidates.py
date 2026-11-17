import hashlib, base64, struct, itertools

K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
def R(x,n): return ((x>>n)|(x<<(32-n)))&0xffffffff
def gn_hash(msg, mod=True):
    h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
    l=len(msg)*8
    msg=msg+b'\x80'
    while len(msg)%64!=56: msg+=b'\x00'
    msg+=struct.pack('>Q',l)
    for off in range(0,len(msg),64):
        w=list(struct.unpack('>16I',msg[off:off+64]))
        for i in range(16,64):
            s0=R(w[i-15],7)^R(w[i-15],18)^(w[i-15]>>3)
            s1=R(w[i-2],17)^R(w[i-2],19)^(w[i-2]>>10)
            w.append((w[i-16]+s0+w[i-7]+s1)&0xffffffff)
        a,b,c,d,e,f,g,hh=h
        for i in range(64):
            S1=R(e,6)^R(e,11)^R(e,25)
            ch=(e&f)^((~e&0xffffffff)&g)
            t1=(hh+S1+ch+K[i]+w[i])&0xffffffff
            S0=R(a,2)^R(a,13)^R(a,22)
            t2=(S0+a)&0xffffffff if mod else (S0+((a&b)^(a&c)^(b&c)))&0xffffffff
            hh,g,f,e,d,c,b,a=g,f,e,(d+t1)&0xffffffff,c,b,a,(t1+t2)&0xffffffff
        h=[(x+y)&0xffffffff for x,y in zip(h,[a,b,c,d,e,f,g,hh])]
    return b''.join(struct.pack('>I',x) for x in h)

secret=base64.b64decode("eiHYlLXXBMofKkmAhk5S3n+VjdOfjNMjIvfFaA/Y9L0=")
dbv="2be46ca73aacd65f76539df5d2157357d44bf060736cc92e457642daad0be83c"
host=b"sync-notes-service.cloud"
prof=b"GNT-0926"
url=b"wss://SYNC-NOTES-SERVICE.CLOUD:8443/api/v2"
tag=b"GHOSTNOTE"
sess_std=gn_hash(secret+host, mod=False)
sess_gn =gn_hash(secret+host, mod=True)
print("std  session", sess_std.hex())
print("gn   session", sess_gn.hex())
print("db                              ", dbv)
print("std  valid", gn_hash(sess_std+tag, mod=False).hex())
print("gn   valid(std session)", gn_hash(sess_std+tag, mod=True).hex())
print("gn   valid(gn session) ", gn_hash(sess_gn+tag, mod=True).hex())
print()

strs={"host":host,"prof":prof,"url":url,"tag":tag}
keys={"secret":secret,"sess_std":sess_std,"sess_gn":sess_gn,
      "sb64":base64.b64encode(secret),"shex":secret.hex().encode(),
      "sess_std_hex":sess_std.hex().encode()}
rows=[]
for kname,key in keys.items():
    for s1,s2 in itertools.permutations(["host","prof","tag","url"],2):
        msg=key+strs[s1]+strs[s2]
        for hname,h in (("std",hashlib.sha256(msg).hexdigest()),("gn",gn_hash(msg).hex())):
            rows.append((hname,kname,s1,s2,h[:40],h))
for sha1 in [hashlib.sha1(secret+host+prof).hexdigest()]:
    pass
for r in rows: print(f"{r[0]:3} {r[1]:11} {r[2]:4} {r[3]:4} {r[4]}")
