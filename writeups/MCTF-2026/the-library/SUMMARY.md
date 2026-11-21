# The Library
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Web (crawling)
* **Difficulty:** Medium
* **Flag:** `MCTF26{tH3_s34rCh_h45_p41D_0ff}`

## Objective
Find a flag hidden somewhere in a binary maze of roughly 14,000 single-hex-named PHP pages.

## Reconnaissance & Methodology
1. Enumerated the entry page (`abed06cac40c9480.php`) and discovered links to 16-hex `.php` pages.
2. Wrote an async BFS crawler using `aiohttp` with a semaphore of about 80 to follow `href="[a-f0-9]{16}\.php"` links.
3. Recorded each page heading into `lib_map.json`; the live regex looked for `MCTF{` and missed `MCTF26{`, but the saved map preserved the hit.
4. Flagged page `10fc184c0d0db821.php` contained the red-and-green book and the flag.
5. Used `ffuf` plus follow-up link/header scripts for recon and verification.

## Solution & Exploitation
* The maze grows as 2^n through linked 16-hex pages. A breadth-first crawl is the intended scalable approach; the flag page heading was preserved even though the live regex was too narrow.
* Final flag: `MCTF26{tH3_s34rCh_h45_p41D_0ff}`
