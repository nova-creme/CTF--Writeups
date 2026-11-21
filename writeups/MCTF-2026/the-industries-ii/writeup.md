---
title: "The Industries (II)"
ctf: "MCTF26"
date: 2026-11-20
category: web
difficulty: easy
points: 1000
flag_format: "MCTF26{...}"
author: "novacreme"
---

# The Industries (II)

## Summary

The rebuilt site replaced the base64 role cookie with a Flask signed session and a
login form. The administrator credentials were still `admin:admin`, and the "psychic"
defense is only a client-side popup — after logging in, the flag is in `/admin`.

## Solution

### Step 1: Log in

`/admin` redirects to `/login`, which POSTs `username` and `password` to `/login`.
Trying the default pair works:

```
POST /login
username=admin&password=admin
```

Response: `302` with `Set-Cookie: session=...; HttpOnly; Path=/` and a redirect to `/admin`.

### Step 2: Read the flag

The authenticated `/admin` page contains:

```html
<div class="flag">MCTF26{p5ycH1c_d3S7R0y3d}</div>
```

The "Psychic Attack" popup injected into pages is cosmetic JavaScript (`setTimeout`
with a random 3–6 second delay) and does not affect the server-side session.

## Flag

```
MCTF26{p5ycH1c_d3S7R0y3d}
```
