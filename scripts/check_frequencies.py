"""Check (and with --write update) every frequency and DPD count quoted in the BPC and IPC lessons.

Usage:
    uv run python scripts/check_frequencies.py           # read-only report
    uv run python scripts/check_frequencies.py --write   # update numbers, kita order, footnote years

Data: the local DPD database (``$DPD_DB``, default /Users/deva/Documents/dpd-db/dpd.db,
opened read-only) and the CST frequency JSON ``<dir of DB>/shared_data/frequency/cst_file_freq.json``.

Counting rule for DPD words: every DPD word count counts unique words that have a meaning,
i.e. distinct ``clean(lemma_1)`` over rows with ``meaning_1 != ''``, where
``clean(l) = re.sub(r" \\d.*$", "", l)`` strips homonym numbers. Each claim adds its own filter.
Roots (``dpd_roots``) are not words, so the rule does not apply to them.

Corpus section file sets (``re.fullmatch`` on the CST file name):
    NIK4 s0[1-4]\\d+m\\d*\\.mul\\.xml    VIN vin\\d+m\\d*\\.mul\\.xml
    DN s01..  MN s02..  SN s03..  AN s04..  KN s05\\d+m\\d*\\.mul\\.xml (``.nrf`` excluded)
Form count: sum of the exact-form counts over the set. Absolutive count for a suffix
(tvā, tvāna, tūna, yāna): sum over forms in the set that end with the suffix and are
DPD absolutives (lookup headword ids intersect ids with pos 'abs' or 'ger').

DB counts (all unique words with a meaning):
    MASC_A      pos masc, pattern a masc / a masc pl / a2 masc / a masc east
    MASC_IU     pos masc, patterns i, ī, u, ū masc (and pl)
    NT_A, NT_IU, MASC_I, NT_ALL, NT_U   the same idea for neuters / one ending
    PRP_ANA     pos prp, lemma ends with āna but not māna
    PTP         pos ptp
    IMPERF      pos imperf, source_1 not '' and not 'kaccāyana'
    ROOTS_G1 / ROOTS_ALL   count of dpd_roots with root_group 1 / all
KITA rows: meaning_1 != '', suffix != '', root_key != '', construction on one line
(no taddhita step), pos in pp prp adj masc nt fem. kpos(s, p) is the unique words with
suffix s and pos p; ktotal(s) is the sum of kpos over the six POS (so a word with two POS
counts twice, as in the course's method). All 45 ``## <suffix>`` sections of IPC class 28
are ranked by ktotal (ties keep their current order): ranks 1-18 live in 1_kita_1.md, the
rest in 2_kita_less.md. The POS table of each section, the ranking table and the two
suffix lists of the first page are rebuilt from the counts; section text is otherwise moved
verbatim and a content guard aborts the write if any other line would change.

Precision: exact; round10 (v+5)//10*10; round100 (v+50)//100*100; floor10; floor1000;
pct(a, b) = (100*a + b//2)//b. A number after "about", "around" or "more than" is rounded.

Footnotes: every data footnote ends with ``This data is relevant for the year YYYY.``;
``--write`` sets YYYY to the current calendar year and renumbers footnotes.
"""

import argparse
import datetime
import json
import os
import re
import sqlite3
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from tools.printer import printer as pr

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
DEFAULT_DB = "/Users/deva/Documents/dpd-db/dpd.db"

POS6 = ("pp", "prp", "adj", "masc", "nt", "fem")
EXPECTED_SECTIONS = 45
EXPECTED_TOTAL_ROWS = 45
TOP_N = 18
BIG_CHANGE = 0.25

SETS = {
    "NIK4": r"s0[1-4]\d+m\d*\.mul\.xml",
    "VIN": r"vin\d+m\d*\.mul\.xml",
    "DN": r"s01\d+m\d*\.mul\.xml",
    "MN": r"s02\d+m\d*\.mul\.xml",
    "SN": r"s03\d+m\d*\.mul\.xml",
    "AN": r"s04\d+m\d*\.mul\.xml",
    "KN": r"s05\d+m\d*\.mul\.xml",
}

DB_FILTERS = {
    "MASC_A": "pos='masc' AND pattern IN ('a masc','a masc pl','a2 masc','a masc east')",
    "MASC_IU": "pos='masc' AND pattern IN ('i masc','i masc pl','ī masc','ī masc pl','u masc','u masc pl','ū masc')",
    "NT_A": "pos='nt' AND pattern IN ('a nt','a nt pl','a nt east','a nt irreg')",
    "NT_IU": "pos='nt' AND pattern IN ('i nt','u nt','u nt pl')",
    "MASC_I": "pos='masc' AND pattern IN ('i masc','i masc pl')",
    "NT_ALL": "pos='nt'",
    "NT_U": "pos='nt' AND pattern IN ('u nt','u nt pl')",
    "PRP_ANA": "pos='prp'",
    "PTP": "pos='ptp'",
    "IMPERF": "pos='imperf' AND source_1 NOT IN ('','kaccāyana')",
}

KITA_WHERE = (
    "meaning_1!='' AND suffix!='' AND root_key!='' AND instr(construction, char(10))=0 "
    "AND pos IN ('pp','prp','adj','masc','nt','fem')"
)

KITA1 = "ipc/class_28/1_kita_1.md"
KITA2 = "ipc/class_28/2_kita_less.md"

YEAR_RE = re.compile(r"This data is relevant for the year \d{4}\.")
TOTAL_RE = re.compile(r"^\| (\*\*)?total(\*\*)? \| (\*\*)?(?P<n>\d+)(\*\*)? \|$")
POS_ROW_RE = re.compile(r"^\| (\*\*)?(?P<p>pp|prp|adj|masc|nt|fem)(\*\*)? \| \d+ \|$")
SEP_RE = re.compile(r"^\| --- \| --- \|$")
RANK_ROW_RE = re.compile(r"^\| \d+ \| \*\*\+ .+\*\* \| \d+ \|$")
SUFFIX_INTRO = "Here are most of *kita* suffixes in DPD"


# --------------------------------------------------------------------------- precision


def round10(v: int) -> int:
    return (v + 5) // 10 * 10


def round100(v: int) -> int:
    return (v + 50) // 100 * 100


def floor10(v: int) -> int:
    return v // 10 * 10


def floor1000(v: int) -> int:
    return v // 1000 * 1000


def pct(a: int, b: int) -> int:
    return (100 * a + b // 2) // b


def apply_precision(rule: str, v: int) -> int:
    if rule == "exact":
        return v
    return {
        "round10": round10,
        "round100": round100,
        "floor10": floor10,
        "floor1000": floor1000,
    }[rule](v)


def clean(lemma: str) -> str:
    """Strip the homonym number from a lemma."""
    return re.sub(r" \d.*$", "", lemma)


# --------------------------------------------------------------------------- claims


@dataclass(frozen=True)
class Claim:
    file: str
    label: str
    regex: str
    value: str
    precision: str = "exact"
    group: str = "n"
    after: str | None = None


def _forms_claims() -> list[Claim]:
    claims: list[Claim] = []
    f5 = "bpc/class_5/2_pers_pron.md"
    forms5 = (
        "ahaṃ maṃ mayā me mayhaṃ mama mamaṃ mayi mayaṃ amhākaṃ no "
        "tvaṃ taṃ tuvaṃ tayā te tava tumhe tumhākaṃ vo"
    ).split()
    for form in forms5:
        rx = (
            rf"^\| (\*\*)?{re.escape(form)}(\*\*)? \|.*\| (\*\*)?(?P<n>\d+)(\*\*)?"
            r"( / \(Including [^)]*\))? \|$"
        )
        claims.append(Claim(f5, form, rx, f"form:NIK4:{form}"))
    for form in ("bhagavā", "bhagavantaṃ", "bhagavatā", "bhagavato"):
        rx = rf"^{re.escape(form)} (?P<n>\d+)(\[\^\d+\])?$"
        claims.append(Claim("bpc/class_6/4_subst.md", form, rx, f"form:NIK4:{form}"))
    f8 = "bpc/class_8/2_abs_ger.md"
    names = {
        "VIN": "Vinaya",
        "DN": "Dīgha Nikāya",
        "MN": "Majjhima Nikāya",
        "SN": "Saṃyutta Nikāya",
        "AN": "Aṅguttara Nikāya",
        "KN": "Khuddaka Nikāya",
    }
    for sec, name in names.items():
        claims.append(
            Claim(
                f8,
                f"{sec} tvā",
                rf"^(?P<n>\d+) times in {name}",
                f"abs:{sec}:tvā",
                "round100",
            )
        )
    for sec in names:
        rx = rf"^\| {sec}(\[\^\d+\])? \| (\\>)?(?P<n1>\d+) \| (?P<n2>\d+) \| (?P<n3>\d+) \|$"
        first = "floor1000" if sec == "KN" else "exact"
        for grp, suffix, prec in (
            ("n1", "tvāna", first),
            ("n2", "tūna", "exact"),
            ("n3", "yāna", "exact"),
        ):
            claims.append(
                Claim(f8, f"{sec} {suffix}", rx, f"abs:{sec}:{suffix}", prec, grp)
            )
    return claims


def _build_claims() -> list[Claim]:
    c2 = "bpc/class_2/3_decl_nouns.md"
    masc_total = r"^\| masculine nouns total \| \*\*\d+\*\* \|$"
    nt_total = r"^\| neuter nouns total \| \*\*\d+\*\* \|$"
    share = r"^\| share of \*\*-a\*\* \| \*\*(?P<n>\d+)%\*\* \|$"
    claims = [
        Claim(
            c2,
            "masc -a",
            r"^\| masculine nouns ending in \*\*-a\*\* \| \*\*(?P<n>\d+)\*\* \|$",
            "MASC_A",
        ),
        Claim(
            c2,
            "masc -i -ī -u -ū",
            r"^\| masculine nouns ending in \*\*-i -ī -u -ū\*\* \| (?P<n>\d+) \|$",
            "MASC_IU",
        ),
        Claim(
            c2,
            "masc total",
            r"^\| masculine nouns total \| \*\*(?P<n>\d+)\*\* \|$",
            "MASC_TOTAL",
        ),
        Claim(c2, "masc share -a", share, "MASC_SHARE", after=masc_total),
        Claim(
            c2,
            "nt -a",
            r"^\| neuter nouns ending in \*\*-a\*\* \| \*\*(?P<n>\d+)\*\* \|$",
            "NT_A",
        ),
        Claim(
            c2,
            "nt -i -u",
            r"^\| neuter nouns ending in \*\*-i -u\*\* \| (?P<n>\d+) \|$",
            "NT_IU",
        ),
        Claim(
            c2,
            "nt total",
            r"^\| neuter nouns total \| \*\*(?P<n>\d+)\*\* \|$",
            "NT_TOTAL",
        ),
        Claim(c2, "nt share -a", share, "NT_SHARE", after=nt_total),
        Claim(
            "bpc/class_3/6_root_1.md",
            "roots group 1 %",
            r"(?P<n>\d+)% of roots in Pāḷi \(around \d+\)",
            "ROOTS_PCT",
        ),
        Claim(
            "bpc/class_3/6_root_1.md",
            "roots group 1 around",
            r"\d+% of roots in Pāḷi \(around (?P<n>\d+)\)",
            "ROOTS_G1",
            "round100",
        ),
        Claim(
            "bpc/class_4/9_masc_i.md",
            "masc -i about",
            r"There are about (?P<n>\d+) of these nouns in the DPD",
            "MASC_I",
            "round100",
        ),
    ]
    claims += _forms_claims()
    claims += [
        Claim(
            "bpc/class_9/2_nt.md",
            "nt more than",
            r"more than (?P<n>\d+) words in the current DPD database",
            "NT_ALL",
            "floor1000",
        ),
        Claim(
            "bpc/class_9/2_nt.md",
            "nt -u about",
            r"less common, about (?P<n>\d+) in the current DPD database",
            "NT_U",
            "round100",
        ),
        Claim(
            "bpc/class_10/2_prp.md",
            "prp -āna",
            r"DPD has only about (?P<n>\d+)\[\^",
            "PRP_ANA",
            "round10",
        ),
        Claim(
            "bpc/class_14/4_ptp.md",
            "ptp",
            r"DPD has around (?P<n>\d+)\[\^\d+\] unique entries",
            "PTP",
            "round100",
        ),
        Claim(
            "ipc/class_21/8_imperf.md",
            "imperfect",
            r"In DPD there are \*\*(?P<n>\d+)\*\*\[\^\d+\] Tipiṭaka examples",
            "IMPERF",
        ),
        Claim(
            KITA1,
            "kita suffixes",
            r"more than (?P<n>\d+) suffixes of primary derivatives",
            "SUFFIX_COUNT",
            "floor10",
        ),
        Claim(
            KITA1,
            "kita words",
            r"used to form more than (?P<n>\d+) nouns",
            "KITA_WORDS",
            "floor1000",
        ),
        Claim(
            KITA1,
            "kita top-18 share",
            r"account for \*\*(?P<n>\d+)%\*\*",
            "KITA_TOP18_SHARE",
        ),
    ]
    return claims


CLAIMS: list[Claim] = _build_claims()


def locate_claim(lines: list[str], claim: Claim) -> int | None:
    """Index of the single line the claim matches, or None when 0 or 2+ lines match."""
    rx = re.compile(claim.regex)
    if claim.after is None:
        hits = [i for i, line in enumerate(lines) if rx.search(line)]
        return hits[0] if len(hits) == 1 else None
    anchor = re.compile(claim.after)
    anchors = [i for i, line in enumerate(lines) if anchor.search(line)]
    if len(anchors) != 1:
        return None
    for i in range(anchors[0] + 1, len(lines)):
        if rx.search(lines[i]):
            return i
    return None


def read_group(line: str, claim: Claim) -> int | None:
    m = re.search(claim.regex, line)
    return int(m.group(claim.group)) if m else None


def replace_group(line: str, claim: Claim, new: int) -> str | None:
    """Replace only the claim's named group in the line."""
    m = re.search(claim.regex, line)
    if not m:
        return None
    s, e = m.span(claim.group)
    return line[:s] + str(new) + line[e:]


# --------------------------------------------------------------------------- data


@dataclass
class Data:
    values: dict[str, int]
    kpos: dict[tuple[str, str], int] = field(default_factory=dict)


def _in_set(name: str, filename: str) -> bool:
    return re.fullmatch(SETS[name], filename) is not None


def _db_path() -> str:
    return os.environ.get("DPD_DB", DEFAULT_DB)


def _unique(conn: sqlite3.Connection, where: str) -> set[str]:
    rows = conn.execute(
        f"SELECT lemma_1 FROM dpd_headwords WHERE meaning_1 != '' AND {where}"
    ).fetchall()
    return {clean(r[0]) for r in rows}


def load_data(claims: list[Claim]) -> Data:
    """Compute every named value the claims need from the DB and the CST frequency JSON."""
    db = _db_path()
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    v: dict[str, int] = {}
    for name, where in DB_FILTERS.items():
        words = _unique(conn, where)
        if name == "PRP_ANA":
            words = {w for w in words if w.endswith("āna") and not w.endswith("māna")}
        v[name] = len(words)
    v["ROOTS_G1"] = conn.execute(
        "SELECT count(*) FROM dpd_roots WHERE root_group=1"
    ).fetchone()[0]
    v["ROOTS_ALL"] = conn.execute("SELECT count(*) FROM dpd_roots").fetchone()[0]

    kpos_sets: dict[tuple[str, str], set[str]] = {}
    kita_words: set[str] = set()
    for lemma, suffix, pos in conn.execute(
        f"SELECT lemma_1, suffix, pos FROM dpd_headwords WHERE {KITA_WHERE}"
    ):
        w = clean(lemma)
        kpos_sets.setdefault((suffix, pos), set()).add(w)
        kita_words.add(w)
    kpos = {k: len(s) for k, s in kpos_sets.items()}
    v["KITA_WORDS"] = len(kita_words)
    v["SUFFIX_COUNT"] = len({s for s, _ in kpos})

    wanted = {c.value for c in claims if c.value.startswith(("form:", "abs:"))}
    if wanted:
        _corpus_values(conn, db, wanted, v)
    conn.close()
    derive(v)
    return Data(v, kpos)


def release_version() -> str:
    conn = sqlite3.connect(f"file:{_db_path()}?mode=ro", uri=True)
    row = conn.execute(
        "SELECT value FROM db_info WHERE key='dpd_release_version'"
    ).fetchone()
    conn.close()
    return row[0] if row else "not recorded"


def _corpus_values(
    conn: sqlite3.Connection, db: str, wanted: set[str], v: dict[str, int]
) -> None:
    path = Path(db).parent / "shared_data" / "frequency" / "cst_file_freq.json"
    freq = cast(dict[str, dict[str, int]], json.loads(path.read_text(encoding="utf-8")))
    merged: dict[str, Counter[str]] = {}
    for name in SETS:
        counter: Counter[str] = Counter()
        for fname, forms in freq.items():
            if _in_set(name, fname):
                for form, n in forms.items():
                    counter[unicodedata.normalize("NFC", form)] += n
        merged[name] = counter
    abs_ids = {
        r[0]
        for r in conn.execute("SELECT id FROM dpd_headwords WHERE pos IN ('abs','ger')")
    }
    for key in wanted:
        kind, sec, item = key.split(":")
        item = unicodedata.normalize("NFC", item)
        if kind == "form":
            v[key] = merged[sec].get(item, 0)
            continue
        total = 0
        for form, n in merged[sec].items():
            if not form.endswith(item):
                continue
            row = conn.execute(
                "SELECT headwords FROM lookup WHERE lookup_key=?", (form,)
            ).fetchone()
            if row and row[0] and abs_ids.intersection(json.loads(row[0])):
                total += n
        v[key] = total


def derive(v: dict[str, int]) -> None:
    v["MASC_TOTAL"] = v["MASC_A"] + v["MASC_IU"]
    v["NT_TOTAL"] = v["NT_A"] + v["NT_IU"]
    v["MASC_SHARE"] = pct(v["MASC_A"], v["MASC_TOTAL"])
    v["NT_SHARE"] = pct(v["NT_A"], v["NT_TOTAL"])
    v["ROOTS_PCT"] = pct(v["ROOTS_G1"], v["ROOTS_ALL"])


# --------------------------------------------------------------------------- sections


def split_sections(text: str) -> tuple[list[str], list[list[str]]]:
    """Split into the preamble lines and the ``## `` sections (heading line first)."""
    pre: list[str] = []
    secs: list[list[str]] = []
    for line in text.split("\n"):
        if line.startswith("## "):
            secs.append([line])
        elif secs:
            secs[-1].append(line)
        else:
            pre.append(line)
    return pre, secs


def join_sections(pre: list[str], secs: list[list[str]]) -> str:
    lines = list(pre)
    for s in secs:
        lines.extend(s)
    return "\n".join(lines)


def unesc(s: str) -> str:
    return s.replace("\\*", "*")


def esc(s: str) -> str:
    return s.replace("*", "\\*")


def heading_suffix(sec: list[str]) -> str:
    return unesc(sec[0][3:].strip())


def suffix_totals(kpos: dict[tuple[str, str], int]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for (suffix, _pos), n in kpos.items():
        totals[suffix] = totals.get(suffix, 0) + n
    return totals


def ktotal(kpos: dict[tuple[str, str], int], suffix: str) -> int:
    return sum(kpos.get((suffix, p), 0) for p in POS6)


def _trim(sec: list[str]) -> tuple[list[str], int]:
    body = list(sec)
    gap = 0
    while body and body[-1] == "":
        body.pop()
        gap += 1
    return body, gap


def _find_table(sec: list[str]) -> tuple[int, int] | None:
    """Span (start, end) of the section's two-column POS table, if it has one."""
    for i in range(1, len(sec)):
        if sec[i - 1] == "| | |" and SEP_RE.match(sec[i]):
            j = i + 1
            while j < len(sec) and (POS_ROW_RE.match(sec[j]) or TOTAL_RE.match(sec[j])):
                j += 1
            if j > i + 1:
                if j < len(sec) and sec[j].startswith("|"):
                    raise ValueError(f"unexpected row in POS table: {sec[j][:40]}")
                return i - 1, j
    return None


def pos_table(suffix: str, kpos: dict[tuple[str, str], int]) -> list[str]:
    """The POS table of a section: rows with count > 0 sorted descending, then the total."""
    counts = [(p, kpos.get((suffix, p), 0)) for p in POS6]
    ranked = sorted((c for c in counts if c[1] > 0), key=lambda c: -c[1])
    rows = [f"| **{p}** | {n} |" for p, n in ranked]
    return [
        "| | |",
        "| --- | --- |",
        *rows,
        f"| **total** | **{ktotal(kpos, suffix)}** |",
    ]


def update_pos_table(
    sec: list[str], suffix: str, kpos: dict[tuple[str, str], int]
) -> list[str]:
    """Rebuild (or add) the section's POS table in the one standard style."""
    try:
        found = _find_table(sec)
    except ValueError as exc:
        raise ValueError(f"section {suffix}: {exc}") from exc
    table = pos_table(suffix, kpos)
    if found is not None:
        return sec[: found[0]] + table + sec[found[1] :]
    # no table yet: after the heading, and after a one-line description if there is one
    i = 2
    if len(sec) > 2 and not sec[2].startswith(("|", "**+")) and sec[2].strip():
        if len(sec) > 3 and sec[3].strip():
            raise ValueError(
                f"section {suffix}: description is not one line; add the table by hand"
            )
        i = 4
    head = sec[:i]
    while len(head) < i:
        head.append("")
    return head + table + [""] + sec[i:]


def _sort_tokens(
    line: str, key_of: dict[str, int] | None, kt: dict[str, int], bold: bool
) -> str:
    body = line[2:-2] if bold else line
    tokens = body.split(" ")
    if key_of is not None:
        missing = [t for t in tokens if unesc(t) not in key_of]
        if missing:
            raise ValueError(f"suffix list token without section: {missing}")
        tokens.sort(key=lambda t: key_of[unesc(t)])
    else:
        tokens.sort(key=lambda t: -kt.get(unesc(t), 0))
    out = " ".join(tokens)
    return f"**{out}**" if bold else out


@dataclass
class KitaPlan:
    ranking: list[str]
    new1: str
    new2: str
    totals: dict[str, int]
    old_file: dict[str, int]  # suffix -> 1 or 2
    old_order: list[str]
    errors: list[str] = field(default_factory=list)
    total_rows: int = 0
    sections: int = 0


def plan_kita(t1: str, t2: str, kpos: dict[tuple[str, str], int]) -> KitaPlan:
    """Rank all sections by ktotal and rebuild the two pages (returned as texts)."""
    pre1, secs1 = split_sections(t1)
    pre2, secs2 = split_sections(t2)
    all_secs = [(1, s) for s in secs1] + [(2, s) for s in secs2]
    plan = KitaPlan([], t1, t2, {}, {}, [])
    plan.sections = len(all_secs)
    names = [heading_suffix(s) for _, s in all_secs]
    if len(set(names)) != len(names):
        plan.errors.append("duplicate section headings")
        return plan
    if plan.sections != EXPECTED_SECTIONS:
        plan.errors.append(
            f"expected {EXPECTED_SECTIONS} sections, found {plan.sections}"
        )
    plan.old_order = names
    plan.old_file = {heading_suffix(s): f for f, s in all_secs}
    plan.totals = {n: ktotal(kpos, n) for n in names}
    plan.ranking = sorted(names, key=lambda n: -plan.totals[n])
    rank_of = {n: i for i, n in enumerate(plan.ranking)}
    kt = suffix_totals(kpos)

    try:
        updated = {
            heading_suffix(s): update_pos_table(s, heading_suffix(s), kpos)
            for _, s in all_secs
        }
        pre1 = _rebuild_preamble(pre1, plan, rank_of, kt)
    except ValueError as exc:
        plan.errors.append(str(exc))
        return plan
    plan.total_rows = sum(1 for s in updated.values() for ln in s if TOTAL_RE.match(ln))
    if plan.total_rows != EXPECTED_TOTAL_ROWS:
        plan.errors.append(
            f"expected {EXPECTED_TOTAL_ROWS} total rows, found {plan.total_rows}"
        )

    def assemble(pre: list[str], suffixes: list[str]) -> str:
        lines = list(pre)
        for k, n in enumerate(suffixes):
            body, gap = _trim(updated[n])
            lines.extend(body)
            if k < len(suffixes) - 1:
                lines.extend([""] * max(gap, 1))
        return "\n".join(lines) + "\n"

    plan.new1 = assemble(pre1, plan.ranking[:TOP_N])
    plan.new2 = assemble(pre2, plan.ranking[TOP_N:])
    return plan


def _rebuild_preamble(
    pre: list[str], plan: KitaPlan, rank_of: dict[str, int], kt: dict[str, int]
) -> list[str]:
    out = list(pre)
    rows = [i for i, line in enumerate(out) if RANK_ROW_RE.match(line)]
    if len(rows) != TOP_N or rows[-1] - rows[0] != TOP_N - 1:
        raise ValueError(
            f"ranking table: expected {TOP_N} contiguous rows, found {len(rows)}"
        )
    new_rows = [
        f"| {i + 1} | **+ {esc(n)}** | {plan.totals[n]} |"
        for i, n in enumerate(plan.ranking[:TOP_N])
    ]
    out[rows[0] : rows[-1] + 1] = new_rows
    intro = next((i for i, line in enumerate(out) if SUFFIX_INTRO in line), None)
    if intro is None:
        raise ValueError("suffix list intro line not found")
    lists = [i for i in range(intro + 1, len(out)) if out[i].strip()][:2]
    if len(lists) != 2 or not (
        out[lists[0]].startswith("**") and out[lists[0]].endswith("**")
    ):
        raise ValueError("suffix lists not found after intro")
    out[lists[0]] = _sort_tokens(out[lists[0]], rank_of, kt, True)
    out[lists[1]] = _sort_tokens(out[lists[1]], None, kt, False)
    return out


def _section_core(sec: list[str]) -> list[str]:
    """The section's non-blank lines without its POS table."""
    body, _ = _trim(sec)
    found = _find_table(body)
    if found is not None:
        body = body[: found[0]] + body[found[1] :]
    return [ln for ln in body if ln.strip()]


def guard_kita(old1: str, old2: str, new1: str, new2: str) -> list[str]:
    """Problems found when comparing the sections before and after the rebuild."""
    old = {
        heading_suffix(s): _section_core(s)
        for t in (old1, old2)
        for s in split_sections(t)[1]
    }
    new_secs = [s for t in (new1, new2) for s in split_sections(t)[1]]
    new = {heading_suffix(s): _section_core(s) for s in new_secs}
    problems: list[str] = []
    if len(new_secs) != len(new) or set(old) != set(new):
        problems.append("section headings differ after the rebuild")
    for name in sorted(set(old) & set(new)):
        if old[name] != new[name]:
            problems.append(f"section {name}: text outside its POS table differs")
    return problems


# --------------------------------------------------------------------------- years


def rewrite_years(text: str, year: int) -> str:
    return YEAR_RE.sub(f"This data is relevant for the year {year}.", text)


def current_year() -> int:
    return datetime.date.today().year


# --------------------------------------------------------------------------- process


@dataclass
class Row:
    file: str
    line: int
    label: str
    old: str
    new: str
    status: str
    big: bool = False


@dataclass
class Result:
    rows: list[Row] = field(default_factory=list)
    reorders: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    new_texts: dict[str, str] = field(default_factory=dict)


def claim_files(claims: list[Claim]) -> list[str]:
    files: list[str] = []
    for f in [c.file for c in claims] + [KITA1, KITA2]:
        if f not in files:
            files.append(f)
    return files


def process(
    texts: dict[str, str], data: Data, claims: list[Claim], year: int
) -> Result:
    res = Result()
    values = dict(data.values)

    plan = plan_kita(texts[KITA1], texts[KITA2], data.kpos)
    res.errors.extend(plan.errors)
    if not plan.errors:
        values["KITA_TOP18_SHARE"] = pct(
            sum(plan.totals[n] for n in plan.ranking[:TOP_N]),
            sum(suffix_totals(data.kpos).values()),
        )
    lines = {f: texts[f].split("\n") for f in texts}

    for c in claims:
        idx = locate_claim(lines[c.file], c)
        if idx is None or c.value not in values:
            res.rows.append(Row(c.file, 0, c.label, "-", "-", "NOT FOUND"))
            continue
        old = read_group(lines[c.file][idx], c)
        assert old is not None
        new = apply_precision(c.precision, values[c.value])
        replaced = replace_group(lines[c.file][idx], c, new)
        assert replaced is not None
        lines[c.file][idx] = replaced
        status = "OK" if old == new else "CHANGED"
        big = old > 0 and abs(new - old) / old > BIG_CHANGE
        res.rows.append(Row(c.file, idx + 1, c.label, str(old), str(new), status, big))
    out = {f: "\n".join(ls) for f, ls in lines.items()}

    if not plan.errors:
        plan2 = plan_kita(out[KITA1], out[KITA2], data.kpos)
        res.errors.extend(plan2.errors)
        problems = guard_kita(out[KITA1], out[KITA2], plan2.new1, plan2.new2)
        res.errors.extend(problems)
        if not plan2.errors and not problems:
            _kita_rows(res, texts, out, plan2, data)
            out[KITA1], out[KITA2] = plan2.new1, plan2.new2

    for f in claim_files(claims):
        found = YEAR_RE.findall(out[f])
        if not found:
            res.errors.append(
                f"{f}: no 'This data is relevant for the year YYYY.' sentence"
            )
            continue
        old_years = sorted({m[-5:-1] for m in found})
        status = "OK" if old_years == [str(year)] else "CHANGED"
        line_no = (
            next(i for i, ln in enumerate(texts[f].split("\n")) if YEAR_RE.search(ln))
            + 1
        )
        res.rows.append(Row(f, line_no, "year", "/".join(old_years), str(year), status))
        out[f] = rewrite_years(out[f], year)
    res.new_texts = out
    return res


def _kita_rows(
    res: Result,
    texts: dict[str, str],
    claimed: dict[str, str],
    plan: KitaPlan,
    data: Data,
) -> None:
    for key in (KITA1, KITA2):
        _, secs = split_sections(texts[key])
        offset = len(split_sections(texts[key])[0])
        for s in secs:
            name = heading_suffix(s)
            tidx = next((i for i, ln in enumerate(s) if TOTAL_RE.match(ln)), None)
            old_n: int | None = None
            if tidx is not None:
                old_n = int(cast(re.Match[str], TOTAL_RE.match(s[tidx])).group("n"))
            changed = update_pos_table(s, name, data.kpos) != s
            big = (
                old_n is not None
                and old_n > 0
                and abs(plan.totals[name] - old_n) / old_n > BIG_CHANGE
            )
            res.rows.append(
                Row(
                    key,
                    offset + (tidx or 0) + 1,
                    f"kita total {name}",
                    "-" if old_n is None else str(old_n),
                    str(plan.totals[name]),
                    "CHANGED" if changed else "OK",
                    big,
                )
            )
            offset += len(s)
    old_pre = split_sections(claimed[KITA1])[0]
    new_pre = split_sections(plan.new1)[0]
    old_rank = [ln for ln in old_pre if RANK_ROW_RE.match(ln)]
    new_rank = [ln for ln in new_pre if RANK_ROW_RE.match(ln)]
    first = next((i for i, ln in enumerate(old_pre) if RANK_ROW_RE.match(ln)), 0) + 1
    status = "OK" if old_rank == new_rank else "CHANGED"
    res.rows.append(Row(KITA1, first, "kita ranking table", "-", "-", status))
    intro = next(i for i, ln in enumerate(old_pre) if SUFFIX_INTRO in ln)
    lists = [i for i in range(intro + 1, len(old_pre)) if old_pre[i].strip()][:2]
    for label, i in zip(("kita suffix list (bold)", "kita suffix list (plain)"), lists):
        res.rows.append(
            Row(
                KITA1,
                i + 1,
                label,
                "-",
                "-",
                "OK" if old_pre[i] == new_pre[i] else "CHANGED",
            )
        )
    moved = [
        n
        for n in plan.ranking
        if plan.old_file[n] != (1 if plan.ranking.index(n) < TOP_N else 2)
    ]
    for n in moved:
        dest = 1 if plan.ranking.index(n) < TOP_N else 2
        res.reorders.append(
            f"REORDER {n}: file {plan.old_file[n]} -> file {dest} (rank {plan.ranking.index(n) + 1}, total {plan.totals[n]})"
        )
    new_order_changed = plan.old_order != plan.ranking
    if new_order_changed:
        res.reorders.append("REORDER order of the sections changes (sorted by total)")


# --------------------------------------------------------------------------- io


def rel_path(rel: str) -> Path:
    return DOCS / rel


def load_texts(claims: list[Claim]) -> dict[str, str]:
    return {f: rel_path(f).read_text(encoding="utf-8") for f in claim_files(claims)}


def report(res: Result) -> int:
    counts: Counter[str] = Counter(r.status for r in res.rows)
    for r in res.rows:
        loc = f"{r.file}:{r.line}"
        msg = f"{loc:<42} {r.label:<26} {r.old:>8} -> {r.new:<8} {r.status}"
        if r.status == "NOT FOUND":
            pr.red(msg)
        elif r.big:
            pr.amber(msg + "  (>25%)")
        elif r.status == "CHANGED":
            pr.cyan(msg)
        else:
            pr.white(msg)
    for line in res.reorders:
        pr.amber(line)
    for e in res.errors:
        pr.red(f"ERROR {e}")
    pr.summary("OK", counts["OK"])
    pr.summary("CHANGED", counts["CHANGED"])
    pr.summary("NOT FOUND", counts["NOT FOUND"])
    pr.summary("REORDER", len(res.reorders))
    return 1 if counts["NOT FOUND"] or res.errors else 0


def write_all(texts: dict[str, str], res: Result) -> None:
    for rel, new in res.new_texts.items():
        if new != texts[rel]:
            rel_path(rel).write_text(new, encoding="utf-8")


def renumber() -> None:
    from scripts.renumber_footnotes import (
        get_ordered_files_for_folder,
        renumber_footnotes_in_files,
    )

    warnings: list[str] = []
    for course in ("bpc", "ipc"):
        files = get_ordered_files_for_folder(str(DOCS / course))
        renumber_footnotes_in_files(files, warnings, dry_run=False)
    for w in warnings:
        pr.amber(w)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check/update frequencies and DPD counts in the lessons."
    )
    parser.add_argument(
        "--write", action="store_true", help="Update the docs in place."
    )
    args = parser.parse_args()

    pr.green_tmr("Loading DPD data")
    try:
        data = load_data(CLAIMS)
    except (sqlite3.Error, OSError) as exc:
        pr.no("failed")
        pr.red(str(exc))
        return 1
    pr.yes("ok")
    pr.white(f"DPD release {release_version()}")

    texts = load_texts(CLAIMS)
    res = process(texts, data, CLAIMS, current_year())
    code = report(res)
    if not args.write:
        return code
    if code:
        pr.red("not writing: fix the errors above first")
        return code
    for rel, old in texts.items():
        if rel_path(rel).read_text(encoding="utf-8") != old:
            pr.red(f"{rel} changed on disk since it was read; aborting without writing")
            return 1

    pr.green_tmr("Writing")
    write_all(texts, res)
    pr.yes(f"{sum(1 for k in texts if res.new_texts[k] != texts[k])} files")
    pr.green_tmr("Renumbering footnotes")
    renumber()
    pr.yes("ok")

    pr.green_tmr("Re-checking")
    again = process(load_texts(CLAIMS), data, CLAIMS, current_year())
    changed = [r for r in again.rows if r.status != "OK"]
    if changed or again.reorders or again.errors:
        pr.no("not clean")
        for r in changed:
            pr.amber(f"{r.file}:{r.line} {r.label} {r.status}")
        return 1
    pr.yes("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
