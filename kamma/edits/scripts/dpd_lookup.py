"""Print every DPD headword row (pos, grammar, root, compound, construction, meaning) for the lemmas or inflected forms given as arguments; with --sentence, mark headwords whose DPD example quotes that sentence; read-only audit helper, DB path from $DPD_DB or the default below."""

import argparse
import os
import re
import sqlite3

from sbs_sync import example_matches

DB = os.environ.get("DPD_DB", "/Users/deva/Documents/dpd-db/dpd.db")

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("words", nargs="+", help="lemmas or inflected forms")
ap.add_argument(
    "--sentence",
    help="key sentence (Pāli); headwords whose example_1/example_2 matches get an EXAMPLE prefix",
)
args = ap.parse_args()

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
for w in args.words:
    rows = con.execute(
        "select lemma_1, pos, grammar, root_key, root_sign, compound_type, compound_construction, construction, meaning_1, meaning_2, example_1, example_2 from dpd_headwords"
        " where lemma_1 = ? or lemma_1 like ?"
        " or id in (select j.value from lookup, json_each(lookup.headwords) j where lookup.lookup_key = ? and lookup.headwords != '')"
        " order by lemma_1",
        (w, w + " %", w),
    ).fetchall()
    if not rows:
        print(f"-- {w}: no headword")
    for r in rows:
        cons = re.sub(r"\s+", " ", (r[7] or "").replace("\n", " / "))
        quoted = args.sentence and any(
            example_matches(e or "", args.sentence) for e in (r[10], r[11])
        )
        print(
            f"{'EXAMPLE ' if quoted else ''}{r[0]} | {r[1]} | {r[2]} | {r[3]} {r[4]} | {r[5]} {r[6]} | {cons} | {(r[8] or r[9] or '')[:90]}"
        )
