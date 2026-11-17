# InIt CTF — The Troll's Ticket (Misc, 200)

## Flag

```
InIt{j0urney_4cr0ss_1ndia}
```

## Files given

- `IRCTC_Tatkal_Hack.pdf` (actually a zip)
- `outer_wordlist.txt`
- `README.txt`

This is a multi-stage trail — four cities, each one a JPEG hiding the next
archive appended after its JPEG end marker, unlocked with a password drawn from
the previous stage's wordlist.

## Gate 0 — the "PDF"

`IRCTC_Tatkal_Hack.pdf` opens as a password-protected zip (`unzip -l` shows
README/wordlist/jpg entries). Cracked `outer_wordlist.txt` (88k words) against
it with Python's `zipfile`:

```python
import zipfile
zf = zipfile.ZipFile("IRCTC_Tatkal_Hack.pdf")
for w in open("outer_wordlist.txt"):
    try:
        zf.read("README.txt", pwd=w.strip().encode())
        print(w)
        break
    except Exception:
        pass
```

→ password `railwaystationroyaljourney`, revealing `delhi.jpg` and
`delhi_wordlist.txt`.

## Gate 1 — Delhi

`delhi.jpg` is a real, viewable JPEG, but it has a zip appended after its `FFD9`
end-of-image marker. Python's `zipfile` handles this transparently since it
scans backward from EOF for the end-of-central-directory record. Opening
`delhi.jpg` as a zip lists `delhi.txt`, `mumbai.jpg`, `mumbai_wordlist.txt`,
encrypted with ZipCrypto. Cracked with `delhi_wordlist.txt` (17 words) →
`cholebhature`.

## Gate 2 — Mumbai

Same trick: `mumbai.jpg` has a zip appended, containing `mumbai.txt`,
`chennai.jpg`, `chennai_wordlist.txt`. Cracked with `mumbai_wordlist.txt`
(15 words) → `vada_pav`.

## Gate 3 — Chennai

`chennai.jpg` → appended zip with `chennai.txt`, `kolkata.jpg`. Cracked with
`chennai_wordlist.txt` (15 words) → `mylapore`.

## Gate 4 — Kolkata (format switch)

`kolkata.jpg` has data appended after its EOI too, but it's **not** a zip —
`file` identifies it as a POSIX tar archive. Extracting it (`tar -xf`) gives
`kolkata.txt`, `final_list.txt`, and `golden_diamond_ticket_locked.pdf`. This is
the "old-fashioned format" the note warns about.

## Final gate — the ticket

The PDF is encrypted (standard PDF password protection, not a zip this time).
Brute-forced with `pikepdf` against `final_list.txt` (20 words) → `peacock`.
The decrypted PDF is the e-ticket, with the flag printed directly in its text.

## Chain of passwords

```
railwaystationroyaljourney → cholebhature → vada_pav → mylapore → peacock
```

## Takeaway

Classic "file within a file" chain combining three append tricks:
zip-after-EOF (most common), tar-after-EOF (less common, breaks tools that only
check zip signatures), and PDF owner/user-password encryption at the very end.
Each wordlist was scoped tightly (15–20 words) so a plain dictionary brute
force was always fast; the only large one was the first gate.
