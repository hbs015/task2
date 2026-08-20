import csv
import sqlite3
from pathlib import Path

here = Path(__file__).resolve().parent
db = here.parent / "task1" / "data" / "people.db"
out = here / "known_identities.csv"

con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
q = """
select p.person_id, p.canonical_name, e.email as value, 'email' as kind
from people p
join person_emails e on e.person_id = p.person_id
union all
select p.person_id, p.canonical_name, ph.phone, 'phone'
from people p
join person_phones ph on ph.person_id = p.person_id
order by 1, 4, 3
"""
rows = [dict(r) for r in con.execute(q)]
con.close()

with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["person_id", "canonical_name", "kind", "value"])
    w.writeheader()
    w.writerows(rows)

print(len(rows), "->", out)
