"""Print DPD headword rows (pos, grammar, root, compound, construction, meaning) for the lemmas given as arguments; read-only helper for the key audit."""

import re
import sqlite3
import sys

con = sqlite3.connect("file:/Users/deva/Documents/dpd-db/dpd.db?mode=ro", uri=True)
for w in sys.argv[1:]:
    rows = con.execute(
        "select lemma_1, pos, grammar, root_key, root_sign, compound_type, compound_construction, construction, meaning_1, meaning_2 from dpd_headwords where lemma_1 = ? or lemma_1 like ? order by lemma_1",
        (w, w + " %"),
    ).fetchall()
    if not rows:
        print(f"-- {w}: no headword")
    for r in rows[:6]:
        cons = re.sub(r"\s+", " ", (r[7] or "").replace("\n", " / "))
        print(
            f"{r[0]} | {r[1]} | {r[2]} | {r[3]} {r[4]} | {r[5]} {r[6]} | {cons} | {(r[8] or r[9] or '')[:90]}"
        )
