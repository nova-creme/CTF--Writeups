# SAFCTF — Arcane, the Aftermath (500 pts)

- **Category:** OSINT / Web recon
- **Description:** Multi-hop investigation into a wiped corporate site to recover a secretly-preserved project.

## Commands run (in order)

```bash
# 1. View the "archived" homepage's raw HTML source for hidden comments
curl -s http://54.72.82.22:8345/
# → HTML comment revealed original hostname: www.piltover-tech.example
#   and mentioned archive partner "Hexvault"

# 2. Explore Hexvault
curl -s http://54.72.82.22:8345/hexvault/
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/
# → listed 2 snapshots: 20220601 (6 pages incl. orion, people) and 20230317

# 3. Pull pages from the earliest snapshot
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/20220601/
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/20220601/orion.html
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/20220601/people.html
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/20220601/careers.html
curl -s http://54.72.82.22:8345/hexvault/web/www.piltover-tech.example/20230317/orion.html
# → orion.html named "Project Director: Viktor Veylan"
# → people.html linked his code profile: "Code: cogforge / vveylan" → /cogforge/vveylan/

# 4. Cogforge profile → archived repo
curl -s http://54.72.82.22:8345/cogforge/vveylan/
curl -s http://54.72.82.22:8345/cogforge/vveylan/orion/
# → repo marked "archived", clone URL given

# 5. Clone and inspect both branches
git clone http://54.72.82.22:8345/cogforge/vveylan/orion.git
cd orion
git log --all --oneline --graph
git branch -a
# → two branches: main (clean) and mirror (pushed AFTER archive date)

git log --all -p | grep -i -B5 -A5 "safctf\|password\|secret\|key\|token\|credential"
# → found MIRROR file content:
#     "mirrored before they pulled the plug.
#      topside doesn't get to bury this one.
#      signed with the crew key. the keeper knows whose."

git checkout mirror
cat docs/DEPLOYMENT.md
# → Archive ID: PX-7319
#   "Classification is recorded on the architecture deck, not here."

git log --show-signature -1 66e0b2c
# → commit author "J <j@users.noreply.cogforge.example>"

# 6. Find "the architecture deck" — Viktor's conference talk slides
curl -s http://54.72.82.22:8345/hextech/
# → link: slides/veylan-building-infrastructure.pdf

curl -s http://54.72.82.22:8345/hextech/slides/veylan-building-infrastructure.pdf -o deck.pdf
file deck.pdf
pdftotext deck.pdf -
exiftool deck.pdf
# → Keywords: "ORION, Piltover, Zaun, PILTOVER-NORTH, classification HEXTECH-7"

# 7. Submit to Hexvault's sealed records (client-side SHA-256 of "ARCHIVEID:CLASSIFICATION")
curl -s http://54.72.82.22:8345/hexvault/records/
curl -s http://54.72.82.22:8345/sha256.js   # confirmed hashing algorithm used by the form

python3 -c "
import hashlib
key = ('PX-7319' + ':' + 'HEXTECH-7').upper()
print(hashlib.sha256(key.encode()).hexdigest())
"
# → cde19ad8094f414548d57e3ba3b2b270570d8c7d8d820fbc348afa3514ce6063

curl -s http://54.72.82.22:8345/hexvault/records/cde19ad8094f414548d57e3ba3b2b270570d8c7d8d820fbc348afa3514ce6063.html
# → Incident report: Viktor cleared; mirror push signed with an unverified
#   Zaun Systems key, sig-id ZS1-4E7B-9A2C, author initial "J" only.
#   fingerprint: 7F3A 9C1E 44B0 D2E8 1A6F  B3C9 0E57 2D48 86A1 5F3B

# 8. Follow lead to Zaun Systems' crew page
curl -s http://54.72.82.22:8345/zaun/
curl -s http://54.72.82.22:8345/zaun/crew.html
# → "Eko: keeper of the crew keyring" with a public keys.txt and verify.html

curl -s http://54.72.82.22:8345/zaun/keys.txt
# → matched the exact fingerprint to alias "jynx" (not decoy "jek", a rotated/retired key)

curl -s http://54.72.82.22:8345/zaun/verify.html
# → confirmed form hashes (SIGID:ALIAS).upper() with the same sha256.js

python3 -c "
import hashlib
sig = 'ZS1-4E7B-9A2C'.upper().replace(' ','')
alias = 'jynx'.upper().replace(' ','')
print(hashlib.sha256((sig + ':' + alias).encode()).hexdigest())
"
# → 4e5eb63f3bc6c28b2304a7c74647dcd6c354c08b6104e148298a129154f2796c

curl -s http://54.72.82.22:8345/zaun/verify/4e5eb63f3bc6c28b2304a7c74647dcd6c354c08b6104e148298a129154f2796c.html
```
→ `"VERIFIED ... ZS1-4E7B-9A2C → jynx"` — message from jynx plus the flag.

## Flag

```
safctf{92890a18-9192-4627-b464-306797af13b0}
```
