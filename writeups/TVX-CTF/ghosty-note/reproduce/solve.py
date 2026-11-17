#!/usr/bin/env python3
"""
TVX CTF - Ghosty note (forensics)
Reconstruct the GhostNote flag from the triage package.

Chain (from NotionUpdate.exe exports):
  decodeServer()       : XOR 0x37 on the embedded strings
  getC2(i)             : three candidate C2 URLs
  deriveSession()      : sha256(deviceSecret_raw32 || host)
  validationDigest()   : sha256(session || "GHOSTNOTE")  -> matches vault.db config
  finalFlagDigest()    : sha256(session || host || profile) -> first 20 bytes -> flag
"""
import base64, hashlib, sqlite3

BASE = "GhostNote"

# --- 1. identity (deviceSecret) from the Notion vault -----------------------
db = sqlite3.connect(f"{BASE}/Users/john/AppData/Roaming/Notion/vault.db")
secret_b64 = db.execute("select secret from identity where name='deviceSecret'").fetchone()[0]
db_validation = db.execute("select value from config where name='serverValidation'").fetchone()[0]
secret = base64.b64decode(secret_b64)

# --- 2. campaign profile from NTUSER.DAT (UTF-16LE) -------------------------
reg = open(f"{BASE}/Users/john/NTUSER.DAT.reg", "rb").read().decode("utf-16-le")
profile = [l.split('=')[1].strip('"') for l in reg.splitlines() if "SyncProfile" in l][0]

# --- 3. C2 candidates decoded from NotionUpdate.exe (.rdata, XOR 0x37) ------
enc = [
 "40 44 44 0d 18 18 59 58 43 5e 58 59 1a 56 44 44 52 43 44 1a 54 53 59 19 54 58 5a 0d 0e 03 03 04 18 42 47 53 56 43 52 37",
 "40 44 44 0d 18 18 64 6e 79 74 1a 79 78 63 72 64 1a 64 72 65 61 7e 74 72 19 74 7b 78 62 73 0d 0f 03 03 04 18 56 47 5e 18 41 05 37",
 "40 44 44 0d 18 18 59 58 43 52 44 1a 52 53 50 52 1a 54 56 54 5f 52 19 59 52 43 0d 03 03 04 18 44 4e 59 54 37",
]
urls = [bytes(int(b,16) ^ 0x37 for b in s.split()).rstrip(b"\x00").decode() for s in enc]
hosts = [u.split("://",1)[1].split("/",1)[0].rsplit(":",1)[0].lower() for u in urls]
tag = "GHOSTNOTE"

# --- 4. pick the host whose derived session validates ----------------------
session = host = None
for u, h in zip(urls, hosts):
    s = hashlib.sha256(secret + h.encode()).digest()
    if hashlib.sha256(s + tag.encode()).hexdigest() == db_validation:
        session, host = s, h
        print(f"[+] valid C2 {u}  host={h}")
        break
assert session, "no C2 validated"

print("[+] profile       :", profile)
print("[+] validation    :", hashlib.sha256(session + tag.encode()).hexdigest())

# --- 5. final flag digest --------------------------------------------------
digest = hashlib.sha256(session + host.encode() + profile.encode()).hexdigest()
print("[+] final digest  :", digest)
print("[+] FLAG          : Tvx{%s}" % digest[:40])
