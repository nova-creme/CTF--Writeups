# OSINT Chain Stage 1 — Trail of Outis (100 pts)

**Flag:** `safctf{trail_of_outis_a1}`

## Commands run

```bash
cat portal-audit.log
# Spotted the anomalous entries near the end:
#   203.0.113.58  curl/8.4.0  password spray 40 attempts
#   203.0.113.58  user=svc-steward  "stale contractor credential"
#   203.0.113.58  POST /admin/motd  x_contact="outis-k"
#       msg="The hall went dark at midnight. ... -- outis-k"

curl -s http://54.72.82.22:8098/agora/u/outis-k
# → Bio: "ex-security at Ithaca Systems", pinned post matching incident timing

curl -s http://54.72.82.22:8098/agora/u/outis-k/links
```
→ The Links page contained a "Site verification" card with the flag labeled directly.
