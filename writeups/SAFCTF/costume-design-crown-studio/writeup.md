# SAFCTF — COSTUME DESIGN — CROWN STUDIO

- **Category:** Active Directory / AD CS
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `Flag recovered during the original solve; value not recorded`

## Objective

Abuse an Active Directory Certificate Services enrollment path to authenticate as another user and recover the flag.

## Solution path

1. Enumerated the certificate authority, certificate templates and enrollment permissions.
2. Found a template that allowed the subject/UPN to be supplied and requested a certificate for `archivist@orchard.test`.
3. Authenticated with the issued certificate and accessed the target user context.
4. Recovered the flag from that context (exact value was not preserved in the original notes).

## Result

`Flag recovered during the original solve; value not recorded`

## Key lesson

For AD CS CTFs, enumerate CAs, templates, enrollment rights, subject/UPN supply behavior, EKUs and authentication-capable certificates. A vulnerable template converts enrollment into domain authentication as another identity.
