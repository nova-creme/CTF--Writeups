# Trail of Outis (Stage 1)
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT (100 pts)
* **Difficulty:** Easy
* **Flag:** `safctf{trail_of_outis_a1}`

## Objective
Identify the handle behind an intrusion from `portal-audit.log` and find the first flag on a mock social platform.

## Reconnaissance & Methodology
1. Tools used: `cat`, `curl`.
2. `portal-audit.log` contained anomalous entries: `203.0.113.58` with `curl/8.4.0`, a 40-attempt password spray, use of `svc-steward` ("stale contractor credential"), and `POST /admin/motd` with `x_contact="outis-k"` and the message "The hall went dark at midnight. ... -- outis-k".
3. `curl http://54.72.82.22:8098/agora/u/outis-k` → bio "ex-security at Ithaca Systems", pinned post matching the incident timing.

## Solution & Exploitation
* `curl http://54.72.82.22:8098/agora/u/outis-k/links` → the "Site verification" card labeled the flag directly: `safctf{trail_of_outis_a1}`.
