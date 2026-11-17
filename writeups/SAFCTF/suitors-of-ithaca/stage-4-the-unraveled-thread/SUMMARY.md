# The Unraveled Thread (Stage 4)
* **Platform/Event:** PWNZONE-26 / SAFCTF
* **Category:** OSINT / Git forensics (300 pts)
* **Difficulty:** Medium
* **Flag:** `safctf{unraveled_thread_d4}`

## Objective
Mine a public git repository linked from the suspect's Agora profile for deleted notes containing the fourth flag.

## Reconnaissance & Methodology
1. Tools used: `curl`, `git clone`, `git log --all`, `git log --all -p | grep`.
2. `/agora/u/outis-k/code` revealed `git clone http://54.72.82.22:8098/git/portfolio.git`.
3. `git log --all --format="%an <%ae> - %s"` mapped commit authors/messages (including the author email used in Stage 5).
4. `git log --all -p | grep -i -A3 -B3 "safctf\|name\|email\|real"` surfaced a deleted commit ("oops, remove private notes") whose removed TODO list contained the flag.

## Solution & Exploitation
* Flag: `safctf{unraveled_thread_d4}` from the deleted TODO item "drop token for the note".
* The same deleted notes yielded the Stage 5 leads: the Argonaut headline, the camera body serial `6021743`, and the stale contractor creds hint.
