# Citrus Proof (Web, JWT role escalation) — IN PROGRESS

**Status:** unsolved — signature validation confirmed; HS256 secret not found.

```bash
curl -s -X POST http://54.72.82.22:8320/api/session -H "Content-Type: application/json" -d '{}'
# → always returns the same static visitor-role JWT:
#   eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJyb2xlIjogInZpc2l0b3IifQ.DSqPy-NslHpsP1xtXyflSfqRMbO0f0d2dH6Zsfof9ws

curl -s -X POST http://54.72.82.22:8320/api/proof -H "Content-Type: application/json" \
  -H "Authorization: Bearer <visitor token>" -d '{"layout":"test"}'
# → {"message":"The request could not be completed.","ok":false}  (role-gated, signature valid)

# Attempts that failed (all returned {"message":"Request unavailable."} — signature rejected):
#  - alg:none forged token (and case variants None/NONE/nOnE)
#  - kid injection pointing at /dev/null and path-traversal variants
#  - stripped-signature token (alg kept as HS256, signature segment emptied)

# Secret-cracking attempts (all failed — no match found):
python3 -c "
import jwt
token = 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJyb2xlIjogInZpc2l0b3IifQ.DSqPy-NslHpsP1xtXyflSfqRMbO0f0d2dH6Zsfof9ws'
for secret in ['secret','password','citrus','proof','safaricom']:
    try:
        print('FOUND:', secret, jwt.decode(token, secret, algorithms=['HS256']))
    except Exception: pass
"
# Also tried: jwt-secrets GitHub wordlist (jwt.secrets.list), jwt_tool's jwt-common.txt,
# a rockyou.txt brute-force (in progress / inconclusive), theme-word permutations.

# Found /submit and /health via gobuster:
gobuster dir -u http://54.72.82.22:8320 -w /usr/share/wordlists/dirb/common.txt -t 30
curl -s http://54.72.82.22:8320/health   # {"status":"ok"}
curl -s -X POST http://54.72.82.22:8320/submit -d '{"layout":"test"}'
# → same role-gated rejection as /api/proof

curl -s -X OPTIONS http://54.72.82.22:8320/api/session -i
curl -s -X OPTIONS http://54.72.82.22:8320/api/proof -i
# → Allow: HEAD, OPTIONS, POST, GET, PATCH  (GET/PATCH on /api/session returned the
#   same static token regardless of input — dead end)
```

**Status:** Confirmed the server validates signatures properly (rules out
`alg:none`/`kid` tricks); the HS256 secret has not been found via wordlists tried
so far.
