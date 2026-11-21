# SAFCTF — WINTER PAVILION — ICE FESTIVAL

- **Category:** Active Directory / Group Policy
- **Source:** reconstructed from `Documents/CTF-SOLNS.odt` (original solve notes)
- **Flag:** `safctf{8a97f3881e4828d37406ed0953ff9573}`

## Objective

Follow a chain of Group Policy objects and permissions to reach the privileged resource holding the flag.

## Solution path

1. Established an initial foothold and enumerated domain Group Policy objects.
2. Identified a writable/interesting policy rather than treating the first accessible GPO as the goal.
3. Followed linked policies through successive privileged configurations.
4. Reached the final resource and read the flag.

## Result

`safctf{8a97f3881e4828d37406ed0953ff9573}`

## Key lesson

GPO-chain challenges reward following links and delegated permissions step by step; the first writable policy is an entry point, not the finish line.
