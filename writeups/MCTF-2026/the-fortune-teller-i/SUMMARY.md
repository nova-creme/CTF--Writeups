# The Fortune Teller (I)
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Reversing (binary patching)
* **Difficulty:** Medium
* **Flag:** `MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}`

## Objective
Patch a fortune-telling binary so the unworthy path falls through to the routine that prints the decrypted fortune.

## Reconnaissance & Methodology
1. Disassembled `fortuneteller`; identified `main`, `gen1`–`gen4` and the global `worthy` at `0x40403c` (`.bss`, never written).
2. Located the `gen3` check at `0x40159a`: `jne 0x4015a2` falls through to the “not worthy” branch and `exit(1)`.
3. Patched file offset `0x15a2` from `0x75` (`jne`) to `0xeb` (`jmp`).
4. Built a stub `sleep()` shared object and ran with `LD_PRELOAD=/tmp/nosleep.so /tmp/fortuneteller_patched` so `gen4` printed the fortune immediately.

## Solution & Exploitation
* Because `worthy` is never set, the check always fails. Inverting the conditional jump and skipping sleeps makes the binary reveal the flag without implementing the intended input.
* Final flag: `MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}`
