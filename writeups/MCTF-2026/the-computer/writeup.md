---
title: "[INTRO] The Computer"
ctf: "MCTF 2026"
date: 2026-11-20
category: web
difficulty: easy
points: 1000
flag_format: "MCTF26{...}"
---

# [INTRO] The Computer

## Summary

A guided web onboarding task. The challenge description publishes the completion flag directly, so the solve is recognising that no service interaction is required and submitting the stated value.

## Solution

### Step 1: Read the description

The intro page walks through the web challenge environment and includes the completion flag in its text. There is no form, cookie or endpoint to exploit — the flag is given as part of the tutorial.

```python
flag = "MCTF26{m4k3_1t_gr33n}"
print(flag)
```

### Step 2: Submit it

Submit that value to CTFd to mark the challenge solved.

## Flag

```
MCTF26{m4k3_1t_gr33n}
```
