# The Troll's Ticket
* **Platform/Event:** InIt CTF (live session 2026-11-14)
* **Category:** Misc (multi-stage file carving / archive cracking, 200 pts)
* **Difficulty:** Medium
* **Flag:** `InIt{j0urney_4cr0ss_1ndia}`

## Objective
Work through a four-city trail of files-within-files — `IRCTC_Tatkal_Hack.pdf` (actually a zip), `outer_wordlist.txt`, `README.txt` — each stage hiding the next archive behind a password from the previous stage's wordlist, ending at an encrypted e-ticket PDF containing the flag.

## Reconnaissance & Methodology
1. `unzip -l IRCTC_Tatkal_Hack.pdf` revealed a password-protected zip, not a PDF. Cracked with `outer_wordlist.txt` (88k words) via Python `zipfile` → `railwaystationroyaljourney`; extracted `delhi.jpg`, `delhi_wordlist.txt`.
2. Tools used: `unzip`, Python `zipfile`, `file`, `tar`, `pikepdf`, per-stage wordlists.
3. Gate 1 (Delhi): `delhi.jpg` is a real JPEG with a ZipCrypto archive appended after its `FFD9` EOI marker — `zipfile` scans backward from EOF for the EOCD, so it opens transparently. Cracked with 17 words → `cholebhature`; got `mumbai.jpg`, `mumbai_wordlist.txt`.
4. Gate 2 (Mumbai): same zip-after-EOF trick; 15-word list → `vada_pav`; got `chennai.jpg`, `chennai_wordlist.txt`.
5. Gate 3 (Chennai): same trick; 15-word list → `mylapore`; got `kolkata.jpg`.
6. Gate 4 (Kolkata): appended data is a **POSIX tar** (not a zip), matching the note's "old-fashioned format" warning. `tar -xf` → `kolkata.txt`, `final_list.txt`, `golden_diamond_ticket_locked.pdf`.

## Solution & Exploitation
* Final gate: the PDF uses standard PDF encryption (not ZipCrypto); brute-forced with `pikepdf` against the 20-word `final_list.txt` → `peacock`.
* Password chain: `railwaystationroyaljourney → cholebhature → vada_pav → mylapore → peacock`.
* Decrypted e-ticket PDF prints the flag directly: `InIt{j0urney_4cr0ss_1ndia}`.
* Takeaway: three append tricks in one chain — zip-after-EOF, tar-after-EOF (breaks tools that only check zip signatures), and PDF password encryption; tightly scoped wordlists (15–20 words) make each brute force fast.
