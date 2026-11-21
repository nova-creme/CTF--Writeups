---
title: "PwnIntro"
ctf: "MCTF 2026"
date: 2026-11-20
category: pwn
difficulty: easy
points: N/A
flag_format: "MCTF26{...}"
---

# PwnIntro

## Summary

The challenge binary (`/home/novacreme/Downloads/galaxy/pwnintro`) comes from `main.c`, which
declares `char buf[32]` but the service reads `0x100` bytes into it via `read(STDIN, buf, 0x100)`,
before calling `cast_spell()`. The exploit is a plain stack buffer overflow / ret2win style
overwrite.

## Solution

### Step 1: Trigger the overflow

Send more than 32 bytes of payload into the service input so the overflow hits the saved return
address and redirects execution to `cast_spell`.

**Challenge code (`main.c`):**

```c
#include <stdio.h>
#include <unistd.h>

void cast_spell() {
    puts("MCTF26{FAKE_FLAG_FOR_TESTING}");
}

void read_input() {
    char buf[32];
    puts("Input your payload: ");
    read(STDIN_FILENO, buf, 0x100);
}

int main(void) {
    read_input();
    return 0;
}
```

### Step 2: Land the flag

Once execution lands in the target function, the flag is printed by the service.

## Flag

```
MCTF26{tH4t_was_4actU4lLy_v3rY_s1mpl3}
```
