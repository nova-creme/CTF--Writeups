# Twist Me A Twister
* **Platform/Event:** TVX CTF
* **Category:** Reverse Engineering (310 pts)
* **Difficulty:** Medium
* **Flag:** `TVX{Fl4ggy_fl4g_fl4g_tw15ty_tw15t_tw15t}`

## Objective
Recover the flag from a 4.6 KB .NET assembly without ilspy/mono/dotnet installed.

## Reconnaissance & Methodology
1. Tools used: `file`, `strings`, `dnfile` + `dncil` (pip-installed with `--break-system-packages`), a custom CIL disassembler (`cildis.py`).
2. With no .NET tooling available, parsed the CLR metadata and disassembled the CIL directly with Python.
3. `Main` prompts `flag> ` and compares input to `Reveal()` — the flag **is** `Reveal()`'s output.
4. `Reveal()` decodes a 40-byte static array from the PE `FieldRva` table: `j = (i*7+3) % 40`; `out[i] = ror8(data[j], j%5+1) ^ ((55 + j*11) & 0xFF)`.

## Solution & Exploitation
* Final payload: read the FieldRVA blob with `dnfile`, apply the per-index permutation + rotate-right + XOR — clean ASCII output.
* The `.exe` was never executed; everything was recovered statically.
* Gotcha: the helper script must not be named `dis.py` (shadows the stdlib `dis` module via `inspect`/`dataclasses`/`py7zr`) — renamed to `cildis.py`.
