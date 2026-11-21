---
title: "The Fortune Teller (I)"
ctf: "MCTF 2026"
date: 2026-11-20
category: reverse
difficulty: medium
points: 1000
flag_format: "MCTF26{...}"
---

# The Fortune Teller (I)

## Summary

The binary gates its final "fortune" on a `worthy` global in `.bss` that is never written, so the check always fails. Flipping one conditional jump and stubbing `sleep()` makes the existing decryption routine print the flag.

## Solution

### Step 1: Find the dead gate

`main` calls `gen1`–`gen4`. The global `worthy` at `0x40403c` lives in `.bss` and no instruction writes to it. In `gen3` the check at `0x40159a` is `jne 0x4015a2`; with `worthy == 0` the jump is taken into the "not worthy" branch and `exit(1)`.

### Step 2: Patch and run

Invert the branch (`jne` → `jmp`) at file offset `0x15a2`, then preload a stub `sleep()` so `gen4` prints immediately.

```bash
# 0x75 = jne, 0xeb = jmp at file offset 0x15a2
printf '\xeb' | dd of=fortuneteller_patched bs=1 seek=$((0x15a2)) conv=notrunc

cat > nosleep.c <<'EOF'
int sleep(unsigned int s) { return 0; }
EOF
gcc -shared -fPIC -o nosleep.so nosleep.c

LD_PRELOAD=./nosleep.so ./fortuneteller_patched
```

## Flag

```
MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}
```
