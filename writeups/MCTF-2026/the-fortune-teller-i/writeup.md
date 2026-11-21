# MCTF 2026 — The Fortune Teller (I)

- **Category:** Reversing (binary patching)
- **Source:** reconstructed from session artifacts and confirmed flag submissions
- **Flag:** `MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}`

## Objective

Patch a fortune-telling binary so the unworthy path falls through to the routine that prints the decrypted fortune.

## Solution path

1. Disassembled `fortuneteller`; identified `main`, `gen1`–`gen4` and the global `worthy` at `0x40403c` (`.bss`, never written).
2. Located the `gen3` check at `0x40159a`: `jne 0x4015a2` falls through to the “not worthy” branch and `exit(1)`.
3. Patched file offset `0x15a2` from `0x75` (`jne`) to `0xeb` (`jmp`).
4. Built a stub `sleep()` shared object and ran with `LD_PRELOAD=/tmp/nosleep.so /tmp/fortuneteller_patched` so `gen4` printed the fortune immediately.

## Result

`MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}`

## Key lesson

Check `.bss` globals that gate success: if nothing writes them, a one-byte conditional-jump patch is often sufficient.
