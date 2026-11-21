# COSTUME DESIGN — CROWN STUDIO
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Active Directory / AD CS
* **Difficulty:** Not recorded
* **Flag:** `Flag recovered during the original solve; value not recorded`

## Objective
Abuse an Active Directory Certificate Services enrollment path to authenticate as another user and recover the flag.

## Reconnaissance & Methodology
1. Enumerated the certificate authority, certificate templates and enrollment permissions.
2. Found a template that allowed the subject/UPN to be supplied and requested a certificate for `archivist@orchard.test`.
3. Authenticated with the issued certificate and accessed the target user context.
4. Recovered the flag from that context (exact value was not preserved in the original notes).

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `Flag recovered during the original solve; value not recorded`
