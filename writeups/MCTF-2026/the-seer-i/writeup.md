# MCTF 2026 — The Seer (I)

- **Category:** Forensics (USB HID)
- **Source:** reconstructed from session artifacts and confirmed flag submissions
- **Flag:** `MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}`

## Objective

Decode a USB HID keyboard capture to recover what Šņitrams typed.

## Solution path

1. Parsed the USB capture: 956 packets, including 466 15-byte interrupt-IN keyboard reports and 12 SET_REPORT control transfers.
2. Decoded HID keycodes with modifier `0x02` = Shift and keycode `0x39` = Caps Lock; applied backspace corrections.
3. Recovered a transcript of Google searches, a Gmail address/password, a pasted flag and YouTube browsing.
4. The pasted flag survives in `hid_transcript.txt`, split across idle gaps in the capture.

## Result

`MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}`

## Key lesson

Keyboard captures are plaintext if you map HID usage IDs correctly; modifier state and backspaces are the main sources of error.
