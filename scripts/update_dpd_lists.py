"""Rebuild the five DPD-derived word lists in the BPC docs from the local DPD database."""

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

from tools.printer import printer as pr

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
DB_PATH = os.environ.get("DPD_DB", "/Users/deva/Documents/dpd-db/dpd.db")

ALPHABET = (
    "a ā i ī u ū e o k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh "
    "m y r l v s h ḷ ṃ"
).split()
LETTER_RANK = {letter: i for i, letter in enumerate(ALPHABET)}
ASPIRATED = {"kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh"}
SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
POWER_RE = re.compile(r"10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)")
NUMBER_RE = re.compile(r"\((\d[\d ]*)\)")
IRREGULAR_CASE_RE = re.compile(r"^(by|with|in|of|for|to|from|when|among|at|on)\b")

Row = tuple[str, ...]


def pali_key(word: str) -> list[int]:
    """Sort key for Pāḷi alphabetical order; aspirates are single letters."""
    key: list[int] = []
    i = 0
    while i < len(word):
        if word[i : i + 2] in ASPIRATED:
            key.append(LETTER_RANK[word[i : i + 2]])
            i += 2
            continue
        key.append(LETTER_RANK.get(word[i], len(ALPHABET) + ord(word[i])))
        i += 1
    return key


def clean(lemma: str) -> str:
    """Strip the homonym number from a lemma_1."""
    return re.sub(r" \d.*$", "", lemma)


def group_digits(n: int) -> str:
    """Format an integer with groups of three digits separated by spaces."""
    return f"{n:,}".replace(",", " ")


def word_line(words: list[str], sep: str) -> str:
    """Join words in Pāḷi order."""
    return sep.join(sorted(words, key=pali_key))


def cardinal_rows(rows: list[Row]) -> tuple[list[str], set[str]]:
    """Build L1 table lines and the set of words used. Rows are (lemma_1, stem, meaning_1)."""
    values: dict[str, set[int]] = {}
    regular: dict[int, set[str]] = {}
    irregular: dict[int, set[str]] = {}
    entries: list[tuple[str, int, bool]] = []
    for lemma, stem, meaning in rows:
        found = NUMBER_RE.findall(meaning)
        if len(found) != 1:
            continue
        is_irregular = stem.startswith("!")
        if is_irregular and IRREGULAR_CASE_RE.match(meaning):
            continue
        word = clean(lemma)
        value = int(found[0].replace(" ", ""))
        values.setdefault(word, set()).add(value)
        entries.append((word, value, is_irregular))

    for word, value, is_irregular in entries:
        if value != min(values[word]):
            continue
        target = irregular if is_irregular else regular
        target.setdefault(value, set()).add(word)

    lines: list[str] = []
    used: set[str] = set()
    for value in sorted(regular.keys() | irregular.keys()):
        reg = regular.get(value, set())
        irr = irregular.get(value, set())
        cell = word_line(list(reg), " / ")
        if irr:
            irr_text = f"({word_line(list(irr), ' / ')})"
            cell = f"{cell} / {irr_text}" if cell else irr_text
        shown = group_digits(value) if value >= 1000 else str(value)
        lines.append(f"| {shown} | {cell} |")
        used |= reg | irr
    return lines, used


def large_rows(rows: list[Row], exclude: set[str]) -> list[str]:
    """Build L2 table lines. Rows are (lemma_1, meaning_1, meaning_2)."""
    by_exp: dict[int, set[str]] = {}
    for lemma, m1, m2 in rows:
        m = POWER_RE.search(f"{m1} {m2}")
        if not m:
            continue
        word = clean(lemma)
        if word in exclude:
            continue
        by_exp.setdefault(int(m.group(1).translate(SUPERSCRIPT)), set()).add(word)
    return [
        f"| {word_line(list(words), ' / ')} | 10^{exp} | {group_digits(10**exp)} |"
        for exp, words in sorted(by_exp.items())
    ]


def replace_after_marker(
    text: str, marker: str, new: str | list[str], kind: str
) -> str:
    """Replace the list following a unique marker; kind is 'table', 'line' or 'inline'."""
    if text.count(marker) == 0:
        raise ValueError(f"marker not found: {marker!r}")
    if text.count(marker) > 1:
        raise ValueError(f"marker found more than once: {marker!r}")
    lines = text.split("\n")
    idx = next(i for i, line in enumerate(lines) if marker in line)

    if kind == "inline":
        assert isinstance(new, str)
        pos = lines[idx].index(marker) + len(marker)
        lines[idx] = lines[idx][:pos] + new
        return "\n".join(lines)

    i = idx + 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        raise ValueError(f"no list after marker: {marker!r}")

    if kind == "line":
        assert isinstance(new, str)
        lines[i] = new
        return "\n".join(lines)

    assert isinstance(new, list)
    if not lines[i].startswith("|"):
        raise ValueError(f"no table after marker: {marker!r}")
    start = i
    while i < len(lines) and lines[i].startswith("|"):
        i += 1
    header = lines[start : start + 2]
    lines[start:i] = header + new
    return "\n".join(lines)


def fetch(db: sqlite3.Connection, sql: str) -> list[Row]:
    """Run a query and return all rows."""
    return [tuple(r) for r in db.execute(sql).fetchall()]


def build_lists(db: sqlite3.Connection) -> list[tuple[str, str, str, str | list[str]]]:
    """Return (file, marker, kind, new content) for each of the five lists."""
    card = fetch(
        db,
        "select lemma_1, stem, meaning_1 from dpd_headwords "
        "where pos='card' and meaning_1 != ''",
    )
    card_lines, card_words = cardinal_rows(card)
    large = fetch(
        db,
        "select lemma_1, meaning_1, meaning_2 from dpd_headwords "
        "where meaning_1 like '%10%' or meaning_2 like '%10%'",
    )

    def words(where: str) -> list[str]:
        rows = fetch(
            db,
            f"select lemma_1 from dpd_headwords where {where} and meaning_1 != ''",
        )
        return sorted({clean(r[0]) for r in rows}, key=pali_key)

    return [
        (
            "bpc/class_12/3_card.md",
            "have been *actually* covered by DPD so far",
            "table",
            card_lines,
        ),
        (
            "bpc/class_12/3_card.md",
            "excludes all the “amazing” numbers",
            "table",
            large_rows(large, card_words),
        ),
        (
            "bpc/class_3/5_roots.md",
            "derived from **√bandh**",
            "line",
            " ".join(words("root_key = '√bandh'")),
        ),
        (
            "bpc/class_3/5_roots.md",
            "derived from **√bhū**",
            "line",
            " ".join(words("root_key = '√bhū'")),
        ),
        (
            "bpc/class_14/4_ptp.md",
            "ptp - ",
            "inline",
            ", ".join(words("pos = 'ptp'")),
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write changes in place")
    args = parser.parse_args()

    pr.green_tmr("resolving lists")
    if not Path(DB_PATH).exists():
        pr.no("no DB")
        pr.amber(f"{DB_PATH}: not found (set $DPD_DB)")
        return 1
    db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    texts: dict[str, str] = {}
    original: dict[str, str] = {}
    reports: list[str] = []
    errors: list[str] = []
    try:
        for rel, marker, kind, content in build_lists(db):
            path = DOCS_DIR / rel
            if rel not in texts:
                original[rel] = texts[rel] = path.read_text(encoding="utf-8")
            try:
                new_text = replace_after_marker(texts[rel], marker, content, kind)
            except ValueError as e:
                errors.append(f"{rel}: {e}")
                continue
            if new_text == texts[rel]:
                reports.append(f"{rel} ({marker[:30]}): up to date")
            else:
                old_items = _items(_list_text(texts[rel], marker, kind))
                new_items = _items(_list_text(new_text, marker, kind))
                added, removed = len(new_items - old_items), len(old_items - new_items)
                change = f"+{added} -{removed}" if added or removed else "reordered"
                reports.append(f"{rel} ({marker[:30]}): {change}")
            texts[rel] = new_text
    finally:
        db.close()

    if errors:
        pr.no(f"{len(errors)} errors")
        for e in errors:
            pr.amber(e)
        return 1
    pr.yes("ok")
    for r in reports:
        pr.white(r)

    changed = [rel for rel in texts if texts[rel] != original[rel]]
    if args.write:
        for rel in changed:
            (DOCS_DIR / rel).write_text(texts[rel], encoding="utf-8")
        pr.summary("files written", len(changed))
    elif changed:
        pr.white("dry run: re-run with --write to apply")
    return 0


def _items(text: str) -> set[str]:
    """Return the distinct words in a list text, ignoring digits and separators."""
    return {
        w for w in re.findall(r"[^\s,|/()]+", text) if not re.fullmatch(r"[\d^]+", w)
    }


def _list_text(text: str, marker: str, kind: str) -> str:
    """Return the raw list text after a marker, for added/removed counts."""
    lines = text.split("\n")
    idx = next(i for i, line in enumerate(lines) if marker in line)
    if kind == "inline":
        return lines[idx][lines[idx].index(marker) + len(marker) :]
    i = idx + 1
    while lines[i].strip() == "":
        i += 1
    if kind == "line":
        return lines[i]
    out = []
    while i < len(lines) and lines[i].startswith("|"):
        out.append(lines[i])
        i += 1
    return "\n".join(out[2:])


if __name__ == "__main__":
    sys.exit(main())
