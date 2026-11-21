---
title: "All Your Base Are Belong To Us"
ctf: "MCTF 2026"
date: 2026-11-20
category: crypto
difficulty: easy
points: N/A
flag_format: "MCTF26{...}"
---

# All Your Base Are Belong To Us

## Summary

The challenge file `/home/novacreme/Downloads/galaxy/flag.txt` stores the flag encoded
character-by-character across lines: line 1 is a unary count, and each following line is
that character's ASCII value written in the base equal to its 1-based line number.

## Solution

### Step 1: Decode the unary line

Line 1 holds a run of `1`s whose length is the ASCII code: 77 ones → `M`.

### Step 2: Decode the base lines

Each subsequent line `N` is the ASCII code of the flag character expressed in base N and
converted back to an integer.

### Step 3: Reassemble

Prepend the `MCTF26{` prefix and append the closing brace, then join the decoded characters.

**Run (`cat` + python):**

```bash
cat /home/novacreme/Downloads/galaxy/flag.txt
```

```python
with open("/home/novacreme/Downloads/galaxy/flag.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

flag = [chr(len(lines[0]))]  # Line 1: unary count = 77 ('M')
for base in range(2, len(lines) + 1):
    flag.append(chr(int(lines[base - 1], base)))

print("".join(flag))
```

## Flag

```
MCTF26{v3Ry_b453D_t45k_w45Nt_1t}
```
