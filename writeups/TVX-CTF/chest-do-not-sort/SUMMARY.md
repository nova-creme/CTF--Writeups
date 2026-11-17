# Chest (DO NOT SORT)
* **Platform/Event:** TVX CTF
* **Category:** Crypto (homophonic substitution)
* **Difficulty:** Hard
* **Flag:** `TVX{never_dig_straight_down}`

## Objective
Recover a warning message from `chest.txt` — 1,437 item names (nine per line) forming a homophonic substitution cipher where frequent letters have multiple symbols.

## Reconnaissance & Methodology
1. Tools used: Python `collections.Counter`, `numpy`, NLTK corpora (Brown + Gutenberg, downloaded through the proxy), simulated annealing with an English quadgram model (`lp.npy`).
2. 39 distinct item names map to 26 letters; item frequencies are nearly flat, so ordinary frequency analysis fails.
3. Built a log-probability quadgram table from ~13.7M letters of Brown + Gutenberg.
4. Annealed 6 seeds in parallel; first version collapsed into e/t/s soup because many-to-one mappings can cheat the quadgram score. Added a chi-square penalty forcing the output letter distribution toward English (`W=1.5`).
5. Seeds 2, 3, 4 converged on the same readable text; fixed 6 rare letters by context: `arrow`→k, `lapis_lazuli`→c, `cobblestone`→p, `coal`→x, `bookshelf`→z, `emerald`→j.

## Solution & Exploitation
* Final payload: apply the corrected 39→26 mapping to all 1,437 items; the plaintext warns "never dig straight down".
* Flag assembly: tag `TVX` + the lowercase, underscore-joined phrase → `TVX{never_dig_straight_down}`.
* Gotcha recorded in `GOTCHAS.md`: homophonic ciphers need the letter-frequency penalty or the hill-climber collapses.
