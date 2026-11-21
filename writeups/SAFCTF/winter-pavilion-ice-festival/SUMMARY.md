# WINTER PAVILION — ICE FESTIVAL
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** Active Directory / Group Policy
* **Difficulty:** Not recorded
* **Flag:** `safctf{8a97f3881e4828d37406ed0953ff9573}`

## Objective
Follow a chain of Group Policy objects and permissions to reach the privileged resource holding the flag.

## Reconnaissance & Methodology
1. Established an initial foothold and enumerated domain Group Policy objects.
2. Identified a writable/interesting policy rather than treating the first accessible GPO as the goal.
3. Followed linked policies through successive privileged configurations.
4. Reached the final resource and read the flag.

## Solution & Exploitation
* See [`writeup.md`](writeup.md) for the full reconstructed solution path.
* **Flag:** `safctf{8a97f3881e4828d37406ed0953ff9573}`
