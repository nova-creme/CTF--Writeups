# Three Encores
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Crypto / API submission
* **Difficulty:** Not recorded
* **Flag:** `safctf{dadb56ae-eede-422e-87cb-744462cdfda0} (intermediate item — rejected by scoreboard)`

## Objective
Decrypt a collection receipt and submit it to the correct validation endpoint.

## Reconnaissance & Methodology
1. Decrypted the collection receipt to obtain a UUID-formatted flag.
2. Submitted it to the main scoreboard, which rejected it because it was only an intermediate item.
3. Submitted the same receipt payload directly to the challenge API validation endpoint to complete the objective.

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `safctf{dadb56ae-eede-422e-87cb-744462cdfda0} (intermediate item — rejected by scoreboard)`
