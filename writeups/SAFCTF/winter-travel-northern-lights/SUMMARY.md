# WINTER TRAVEL — NORTHERN LIGHTS
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Crypto / Web (AES-GCM key derivation)
* **Difficulty:** Not recorded
* **Flag:** `safctf{3fd96340be891c629f7e3f3a42202743}`

## Objective
Decrypt a receipt-protected payload by deriving the AES-GCM key from material exposed by the web application.

## Reconnaissance & Methodology
1. Enumerated the web application and located the receipt/encrypted payload.
2. Identified the AES-GCM parameters: nonce/IV, ciphertext and authentication tag.
3. Traced how the exposed application data generated the AES-GCM key instead of attacking AES-GCM itself.
4. Reconstructed the decryption operation and decrypted the receipt to obtain the flag.

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `safctf{3fd96340be891c629f7e3f3a42202743}`
