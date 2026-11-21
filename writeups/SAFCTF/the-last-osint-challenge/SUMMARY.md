# The Last OSINT Challenge
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT / data parsing
* **Difficulty:** Not recorded
* **Flag:** `Final flag value not recorded (`safctf{test_flag_12345}` was only a formatting test)`

## Objective
Correlate maritime logs to isolate a geographic anomaly and secure the final flag.

## Reconnaissance & Methodology
1. Parsed `voyages.json` alongside `tide-station.csv`.
2. Cross-referenced vessel identifiers with tide-gauge metadata and pier notes.
3. Isolated the geographic anomaly required by the challenge.
4. Used `safctf{test_flag_12345}` only to verify API submission formatting; the real flag value was not preserved.

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `Final flag value not recorded (`safctf{test_flag_12345}` was only a formatting test)`
