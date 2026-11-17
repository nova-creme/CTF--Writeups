# Recognition (Stage 5 — boss)
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT (450 pts)
* **Difficulty:** Hard
* **Flag:** `safctf{recognition_e5}`

## Objective
Cross-reference three independent sources to identify the real person behind `outis-k` and submit name, camera serial and domain.

## Reconnaissance & Methodology
1. Tools used: `curl` (GET + POST); leads from Stages 2 and 4.
2. **Argonaut**: `GET /argonaut/find?email=otho@nostos-labs.example` (email from git commit author) → redirect to `/argonaut/in/o-k-7f3a` → profile "O. K.", Security Contractor.
3. **Drachma Market**: `GET /market?q=6021743` (serial from Stage 2 EXIF) → listing `L-1041` → seller `/market/seller/otho_k` → review text names **"Otho Kallistratos"**.
4. **The Oracle**: `GET /oracle?domain=nostos-labs.example` (current record redacted) then `/oracle/history?domain=nostos-labs.example` → original 2022 registration: registrant Otho Kallistratos, email `otho@nostos-labs.example`.

## Solution & Exploitation
* Final payload:
  ```bash
  curl -X POST http://54.72.82.22:8098/recognition \
    -d "name=Otho Kallistratos" -d "serial=6021743" -d "domain=nostos-labs.example"
  ```
* → `"Recognized. Every artefact points to the same person."` + `safctf{recognition_e5}`.
