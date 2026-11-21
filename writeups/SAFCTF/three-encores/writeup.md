# SAFCTF — Three Encores

- **Category:** Crypto / API submission
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `safctf{dadb56ae-eede-422e-87cb-744462cdfda0} (intermediate item — rejected by scoreboard)`

## Objective

Decrypt a collection receipt and submit it to the correct validation endpoint.

## Solution path

1. Decrypted the collection receipt to obtain a UUID-formatted flag.
2. Submitted it to the main scoreboard, which rejected it because it was only an intermediate item.
3. Submitted the same receipt payload directly to the challenge API validation endpoint to complete the objective.

## Result

`safctf{dadb56ae-eede-422e-87cb-744462cdfda0} (intermediate item — rejected by scoreboard)`

## Key lesson

Distinguish the scoreboard from the challenge validation endpoint. An intermediate-looking flag may still be the right ciphertext — just not for the main submission form.
