# OSINT Chain Stage 4 — The Unraveled Thread (300 pts)

**Flag:** `safctf{unraveled_thread_d4}`

## Commands run

```bash
curl -s http://54.72.82.22:8098/agora/u/outis-k/code
# → revealed: git clone http://54.72.82.22:8098/git/portfolio.git

git clone http://54.72.82.22:8098/git/portfolio.git
cd portfolio
git log --all --format="%an <%ae> - %s"
git log --all -p | grep -i -A3 -B3 "safctf\|name\|email\|real"
```
→ A deleted commit ("oops, remove private notes") surfaced in the `-p` diff
output with a TODO list containing the flag plus other leads:

```
- [ ] Ithaca Systems portal: /admin/motd never got locked down. lol.
- [ ] stale contractor creds still work on ithaca-systems.example. lmao.
- [x] drop token for the note: safctf{unraveled_thread_d4}
- [ ] update my Argonaut headline before someone finds it
- [ ] sell the camera (body serial 6021743, check the box)
```
