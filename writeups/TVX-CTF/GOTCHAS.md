# Gotchas worth remembering (TVX CTF session)

* **Never name a helper script after a stdlib module.** The CIL disassembler was
  first called `dis.py`; once its directory was on `sys.path`, Python's own
  `import dis` (pulled in by `inspect`, by `dataclasses`, by `py7zr`) loaded it and
  crashed. Renamed to `cildis.py`.
* **Verify a password checker before trusting its failures.** `py7zr.SevenZipFile.readall`
  does not exist in the installed version, so early "wrong password" results were
  bugs. Calibrate against an archive with a known password.
* **Homophonic ciphers need a letter-frequency penalty** or the hill-climber
  collapses into e/t/s soup.
* **A flag that decrypts too easily may be a decoy.** In the Ender chest challenge
  the public-key-keyed ciphertext was the troll and the hard one was real.
