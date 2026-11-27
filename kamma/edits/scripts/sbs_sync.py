"""Search, check and edit the SBS table in dpd-db so course keys and SBS example fields stay in sync; DB path from $DPD_DB or the default below, writes only with --apply."""

import argparse
import difflib
import json
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

DB = os.environ.get("DPD_DB", "/Users/deva/Documents/dpd-db/dpd.db")

GROUPS: dict[str, list[str]] = {
    "class": [
        "class_source",
        "class_sutta",
        "class_example",
        "class_example_translation",
        "class_extra",
        "class_anki",
    ],
    "sbs_1": [
        "sbs_source_1",
        "sbs_sutta_1",
        "sbs_example_1",
        "sbs_chant_pali_1",
        "sbs_chant_eng_1",
        "sbs_chapter_1",
    ],
    "sbs_2": [
        "sbs_source_2",
        "sbs_sutta_2",
        "sbs_example_2",
        "sbs_chant_pali_2",
        "sbs_chant_eng_2",
        "sbs_chapter_2",
    ],
    "dhp": ["dhp_source", "dhp_sutta", "dhp_example"],
    "pat": ["pat_source", "pat_sutta", "pat_example"],
    "vib": ["vib_source", "vib_sutta", "vib_example"],
    "discourses": ["discourses_source", "discourses_sutta", "discourses_example"],
    "extra": ["extra_source", "extra_sutta", "extra_example"],
}
INT_COLS = {"class_anki", "sbs_class", "sbs_index"}

NOUN_POS = {"masc", "nt", "fem"}
VERB_POS = {"pr", "aor", "fut", "imp", "opt", "perf", "cond"}
POS_ALIAS = {"ger": "abs"}  # DPD ger = key abs


def norm(text: str) -> str:
    """Pāli sentence key: no tags, apostrophes, punctuation, case or extra spaces."""
    text = re.sub(r"\[\^\w+\]", "", re.sub(r"<[^>]+>", "", text))
    text = unicodedata.normalize("NFC", text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())


EXAMPLE_MIN_WORDS = 4
EXAMPLE_COVERAGE = 0.80


ITEM_MARK_RE = re.compile(r"^\s*(?:\([^)]*\)|[A-Z][A-Za-z-]*\.?\s?\d[\d.,:-]*)\s*")


def strip_item_marks(text: str) -> str:
    """Remove leading `(simpl)`-style and citation marks (`UD-a 43`, `DNa2.3`) from a key sentence."""
    while True:
        stripped = ITEM_MARK_RE.sub("", text, count=1)
        if stripped == text:
            return text
        text = stripped


def example_coverage(a: str, b: str) -> float:
    """Share of the shorter sentence's words found in the longer one (0.0 if it has under EXAMPLE_MIN_WORDS words)."""
    wa, wb = norm(strip_item_marks(a)).split(), norm(strip_item_marks(b)).split()
    short, long_ = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
    if len(short) < EXAMPLE_MIN_WORDS:
        return 0.0
    have = set(long_)
    return sum(w in have for w in short) / len(short)


def example_matches(a: str, b: str) -> bool:
    """True when two Pāli sentences are the same or near-identical (see example_coverage)."""
    return example_coverage(a, b) >= EXAMPLE_COVERAGE


def norm_tr(text: str) -> str:
    """Translation key: no tags, footnote markers or markdown bold, whitespace collapsed."""
    text = re.sub(r"\[\^\w+\]", "", re.sub(r"<[^>]+>", "", text)).replace("**", "")
    return " ".join(text.split())


def bold_word(example: str) -> str:
    m = re.search(r"<b>(.*?)</b>", example)
    return m.group(1) if m else ""


def connect(write: bool) -> sqlite3.Connection:
    if write:
        return sqlite3.connect(DB)
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)


def cols_of(con: sqlite3.Connection) -> list[str]:
    return [r[1] for r in con.execute("pragma table_info(sbs)")]


def headword(con: sqlite3.Connection, hid: int) -> tuple[str, str]:
    r = con.execute(
        "select lemma_1, pos from dpd_headwords where id = ?", (hid,)
    ).fetchone()
    return (r[0], r[1]) if r else ("?", "?")


def ex_col(group: str) -> str:
    return next(c for c in GROUPS[group] if "example" in c and "translation" not in c)


def resolve_ids(con: sqlite3.Connection, word: str) -> list[int]:
    if word.isdigit():
        return [int(word)]
    rows = con.execute(
        "select id from dpd_headwords where lemma_1 = ? or lemma_1 like ? order by lemma_1",
        (word, word + " %"),
    ).fetchall()
    return [r[0] for r in rows]


def fmt_row(con: sqlite3.Connection, hid: int, group: str) -> list[str]:
    lemma, pos = headword(con, hid)
    names = GROUPS[group]
    r = con.execute(
        f"select {', '.join(names)} from sbs where id = ?", (hid,)
    ).fetchone()
    out = [f"{hid} | {lemma} | {pos}"]
    if r is None:
        out.append("   (no sbs row)")
        return out
    for name, val in zip(names, r):
        if val not in ("", 0, None):
            out.append(f"   {name}: {str(val).replace(chr(10), ' / ')}")
    return out


# ---------- commands ----------


def cmd_show(a: argparse.Namespace) -> int:
    con = connect(False)
    for w in a.words:
        ids = resolve_ids(con, w)
        if not ids:
            print(f"-- {w}: no headword")
        for hid in ids:
            print("\n".join(fmt_row(con, hid, a.group)))
    return 0


def matching_ids(con: sqlite3.Connection, a: argparse.Namespace) -> list[int]:
    names = GROUPS[a.group]
    where, params = [f"{ex_col(a.group)} != ''"], []
    if a.group == "class" and a.cls is not None:
        where.append("class_anki = ?")
        params.append(a.cls)
    if a.source:
        src = names[0]
        where.append(f"({src} = ? or {src} like ?)")
        params += [a.source, a.source + " %"]
    sql = f"select id, {', '.join(names)} from sbs where {' and '.join(where)} order by id"
    return (
        [r[0] for r in con.execute(sql, params)]
        if not a.text
        else _filter_text(con, sql, params, a)
    )


def _filter_text(
    con: sqlite3.Connection, sql: str, params: list, a: argparse.Namespace
) -> list[int]:
    needle_p, needle_t = norm(a.text), norm_tr(a.text).lower()
    names = GROUPS[a.group]
    out = []
    for r in con.execute(sql, params):
        vals = dict(zip(names, r[1:]))
        hay = " ".join(
            str(v) for k, v in vals.items() if "example" in k or "chant" in k
        )
        if needle_p in norm(hay) or needle_t in norm_tr(hay).lower():
            out.append(r[0])
    return out


def cmd_find(a: argparse.Namespace) -> int:
    con = connect(False)
    ids = matching_ids(con, a)
    for hid in ids:
        print("\n".join(fmt_row(con, hid, a.group)))
    print(f"-- {len(ids)} rows")
    return 0


def _coerce(col: str, val: str) -> int | str:
    return int(val) if col in INT_COLS else val


def cmd_set(a: argparse.Namespace) -> int:
    con = connect(a.apply)
    valid = set(cols_of(con)) - {"id"}
    lemma, pos = headword(con, a.id)
    if con.execute("select 1 from sbs where id = ?", (a.id,)).fetchone() is None:
        print(f"!! {a.id} {lemma}: no sbs row")
        return 1
    changes: dict[str, int | str] = {}
    for pair in a.pairs:
        col, sep, val = pair.partition("=")
        if not sep or col not in valid:
            print(f"!! bad field: {pair}")
            return 1
        changes[col] = _coerce(col, val.replace("\\n", "\n"))
    old = con.execute(
        f"select {', '.join(changes)} from sbs where id = ?", (a.id,)
    ).fetchone()
    print(f"{a.id} | {lemma} | {pos}")
    for (col, new), o in zip(changes.items(), old):
        print(f"   {col}: {o!r}\n   {' ' * len(col)}→ {new!r}")
    if a.apply:
        sets = ", ".join(f"{c} = ?" for c in changes)
        con.execute(f"update sbs set {sets} where id = ?", (*changes.values(), a.id))
        con.commit()
        print("-- written")
    else:
        print("-- dry run, add --apply to write")
    return 0


def source_col(field_name: str) -> str:
    """The *_source column of the group that holds field_name."""
    for names in GROUPS.values():
        if field_name in names:
            return names[0]
    return "class_source"


def tag_replace(val: str, old: str, new: str) -> tuple[str, int, bool]:
    """Replace old with new in the text of val, ignoring <b> tags, and keep the bold on the same letters.

    Returns (new value, number of replacements, conflict). A conflict means the changed letters straddle a
    bold boundary; the value is then returned unchanged.
    """
    if re.search(r"<(?!/?b>)[^>]+>", val):
        return (val.replace(old, new), val.count(old), False)
    chars: list[tuple[str, bool]] = []
    bold = False
    for part in re.split(r"(</?b>)", val):
        if part in ("<b>", "</b>"):
            bold = part == "<b>"
        else:
            chars += [(c, bold) for c in part]
    plain = "".join(c for c, _ in chars)
    if not old or old not in plain:
        return (val, 0, False)
    pre = len(_common_prefix(old, new))
    suf = len(_common_prefix(old[pre:][::-1], new[pre:][::-1]))
    out: list[tuple[str, bool]] = []
    i = n = 0
    while True:
        j = plain.find(old, i)
        if j < 0:
            break
        seg = chars[j : j + len(old)]
        mid = seg[pre : len(old) - suf]
        flags = {b for _, b in mid}
        if len(flags) > 1:
            return (val, 0, True)
        mid_bold = (
            flags.pop()
            if flags
            else (seg[pre - 1][1] if pre else seg[-1][1] if seg else False)
        )
        out += chars[i:j] + seg[:pre]
        out += [(c, mid_bold) for c in new[pre : len(new) - suf]]
        out += seg[len(old) - suf :]
        i = j + len(old)
        n += 1
    out += chars[i:]
    res, cur = "", False
    for c, b in out:
        if b != cur:
            res += "<b>" if b else "</b>"
            cur = b
        res += c
    return (res + ("</b>" if cur else ""), n, False)


def _common_prefix(a: str, b: str) -> str:
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return a[:k]


def cmd_replace(a: argparse.Namespace) -> int:
    con = connect(a.apply)
    if a.field not in cols_of(con):
        print(f"!! unknown field {a.field}")
        return 1
    if a.field in INT_COLS:
        print(f"!! replace is for text fields; use set for {a.field}")
        return 1
    if re.search(r"</?b>", a.new):
        print(
            "!! no <b> tags in the new text: replace keeps the existing bold; use set to move it"
        )
        return 1
    a.old = re.sub(r"</?b>", "", a.old)
    where, params = ["1"], []
    if a.cls is not None:
        where.append("class_anki = ?")
        params.append(a.cls)
    if a.source:
        src = source_col(a.field)
        where.append(f"({src} = ? or {src} like ?)")
        params += [a.source, a.source + " %"]
    rows = con.execute(
        f"select id, {a.field} from sbs where {' and '.join(where)}", params
    ).fetchall()
    changes: list[tuple[str, int]] = []
    conflicts = 0
    for hid, val in rows:
        res, n, conflict = tag_replace(val or "", a.old, a.new)
        if conflict:
            conflicts += 1
            print(
                f"!! {hid}: the change crosses a <b> boundary, edit it with set:\n   {val!r}"
            )
        elif n:
            lemma, pos = headword(con, hid)
            print(f"{hid} | {lemma} | {pos}\n   - {val!r}\n   + {res!r}")
            changes.append((res, hid))
    print(f"-- {len(changes)} rows" + (f", {conflicts} conflicts" if conflicts else ""))
    if a.apply and changes:
        con.executemany(f"update sbs set {a.field} = ? where id = ?", changes)
        con.commit()
        print("-- written")
    elif changes:
        print("-- dry run, add --apply to write")
    return 1 if conflicts else 0


def cmd_move(a: argparse.Namespace) -> int:
    if a.src == a.dst:
        print("!! source and target are the same row")
        return 1
    con = connect(a.apply)
    names = GROUPS[a.group]
    src = con.execute(
        f"select {', '.join(names)} from sbs where id = ?", (a.src,)
    ).fetchone()
    if src is None or not src[names.index(ex_col(a.group))]:
        print(f"!! {a.src}: no {a.group} data to move")
        return 1
    if (
        con.execute("select 1 from dpd_headwords where id = ?", (a.dst,)).fetchone()
        is None
    ):
        print(f"!! {a.dst}: no such headword")
        return 1
    dst = con.execute(
        f"select {', '.join(names)} from sbs where id = ?", (a.dst,)
    ).fetchone()
    if dst is not None and dst[names.index(ex_col(a.group))] and not a.force:
        print(f"!! {a.dst} already has {a.group} data (use --force to overwrite):")
        print("\n".join(fmt_row(con, a.dst, a.group)))
        return 1
    print("FROM", "\n".join(fmt_row(con, a.src, a.group)))
    print("TO  ", "\n".join(fmt_row(con, a.dst, a.group)))
    if not a.apply:
        print(
            "-- dry run, add --apply to write"
            + ("" if dst is not None else " (target sbs row will be created)")
        )
        return 0
    if dst is None:
        con.execute(_insert_blank_sql(con), (a.dst,))
    sets = ", ".join(f"{c} = ?" for c in names)
    con.execute(f"update sbs set {sets} where id = ?", (*src, a.dst))
    blanks = [0 if c in INT_COLS else "" for c in names]
    con.execute(f"update sbs set {sets} where id = ?", (*blanks, a.src))
    con.commit()
    print("-- written")
    return 0


def cmd_clear(a: argparse.Namespace) -> int:
    con = connect(a.apply)
    names = GROUPS[a.group]
    if con.execute("select 1 from sbs where id = ?", (a.id,)).fetchone() is None:
        print(f"!! {a.id}: no sbs row")
        return 1
    print("CLEAR", "\n".join(fmt_row(con, a.id, a.group)))
    if not a.apply:
        print("-- dry run, add --apply to write")
        return 0
    sets = ", ".join(f"{c} = ?" for c in names)
    blanks = [0 if c in INT_COLS else "" for c in names]
    con.execute(f"update sbs set {sets} where id = ?", (*blanks, a.id))
    con.commit()
    print("-- written")
    return 0


def cmd_restore(a: argparse.Namespace) -> int:
    """Put sbs rows back to a JSON backup made with `sqlite3 -json … select * from sbs where id in (…)`."""
    rows = json.loads(Path(a.backup).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not all(
        isinstance(r, dict) and "id" in r for r in rows
    ):
        print(f"!! {a.backup}: not a list of sbs rows with an id")
        return 1
    con = connect(a.apply)
    valid = set(cols_of(con))
    for r in rows:
        if unknown := set(r) - valid:
            print(f"!! {r['id']}: unknown fields {sorted(unknown)}")
            return 1
    changed = 0
    for r in rows:
        hid, cols = r["id"], [c for c in r if c != "id"]
        lemma, pos = headword(con, hid)
        cur = con.execute(
            f"select {', '.join(cols)} from sbs where id = ?", (hid,)
        ).fetchone()
        if cur is None:
            print(
                f"{hid} | {lemma} | {pos}\n   (no sbs row: insert it from the backup)"
            )
        else:
            diffs = [(c, o) for c, o in zip(cols, cur) if o != r[c]]
            if not diffs:
                continue
            print(f"{hid} | {lemma} | {pos}")
            for c, o in diffs:
                print(f"   {c}: {o!r}\n   {' ' * len(c)}→ {r[c]!r}")
        changed += 1
        if a.apply:
            if cur is None:
                con.execute(
                    f"insert into sbs (id, {', '.join(cols)}) values (?, {', '.join('?' * len(cols))})",
                    (hid, *(r[c] for c in cols)),
                )
            else:
                sets = ", ".join(f"{c} = ?" for c in cols)
                con.execute(
                    f"update sbs set {sets} where id = ?", (*(r[c] for c in cols), hid)
                )
    print(f"-- {changed} of {len(rows)} rows differ from the backup")
    if not a.apply:
        print("-- dry run, add --apply to write")
        return 0
    con.commit()
    print("-- written")
    return 0


def _insert_blank_sql(con: sqlite3.Connection) -> str:
    cols = [c for c in cols_of(con) if c != "id"]
    vals = [
        "NULL" if c == "sbs_index" else ("0" if c in INT_COLS else "''") for c in cols
    ]
    return f"insert into sbs (id, {', '.join(cols)}) values (?, {', '.join(vals)})"


# ---------- check ----------


@dataclass
class Sentence:
    """One key sentence: study-tools builds this too; keep the fields stable."""

    line: int
    source: str
    pali: str
    translation: str = ""
    table: list[tuple[str, str]] = field(default_factory=list)  # (pāli cell, pos cell)


def parse_key(text: str) -> list[Sentence]:
    """One Sentence per analysis table: the Pāli is the text block just above it, the translation the first bold line below it."""
    lines = text.splitlines()
    out: list[Sentence] = []
    source = ""
    cur: Sentence | None = None
    more = False
    i = 0
    while i < len(lines):
        raw = lines[i]
        ref = re.match(r"^(?:\d+\\?\.\s+|\*\*)?\[([^\]]+)\]\([^)]*\)\**\s*(.*)$", raw)
        if ref:
            tail = re.match(r"\(simpl\)", ref.group(2))
            source = ref.group(1) + (" (simpl)" if tail else "")
        if raw.startswith("|") and (i == 0 or not lines[i - 1].startswith("|")):
            block: list[str] = []
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            while j >= 0 and lines[j].strip() and not _is_boundary(lines[j]):
                block.insert(0, lines[j].strip())
                j -= 1
            bare = re.match(r"^\d+\\?\.\s+([^\[].*)$", lines[j]) if j >= 0 else None
            if bare:
                block.insert(0, bare.group(1).strip())
            follows_tr = j >= 0 and re.match(r"^\*\*[^*].*\*\*\s*$", lines[j].strip())
            if not block and cur is not None and cur.translation and follows_tr:
                more = (
                    True  # a split sentence: this table and its bold line continue cur
                )
            else:
                cur = Sentence(i + 1, source, "\n".join(block))
                out.append(cur)
                more = False
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if (
                    len(cells) >= 2
                    and cells[0]
                    and not set(cells[0]) <= {"-", " ", ":"}
                    and cells[0] != "Pāli"
                ):
                    gram = cells[2] if len(cells) > 2 else ""
                    cur.table.append(
                        (cells[0].replace("\\#", "").lstrip("#"), f"{cells[1]} {gram}")
                    )
                i += 1
            continue
        if (
            cur is not None
            and (not cur.translation or more)
            and re.match(r"^\*\*[^*].*\*\*\s*$", raw)
            and not ref
        ):
            cur.translation = (
                f"{cur.translation} {raw.strip()}".strip() if more else raw.strip()
            )
            more = False
        i += 1
    return [s for s in out if s.pali]


def _is_boundary(line: str) -> bool:
    s = line.strip()
    return (
        s.startswith(("|", "#", "---"))
        or bool(re.match(r"^\d+\\?\.\s", s))
        or bool(re.match(r"^\*\*.*\*\*$", s))
    )


def pos_ok(dpd_pos: str, key_pos: str) -> bool:
    mapped = (
        "noun" if dpd_pos in NOUN_POS else "verb" if dpd_pos in VERB_POS else dpd_pos
    )
    tokens = set(re.findall(r"[a-z]+", key_pos.lower()))
    return mapped in tokens or dpd_pos in tokens or POS_ALIAS.get(dpd_pos) in tokens


@dataclass
class Issue:
    kind: str  # TRANS | PALI | POS | NO-SBS | ORPHAN
    ids: str  # comma-joined sbs ids, or the key line for NO-SBS
    msg: str
    pali: str = ""  # normalised key sentence the issue belongs to ("" for ORPHAN)


def load_rows(
    con: sqlite3.Connection, group: str, where: str, params: tuple = ()
) -> list[tuple]:
    """SBS rows of a group with an example, as (id, lemma_1, pos, source, example, translation or "", example_1, example_2)."""
    cols = GROUPS[group]
    source = next(c for c in cols if "source" in c)
    trans = next((f"s.{c}" for c in cols if "translation" in c), "''")
    ex = ex_col(group)
    return con.execute(
        f"select s.id, h.lemma_1, h.pos, s.{source}, s.{ex}, {trans}, h.example_1, h.example_2 "
        f"from sbs s join dpd_headwords h on h.id = s.id where ({where}) and s.{ex} != ''",
        params,
    ).fetchall()


def check_key(
    con: sqlite3.Connection, text: str, cls: int, label: str
) -> tuple[list[Issue], str]:
    return compare(
        parse_key(text),
        load_rows(con, "class", "s.class_anki = ?", (cls,)),
        label,
        f"class {cls}",
    )


def compare(
    sentences: list[Sentence], rows: list[tuple], label: str, scope: str
) -> tuple[list[Issue], str]:
    """Pair key sentences with SBS rows (see load_rows) and list the differences; scope names the group in ORPHAN messages.

    TRANS needs a key translation, so Sentences built with translation="" (groups without a translation column) never give TRANS.
    """
    by_ex: dict[str, list[tuple]] = {}
    for r in rows:
        by_ex.setdefault(norm(r[4]), []).append(r)
    keyed = [(norm(s.pali), s) for s in sentences]
    issues: list[Issue] = []
    partial = 0
    used: set[int] = set()
    for ex, hits in by_ex.items():
        exact = [s for k, s in keyed if k == ex]
        part = [s for k, s in keyed if ex and ex in k] if not exact else []
        wide = [s for k, s in keyed if k and k in ex] if not (exact or part) else []
        near = [] if (exact or part or wide) else _near(ex, keyed)
        chunks = exact or part or wide or near
        ids = ",".join(str(h[0]) for h in hits)
        if near:
            msg = (
                f"{label}:{near[0].line} {near[0].source} ids {ids} | Pāli spelling differs from the key"
                f"\n   key: {' / '.join(near[0].pali.splitlines())}"
                f"\n   db : {' / '.join(hits[0][4].splitlines())}"
            )
            issues.append(Issue("PALI", ids, msg, norm(near[0].pali)))
            exact = near
        if not chunks:
            first = hits[0][4].splitlines()[0][:70]
            issues.append(
                Issue("ORPHAN", ids, f"{scope} {hits[0][3]} ids {ids} | {first}")
            )
            continue
        s = chunks[0]
        used.update(c.line for c in chunks)
        loc = f"{label}:{s.line} {s.source}"
        db_trs = {norm_tr(h[5]) for h in hits}
        if exact and s.translation and db_trs != {norm_tr(s.translation)}:
            msg = f"{loc} ids {ids}\n   key: {norm_tr(s.translation)}"
            msg += "".join(f"\n   db : {t}" for t in sorted(db_trs))
            issues.append(Issue("TRANS", ids, msg, norm(s.pali)))
        if part or wide:
            partial += 1
        cells: dict[str, str] = {}
        for chunk in chunks:
            for c, p in chunk.table:
                cells.setdefault(norm(c), p)
        for hid, lemma, pos, _src, exs, _tr, dpd_ex1, dpd_ex2 in hits:
            key_pos = cells.get(norm(bold_word(exs)))
            if key_pos is not None and not pos_ok(pos, key_pos):
                msg = f"{loc} id {hid} {lemma} | dpd {pos} vs key '{key_pos.strip()}' ({bold_word(exs)})"
                if any(example_matches(e or "", s.pali) for e in (dpd_ex1, dpd_ex2)):
                    msg += " | DPD example = this sentence: question the key"
                issues.append(Issue("POS", str(hid), msg, norm(s.pali)))
    for s in sentences:
        if s.line not in used:
            msg = f"{label}:{s.line} {s.source} | {s.pali.splitlines()[0][:70]}"
            issues.append(Issue("NO-SBS", str(s.line), msg, norm(s.pali)))
    summary = (
        f"-- {len(sentences)} sentences, {len(rows)} sbs rows, {{n}} issues"
        f" ({partial} fragment matches: translation not compared)"
    )
    return issues, summary


NEAR_RATIO = 0.85


def _near(ex: str, keyed: list[tuple[str, "Sentence"]]) -> list["Sentence"]:
    """The key sentence that is a spelling variant of ex (similarity >= NEAR_RATIO), if any."""
    best, best_r = None, NEAR_RATIO
    for k, s in keyed:
        sm = difflib.SequenceMatcher(None, ex, k)
        if sm.real_quick_ratio() >= best_r and sm.quick_ratio() >= best_r:
            r = sm.ratio()
            if r >= best_r:
                best, best_r = s, r
    return [best] if best else []


def _ikey(i: Issue) -> tuple[str, str]:
    return (i.kind, i.pali if i.kind == "NO-SBS" else i.ids)


def text_at(path: Path, rev: str) -> str:
    """The text of path at git revision rev; ValueError(stderr) if git cannot show it."""
    old = subprocess.run(
        ["git", "-C", str(path.resolve().parent), "show", f"{rev}:./{path.name}"],
        capture_output=True,
        text=True,
    )
    if old.returncode != 0:
        raise ValueError(old.stderr.strip())
    return old.stdout


def new_since(issues_now: list[Issue], issues_then: list[Issue]) -> list[Issue]:
    """The issues of issues_now that issues_then did not already have (same kind and target)."""
    before = {_ikey(i) for i in issues_then}
    return [i for i in issues_now if _ikey(i) not in before]


def cmd_check(a: argparse.Namespace) -> int:
    con = connect(False)
    path = Path(a.key)
    num = re.match(r"\d+", path.name)
    if a.cls is None and num is None:
        print(f"!! {path.name}: no class number in the file name, pass --class")
        return 1
    cls = a.cls if a.cls is not None else int(num.group()) if num else 0
    text = path.read_text(encoding="utf-8")
    issues, summary = check_key(con, text, cls, str(path))
    if a.since:
        try:
            old_text = text_at(path, a.since)
        except ValueError as err:
            print(f"!! cannot read {path} at {a.since}: {err}")
            return 1
        issues = new_since(issues, check_key(con, old_text, cls, str(path))[0])
        summary += f", showing only issues new since {a.since}"
    if a.only:
        issues = [i for i in issues if i.kind in a.only]
        summary += f", only {' '.join(a.only)}"
    for i in issues:
        print(f"{i.kind:<7} {i.msg}")
    print(summary.format(n=len(issues)))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    grp = {"choices": list(GROUPS), "default": "class"}

    s = sub.add_parser("show", help="print a headword's sbs group fields")
    s.add_argument("words", nargs="+", help="lemma_1 or id")
    s.add_argument("--group", **grp)
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("find", help="search a group's example/translation")
    s.add_argument("text", nargs="?", default="")
    s.add_argument("--group", **grp)
    s.add_argument("--class", dest="cls", type=int)
    s.add_argument("--source")
    s.set_defaults(fn=cmd_find)

    s = sub.add_parser("set", help="set fields of one sbs row")
    s.add_argument("id", type=int)
    s.add_argument("pairs", nargs="+", help="field=value (\\n for newline)")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_set)

    s = sub.add_parser("replace", help="replace text in one field across rows")
    s.add_argument("old")
    s.add_argument("new")
    s.add_argument("--field", required=True)
    s.add_argument("--class", dest="cls", type=int)
    s.add_argument("--source")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_replace)

    s = sub.add_parser("move", help="move a group's data from one headword to another")
    s.add_argument("src", type=int)
    s.add_argument("dst", type=int)
    s.add_argument("--group", **grp)
    s.add_argument("--force", action="store_true")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_move)

    s = sub.add_parser("clear", help="empty a group's fields on one row")
    s.add_argument("id", type=int)
    s.add_argument("--group", **grp)
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_clear)

    s = sub.add_parser(
        "restore", help="put sbs rows back to a JSON backup (sqlite3 -json output)"
    )
    s.add_argument("backup", help="backup file, e.g. kamma/edits/backups/….json")
    s.add_argument("--apply", action="store_true")
    s.set_defaults(fn=cmd_restore)

    s = sub.add_parser("check", help="compare a key file with sbs class_* rows")
    s.add_argument("key")
    s.add_argument(
        "--class", dest="cls", type=int, help="default: leading number of the file name"
    )
    s.add_argument(
        "--since",
        help="git rev: show only issues the key at that rev did not have (issues are matched by sbs ids,"
        " so a translation that was already wrong and is changed to another wrong value is not shown)",
    )
    s.add_argument(
        "--only",
        nargs="+",
        choices=["TRANS", "PALI", "POS", "ORPHAN", "NO-SBS"],
        help="show only these issue kinds (e.g. --only TRANS for the translation sync)",
    )
    s.set_defaults(fn=cmd_check)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
