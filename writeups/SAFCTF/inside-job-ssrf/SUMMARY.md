# Inside Job (SSRF) — "Orbit Dispatch"
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Web (SSRF with blocklist bypass)
* **Difficulty:** Medium
* **Flag:** `safctf{9f3a458f3a26e6372b5b5467e3e51edf}`

## Objective
Abuse a "URL to fetch" feature that returns response headers, status and a body preview to reach internal services and retrieve the flag.

## Reconnaissance & Methodology
1. Tools used: `curl`/browser on the fetch form; JSON response previews as an SSRF oracle.
2. Baseline: `https://example.com` worked; `http://127.0.0.1/`, `http://localhost/`, `http://127.0.0.1:80/` all returned `{"error":"url blocked by policy"}` — a string-based blocklist.
3. Bypass with alternate loopback representations: `0.0.0.0`, `127.1`, `0x7f.0x0.0x0.0x1` all passed the filter (DNS-based `127.0.0.1.nip.io` was blocked); the resulting `Connection refused` error confirmed real outbound requests were made.
4. Port scan through the `0.0.0.0` bypass: `:5000` (nothing useful), `:8000` (Flask/Werkzeug homepage), `:9000` (bare `BaseHTTPServer` returning `{"status_code":404,"preview":"Not found"}` on `/`, proving real routes existed).

## Solution & Exploitation
* Path-guessed on the live internal service: `http://0.0.0.0:9000/flag` → flag in the response preview.
* Final payload: `http://0.0.0.0:9000/flag` via the fetch field → `safctf{9f3a458f3a26e6372b5b5467e3e51edf}`.
* Root cause: blocklist matched specific hostname strings but not equivalent loopback notations, enabling internal port scanning and access to an unauthenticated internal service.
