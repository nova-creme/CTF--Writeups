# The checksum (PHP Module Tester)
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Web (file upload)
* **Difficulty:** Easy
* **Flag:** `MCTF26{cH3ck5uMM3d_4Nd_phpwned}`

## Objective
Upload validation compares only the first 6 hex characters of the uploaded file's
SHA-256 against a hardcoded value. A malicious PHP file was brute-forced until its
SHA-256 prefix matched `test.php`'s checksum (`6b0c11`), then uploaded and executed.

## Reconnaissance & Methodology
1. Step 1: Identify the weak validation
2. Step 2: Mine a colliding payload, upload it, read the flag

## Solution & Exploitation
* Full commands, scripts and artifacts are preserved in [`writeup.md`](writeup.md).
* Final flag: `MCTF26{cH3ck5uMM3d_4Nd_phpwned}`
