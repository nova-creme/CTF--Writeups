---
title: "The Seer (I)"
ctf: "MCTF 2026"
date: 2026-11-20
category: forensics
difficulty: medium
points: 1000
flag_format: "MCTF26{...}"
---

# The Seer (I)

## Summary

A USB HID keyboard capture records everything Šņitrams typed, including a pasted flag. Decoding the interrupt-IN keycode reports with modifier, Caps Lock and backspace handling recovers the plaintext transcript.

## Solution

### Step 1: Extract the HID reports

The capture has 956 packets: 466 are 15-byte interrupt-IN keyboard reports and 12 are SET_REPORT control transfers. In each report byte 0 holds the modifiers (`0x02` = Shift), keycode `0x39` is Caps Lock and `0x2a` is Backspace; bytes 2–7 hold pressed keycodes.

### Step 2: Replay the keystrokes

Map HID usage IDs to characters, apply Shift/Caps Lock, and pop the last character on Backspace. The reconstructed transcript contains Google searches, a Gmail address and password, a pasted flag and YouTube browsing. The flag is split across idle gaps in the capture.

```python
import re

KEY = {**{0x04 + i: chr(ord('a') + i) for i in range(26)},
       **{0x1e + i: str(1 + i) for i in range(9)}, 0x27: '0',
       0x2c: ' ', 0x2d: '-', 0x2e: '=', 0x2f: '[', 0x30: ']',
       0x33: ';', 0x34: "'", 0x36: ',', 0x37: '.', 0x38: '/', 0x28: '\n'}
SHIFTED = {'1':'!','2':'@','3':'#','4':'$','5':'%','6':'^','7':'&','8':'*',
           '9':'(','0':')','-':'_','=':'+','[':'{',']':'}',';':':',
           "'":'"',',':'<','.':'>','/':'?'}

def decode(reports):
    """reports: [(modifier_byte, [keycodes]), ...] from the 15-byte HID reports"""
    out, caps = [], False
    for mod, keys in reports:
        for kc in keys:
            if kc == 0x39:                  # Caps Lock toggle
                caps = not caps
            elif kc == 0x2a:                # Backspace
                if out:
                    out.pop()
            elif kc in KEY:
                ch = KEY[kc]
                if mod & 0x02:
                    ch = SHIFTED.get(ch, ch.upper())
                elif caps:
                    ch = ch.upper()
                out.append(ch)
    return ''.join(out)

text = decode(usb_reports)
print(re.search(r'MCTF26\{[^}]+\}', text).group(0))
```

## Flag

```
MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}
```
