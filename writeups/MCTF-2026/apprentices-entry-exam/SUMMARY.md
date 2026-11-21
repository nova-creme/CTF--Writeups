# ApprenticesEntryExam
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Web (blockchain)
* **Difficulty:** Easy
* **Flag:** `MCTF26{c9ngr4tz_0n_p4551ng_th3_f1r5t_3x4m}`

## Objective
A three-question smart-contract exam. Question I asks for a `private` `seal`, but private
storage is still readable through `eth_getStorageAt`; Questions II and III only require an
exact payment and the caller's address modulo 1000.

## Reconnaissance & Methodology
1. Step 1: Locate the exam and read the private seal
2. Step 2: Answer all three questions and request the flag

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{c9ngr4tz_0n_p4551ng_th3_f1r5t_3x4m}`
