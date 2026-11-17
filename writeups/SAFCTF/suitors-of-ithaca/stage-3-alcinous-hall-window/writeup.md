# OSINT Chain Stage 3 — Alcinous Hall's Window (300 pts)

**Flag:** `safctf{alcinous_window_c3}`

## Commands run

```bash
curl -s "http://54.72.82.22:8098/atlas/reverse?lat=38%2030%2024.58%20N&lon=40%2029%2031.07%20W"
# → confirmed cafe location on the map (Calypso's Rest Cafe) and
#   revealed the full map SVG, including a labeled POI: "Alcinous Hall - 41 Ithaca St"

curl -s http://54.72.82.22:8098/atlas/confirm
# → showed the confirm form (expects a "building" POST field)

curl -s -X POST http://54.72.82.22:8098/atlas/confirm \
  -d "building=Alcinous Hall"
```
→ `"Confirmed. The IR lead has verified the location."` + flag shown directly.
