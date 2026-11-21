---
title: "SSH: The Secure Network"
ctf: "MCTF 2026"
date: 2026-11-20
category: pwn
difficulty: medium
points: N/A
flag_format: "MCTF26{...}"
author: "novacreme"
---

# SSH: The Secure Network

## Summary

A fresh Martina CTF SSH server was stood up for the user (`martins:p455w0rd!`, host
`10.240.5.239`). The challenge task was to take the fresh server, work it, and recover the flag
— the flag being `MCTF26{Th1s_w45_supp0s3d_t0_b3_4_s3cure_n37w0rk}` ("This was supposed to be a
secure network").

## Solution

### Step 1: Reach the service

Connect via SSH with the provided credentials to the running challenge instance.

```bash
# SSH connection
ssh -o StrictHostKeyChecking=no martins:p455w0rd!@<host> <challengeprovided-service>

# netcat submission pattern used for the challenge services
printf '6 7 8 6 3 2\n' | nc -w 60 <host> <port>
```

### Step 2: Complete the challenge task

Carry out the server-side update/fix exercise and read the flag it guards.

## Flag

```
MCTF26{Th1s_w45_supp0s3d_t0_b3_4_s3cure_n37w0rk}
```
