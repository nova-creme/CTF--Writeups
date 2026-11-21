# Mārtiņa-CTF 2026 — Writeups

Flag format `MCTF26{...}`. This event is also known as Martina CTF / MCTF 2026.

| # | Challenge | Category | Difficulty | Points | Flag | Folder |
|---|-----------|----------|------------|--------|------|--------|
| 1 | All Your Base Are Belong To Us | Crypto (base encoding) | Easy | — | `MCTF26{v3Ry_b453D_t45k_w45Nt_1t}` | [all-your-base](all-your-base/) |
| 2 | The Sealed Letter | Crypto (repeating-key XOR) | Easy | — | `MCTF26{r3p34t1ng_k3ys_br34k_s34ls}` | [sealed-letter](sealed-letter/) |
| 3 | The Multi-Prime Seal | Crypto (RSA reuse) | Medium | — | `MCTF26{R0ll1ng_my_0wn_crypt0_t0t13ns_fru5tr4_5un7}` | [multi-prime-seal](multi-prime-seal/) |
| 4 | PwnIntro | Pwn (ret2win) | Easy | — | `MCTF26{tH4t_was_4actU4lLy_v3rY_s1mpl3}` | [pwnintro](pwnintro/) |
| 5 | SSH: The Secure Network | Pwn / network | Medium | — | `MCTF26{Th1s_w45_supp0s3d_t0_b3_4_s3cure_n37w0rk}` | [ssh-secure-network](ssh-secure-network/) |
| 6 | The checksum (PHP Module Tester) | Web (file upload) | Easy | — | `MCTF26{cH3ck5uMM3d_4Nd_phpwned}` | [the-checksum](the-checksum/) |
| 7 | The Industries (I) | Web (cookie forgery) | Easy | 1000 | `MCTF26{w3Lc0m3_t0_Th3_Gu1ld}` | [the-industries-i](the-industries-i/) |
| 8 | The Industries (II) | Web (Flask auth) | Easy | 1000 | `MCTF26{p5ycH1c_d3S7R0y3d}` | [the-industries-ii](the-industries-ii/) |
| 9 | ApprenticesEntryExam | Web (blockchain) | Easy | — | `MCTF26{c9ngr4tz_0n_p4551ng_th3_f1r5t_3x4m}` | [apprentices-entry-exam](apprentices-entry-exam/) |
| 10 | [INTRO] What Is Crypto? | Crypto (encodings) | Easy | 1000 | `MCTF26{3nc0d1ng_1s_n0t_3ncrypt10n_w1z4rd}` | [intro-what-is-crypto](intro-what-is-crypto/) |
| 11 | [INTRO] The Apprentice's Cipher | Crypto (Caesar / Vigenère / XOR) | Easy | 1000 | `MCTF26{k3ys_m4tt3r_4ppr3nt1c3}` | [intro-apprentices-cipher](intro-apprentices-cipher/) |
| 12 | [INTRO] The Computer | Web (guided intro) | Easy | 1000 | `MCTF26{m4k3_1t_gr33n}` | [the-computer](the-computer/) |
| 13 | The Library | Web (crawling) | Medium | 1000 | `MCTF26{tH3_s34rCh_h45_p41D_0ff}` | [the-library](the-library/) |
| 14 | The Seer (I) | Forensics (USB HID) | Medium | 1000 | `MCTF26{m4RT1N5_kn0w5_Wh4t_y0u_wr0T3}` | [the-seer-i](the-seer-i/) |
| 15 | The Fortune Teller (I) | Reversing (binary patching) | Medium | 1000 | `MCTF26{tH4t_w4s_4actU4lLy_v3rY_s1mpl3}` | [the-fortune-teller-i](the-fortune-teller-i/) |
| 16 | The Fishy Board | Stego (chess AI oracle) | Medium | 937 | `MCTF26{S0M3_CH3K3R5}` | [the-fishy-board](the-fishy-board/) |

Each folder contains a template-format `SUMMARY.md` plus the original detailed `writeup.md`.

Notes:

- Rows 1–11 came from the existing `/home/novacreme/Downloads/galaxy/ctf_writeups_MCTF/`
  collection. Rows 12–15 were reconstructed from session artifacts after the flags
  were confirmed; they are shorter command-level writeups. Row 16 was solved and
  CTFd-verified during a later session.
- The Onion / "SSH: The Secure Network" and The Exam / "ApprenticesEntryExam" are
  alternate labels already represented by rows 5 and 9.
- Solves without a recoverable flag or finished writeup are not included here
  (A Mere Cantrip, The Demon, The Blob, The Kernel and several intro tasks).
- Some writeups reference working artifacts under `/home/novacreme/Downloads/galaxy/`; those binaries/scripts are not stored in this repository.
