# SAFCTF — WINTER TRAVEL — NORTHERN LIGHTS

- **Category:** Crypto / Web (AES-GCM key derivation)
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `safctf{3fd96340be891c629f7e3f3a42202743}`

## Objective

Decrypt a receipt-protected payload by deriving the AES-GCM key from material exposed by the web application.

## Solution path

1. Enumerated the web application and located the receipt/encrypted payload.
2. Identified the AES-GCM parameters: nonce/IV, ciphertext and authentication tag.
3. Traced how the exposed application data generated the AES-GCM key instead of attacking AES-GCM itself.
4. Reconstructed the decryption operation and decrypted the receipt to obtain the flag.

## Result

`safctf{3fd96340be891c629f7e3f3a42202743}`

## Key lesson

When ciphertext, nonce/IV and tag are published alongside apparently unrelated application data, inspect key derivation — the weakness is usually there, not in AES-GCM.
