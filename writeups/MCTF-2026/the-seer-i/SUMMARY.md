# The Seer (I)
* **Platform/Event:** Mārtiņa-CTF 2026
* **Category:** Forensics (USB HID)
* **Difficulty:** Medium
* **Flag:** `MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}`

## Objective
Decode a USB HID keyboard capture to recover what Šņitrams typed.

## Reconnaissance & Methodology
1. Parsed the USB capture: 956 packets, including 466 15-byte interrupt-IN keyboard reports and 12 SET_REPORT control transfers.
2. Decoded HID keycodes with modifier `0x02` = Shift and keycode `0x39` = Caps Lock; applied backspace corrections.
3. Recovered a transcript of Google searches, a Gmail address/password, a pasted flag and YouTube browsing.
4. The pasted flag survives in `hid_transcript.txt`, split across idle gaps in the capture.

## Solution & Exploitation
* USB HID interrupt-IN reports encode keystrokes as keycodes plus modifier bytes. Replaying them with Shift/Caps Lock and backspace handling reconstructs the typed text, including the flag.
* Final flag: `MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}`
