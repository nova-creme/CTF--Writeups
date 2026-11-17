# Summer Is Over
* **Platform/Event:** TVX CTF
* **Category:** Reverse Engineering (240 pts)
* **Difficulty:** Medium
* **Flag:** `TVX{4nd_S0_7h3_5un_Sh1n35}`

## Objective
Recover the flag from another small .NET assembly whose `Main` compares input to `Reveal()`.

## Reconnaissance & Methodology
1. Tools used: `file`, `strings` (ASCII + UTF-16), `dnfile`/`dncil` and the same `cildis.py` CIL disassembler.
2. Two static arrays: `blob` (26 bytes) and `schedule` (8 bytes), located via `FieldRva` table rows.
3. Reversed `Reveal()`: for each `i` in 0..25 — read `blob[(i*5+1)%26]`; XOR `(51+11*i)&0xFF`; XOR `schedule[i%8]`; subtract `(3*i*i+25)&0xFF`; ROR by `i%5+1`; XOR `(33+7*i)&0xFF`.
4. Final step: reverse every group of 4 bytes in place (last group of 2 is reversed too).

## Solution & Exploitation
* Final payload: the Python reconstruction in `writeup.md` reads both FieldRVA blobs and applies the 6-step transform + 4-byte group reversal → `TVX{4nd_S0_7h3_5un_Sh1n35}`.
* Same static-only approach as Twist Me A Twister — the binary was never run.
