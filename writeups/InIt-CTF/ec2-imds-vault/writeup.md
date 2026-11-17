# InIt CTF — EC2 IMDS Vault

- **Category:** Forensics (cloud IR / key derivation)
- **Artifact:** `~/Downloads/incident_ec2.zip`
  (`INCIDENT.txt`, `agent/vault.py`, `agent/vault.bin`, `artifacts/` logs)
- **Scenario:** Unauthorised cron script `/opt/agent/vault.py` on a web-tier
  EC2 instance. Vault key not on disk — derived at runtime from the instance's
  own identity.

## Flag

```
InIt{imds_k3y3d_s3cr3t_v4ult}
```

## Solution

**1. Code review** (`vault.py`):

```python
key = sha256(("s4lt_" + instance_id).encode())   # AES-256-CBC, IV prepended
plain = AES.new(key, MODE_CBC, iv).decrypt(ct)
plain = plain[:-plain[-1]]                       # PKCS#7
```

The identity is fetched from IMDS (169.254.169.254); the offline cache
`instance-id.cache` is missing.

**2. Identity from the logs** — `artifacts/cloud-init-output.log` prints it at
boot:

```
instance-id: i-0a1b2c3d4e5f67890
```

**3. Decrypt:**

```python
import hashlib
from Crypto.Cipher import AES
iid = 'i-0a1b2c3d4e5f67890'
key = hashlib.sha256(('s4lt_' + iid).encode()).digest()
blob = open('vault.bin','rb').read()
pt = AES.new(key, AES.MODE_CBC, blob[:16]).decrypt(blob[16:])
pt = pt[:-pt[-1]]
# {"config_version": 2, "collected_region": "ap-south-1",
#  "operator_note": "InIt{imds_k3y3d_s3cr3t_v4ult}"}
```

## Timeline (syslog/crontab corroboration)

```
02:14:07  SSH login from 203.0.113.44 (publickey, ubuntu)
02:15:51  sudo mkdir -p /opt/agent
02:16:03  vault loaded (version 2); cron */5 * * * * runs vault.py
```

Lesson: a key "derived from instance identity" is only as secret as the boot
logs that print that identity — cloud-init output is an IR goldmine.
