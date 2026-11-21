# SAFCTF — The Last OSINT Challenge

- **Category:** OSINT / data parsing
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `Final flag value not recorded (`safctf{test_flag_12345}` was only a formatting test)`

## Objective

Correlate maritime logs to isolate a geographic anomaly and secure the final flag.

## Solution path

1. Parsed `voyages.json` alongside `tide-station.csv`.
2. Cross-referenced vessel identifiers with tide-gauge metadata and pier notes.
3. Isolated the geographic anomaly required by the challenge.
4. Used `safctf{test_flag_12345}` only to verify API submission formatting; the real flag value was not preserved.

## Result

`Final flag value not recorded (`safctf{test_flag_12345}` was only a formatting test)`

## Key lesson

Structured-log correlation often hinges on join keys that look mundane (vessel IDs, station IDs, pier notes); a test flag should never be mistaken for the real result.
