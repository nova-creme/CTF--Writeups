# Alcinous Hall's Window (Stage 3)
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT / geolocation (300 pts)
* **Difficulty:** Medium
* **Flag:** `safctf{alcinous_window_c3}`

## Objective
Use the GPS coordinates from Stage 2 to identify a building on the Ithaca Atlas map and confirm it to earn the third flag.

## Reconnaissance & Methodology
1. Tools used: `curl` (GET and POST).
2. `GET /atlas/reverse?lat=38%2030%2024.58%20N&lon=40%2029%2031.07%20W` confirmed the cafe as "Calypso's Rest Cafe" and returned the full map SVG, including a labeled POI: **"Alcinous Hall - 41 Ithaca St"**.
3. `GET /atlas/confirm` revealed a form expecting a `building` POST field.

## Solution & Exploitation
* Final payload: `curl -X POST http://54.72.82.22:8098/atlas/confirm -d "building=Alcinous Hall"` → `"Confirmed. The IR lead has verified the location."` + `safctf{alcinous_window_c3}`.
