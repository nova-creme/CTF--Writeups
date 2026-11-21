---
title: "The Library"
ctf: "MCTF 2026"
date: 2026-11-20
category: web
difficulty: medium
points: 1000
flag_format: "MCTF26{...}"
---

# The Library

## Summary

A binary maze of roughly 14,000 sixteen-hex-named PHP pages hides one flag-bearing page. An asynchronous breadth-first crawl from the entry page preserves every page heading, which is where the flag survives even though the live regex missed it.

## Solution

### Step 1: Crawl the binary maze

Each page links to exactly two children, so the frontier doubles at every level. Follow `href="[a-f0-9]{16}\.php"` links with a bounded async crawler and store each page's `<h1>` heading to `lib_map.json`.

```python
import asyncio, aiohttp, re, json, time

BASE = "http://10.240.27.178/"
START = "abed06cac40c9480.php"
SEM = asyncio.Semaphore(80)

async def fetch(session, path):
    async with SEM:
        for attempt in range(3):
            try:
                async with session.get(BASE + path,
                        timeout=aiohttp.ClientTimeout(total=15)) as r:
                    return path, r.status, await r.text()
            except Exception:
                await asyncio.sleep(0.2 * (attempt + 1))
    return path, 0, ""

def links(html):
    return re.findall(r'href="([a-f0-9]{16}\.php)"', html)

def heading(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''

async def main():
    visited, headings, frontier = set(), {}, [START]
    async with aiohttp.ClientSession() as session:
        for depth in range(18):
            if not frontier:
                break
            results = await asyncio.gather(
                *(fetch(session, p) for p in frontier if p not in visited))
            nxt = []
            for path, status, body in results:
                if path in visited:
                    continue
                visited.add(path)
                headings[path] = heading(body)
                if "MCTF26{" in body:
                    print("FOUND", path, heading(body))
                nxt += [l for l in links(body) if l not in visited]
            frontier = nxt
    with open("lib_map.json", "w") as f:
        json.dump(headings, f, indent=1)

asyncio.run(main())
```

### Step 2: Read the saved headings

The crawler's live check looked for `MCTF{` and therefore missed `MCTF26{...}`. Searching the persisted `lib_map.json` finds the heading of page `10fc184c0d0db821.php`:

```
a suspicious looking red-and-green book ... MCTF26{tH3_s34rCh_h45_p41D_0ff}
```

## Flag

```
MCTF26{tH3_s34rCh_h45_p41D_0ff}
```
