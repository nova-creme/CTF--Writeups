# OSINT Chain Stage 5 — Recognition (450 pts, boss stage)

**Flag:** `safctf{recognition_e5}`

## Commands run

```bash
# Argonaut — search by email found in git commit author field
curl -s "http://54.72.82.22:8098/argonaut/find?email=otho@nostos-labs.example"
# → redirected to /argonaut/in/o-k-7f3a
curl -s http://54.72.82.22:8098/argonaut/in/o-k-7f3a
# → profile "O. K.", Security Contractor, bio matching suspect

# Drachma Market — search by the camera serial number from Stage 2
curl -s "http://54.72.82.22:8098/market?q=6021743"
curl -s http://54.72.82.22:8098/market/listing/L-1041
# → seller link: /market/seller/otho_k
curl -s "http://54.72.82.22:8098/market/seller/otho_k"
# → review text names him directly: "Otho Kallistratos"

# The Oracle — WHOIS-style lookup, including history (current record was redacted)
curl -s "http://54.72.82.22:8098/oracle?domain=nostos-labs.example"
curl -s "http://54.72.82.22:8098/oracle/history?domain=nostos-labs.example"
# → original 2022 registration: Registrant: Otho Kallistratos, Email: otho@nostos-labs.example

# Final submission — cross-referencing all three confirmed facts
curl -s -X POST http://54.72.82.22:8098/recognition \
  -d "name=Otho Kallistratos" \
  -d "serial=6021743" \
  -d "domain=nostos-labs.example"
```
→ `"Recognized. Every artefact points to the same person."` + flag.
