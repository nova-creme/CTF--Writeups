# Arcane, the Aftermath
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT / Web recon (500 pts)
* **Difficulty:** Hard
* **Flag:** `safctf{92890a18-9192-4627-b464-306797af13b0}`

## Objective
Investigate a wiped corporate site (Piltover Tech) through archive snapshots, git history, PDF metadata and signed-record lookups to recover a secretly preserved project and the flag.

## Reconnaissance & Methodology
1. Tools used: `curl`, `git` (`log --all`, `branch -a`, `checkout`, `show-signature`), `pdftotext`, `exiftool`, `file`, Python `hashlib`.
2. HTML comment on the archived homepage revealed the original host `www.piltover-tech.example` and archive partner **Hexvault**.
3. Hexvault snapshots `20220601` / `20230317`: `orion.html` named "Project Director: Viktor Veylan"; `people.html` linked `cogforge/vveylan`.
4. Cogforge `orion.git` had a clean `main` and a `mirror` branch pushed after the archive date; the mirror's `MIRROR` file and `docs/DEPLOYMENT.md` gave Archive ID `PX-7319` and the hint "Classification is recorded on the architecture deck". Signed commit author: `J <j@users.noreply.cogforge.example>`.
5. Hextech slide deck `veylan-building-infrastructure.pdf` → PDF Keywords gave classification `HEXTECH-7`.
6. Sealed records use client-side SHA-256 of `("PX-7319:HEXTECH-7").upper()` → `cde19ad8…6063`; the incident report named sig-id `ZS1-4E7B-9A2C`, author "J", fingerprint `7F3A 9C1E 44B0 D2E8 1A6F B3C9 0E57 2D48 86A1 5F3B`.
7. Zaun crew page: `keys.txt` matched that fingerprint to alias **`jynx`** (not rotated decoy `jek`). Verify form hashes `("ZS1-4E7B-9A2C:JYNX").upper()` → `4e5eb63f…96c`.

## Solution & Exploitation
* Final payload: `GET /zaun/verify/4e5eb63f3bc6c28b2304a7c74647dcd6c354c08b6104e148298a129154f2796c.html` → `"VERIFIED ... ZS1-4E7B-9A2C → jynx"` plus `safctf{92890a18-9192-4627-b464-306797af13b0}`.
* Two client-side SHA-256 gates: `sha256(upper("ARCHIVEID:CLASSIFICATION"))` and `sha256(upper("SIGID:ALIAS"))` — read `sha256.js` to confirm the exact hashing convention.
