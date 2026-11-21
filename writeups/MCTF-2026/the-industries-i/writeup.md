---
title: "The Industries (I)"
ctf: "MCTF26"
date: 2026-11-20
category: web
difficulty: easy
points: 1000
flag_format: "MCTF26{...}"
author: "novacreme"
---

# The Industries (I)

## Summary

The Flask site put the user's role in a plain base64 cookie. Setting the cookie to
base64("admin") unlocked `/admin`, and the flag was split across two HTML comments:
the prefix in `/history` and the suffix in `/admin`.

## Solution

### Step 1: Forge the role cookie

The homepage set `Set-Cookie: role=Z3Vlc3Q=` (base64 of `guest`). The navigation
comment hinted that admin API access still depended on that link. Replacing the
cookie with `YWRtaW4=` (base64 of `admin`) changes `/admin` from 403 to 200.

### Step 2: Combine the two comment halves

`/history` contains:

```html
<!-- ... I'll just leave half of my password here ... MCTF26{w3Lc0m3_ -->
```

`/admin` (with the forged cookie) contains:

```html
<div class="flag">t0_Th3_Gu1ld}</div>
```

Concatenating them gives the flag.

## Flag

```
MCTF26{w3Lc0m3_t0_Th3_Gu1ld}
```
