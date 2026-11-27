"""Verify BPC/IPC answer keys against their exercises and a tag vocabulary (10a), optionally against the DPD database (10b).

Run (exit 0 is required before any commit touching the keys):
    uv run python kamma/edits/scripts/verify_key.py                       # structural checks, both courses
    uv run python kamma/edits/scripts/verify_key.py --course bpc|ipc|all
    uv run python kamma/edits/scripts/verify_key.py --warnings            # also list word-coverage warnings (never affect exit code)
    uv run python kamma/edits/scripts/verify_key.py --course all --dpd --report temp/key_dpd_report.tsv

Structural checks (gating, exit 1 on error): numbering vs the exercise files, POS vocabulary, Grammar
vocabulary, root-cell format, compound-type spelling (ipc), stray characters. A hand edit that breaks a
tag format is caught here.

--dpd [PATH] checks every row against the local DPD SQLite DB (default
/Users/deva/Documents/dpd-db/dpd.db; local-only; advisory: never affects the exit code).
--report defaults to temp/key_dpd_report.tsv (git-ignored). Output is deterministic.
The DPD layer (tag parsing, readings, buckets) lives in dpd_check.py, shared with study-tools;
the report columns and row_key stay here.

DPD buckets (each key row gets one):
    IMPOSSIBLE      the key's tag is not among the DPD readings of the form (likely a real error)
    NOT-FOUND       the form is not in DPD, or DPD has no reading for it
    ROOT-MISMATCH   key root differs from the DPD root
    EXAMPLE-CONFLICT  a DPD headword quotes this key sentence in example_1/example_2 and the key's
                    POS/grammar disagrees with it (owner rule: the DPD reading wins unless it is a real error)
    AMBIGUOUS       tag is a valid DPD reading, but the form has other readings (gen/dat, nom/acc,
                    gender only, ...); only the sentence can decide
    CONFIRMED / SKIPPED   fine / not checkable (multi-alternative Grammar cells); not reviewed

Report columns (TSV):
    row_key course file line section item occ word pos grammar root gloss sentence translation check
    bucket dpd_readings
- row_key = course/file/section/item/word/occ (e.g. ipc/16_class.md/main/4/aṅgāni/1). It contains no
  tag, so it survives a tag correction. Always key by row_key; `line` shifts after edits.
- The same row can appear in two buckets, so a row_key may repeat in the report. Take the first one.
- Course ranges: bpc classes 1-15, ipc classes 16-29.

Key table format (what edits touch): row `| word | pos | grammar | gloss | root |`. Gotchas:
- Word cell may be `\\#word` or `**word**`; compare after stripping `\\#` and `*`.
- Split cells on `|` (not ` | `): rows with an empty root cell end `| |`.
- Root cells use DPD style `√kar･7 \\*e (do, make)`, not bare `√kar`.
- Causatives: POS `verb.caus`, grammar without "caus" (e.g. `opt.3rd.sg`).
- Keep `<br>` and backslash escapes verbatim; do not lose the trailing `|`.
"""

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from kamma.edits.scripts.dpd_check import (
    BUCKETS,
    FOOTNOTE_RE,
    DpdFinding,
    classify_rows,
    open_db,
    split_cells,
    strip_annotations,
    write_tsv,
)
from kamma.edits.scripts.sbs_sync import example_matches
from tools.printer import printer as pr

ROOT_DIR = Path(__file__).resolve().parents[3]  # kamma/edits/scripts/ → repo root
COURSES: dict[str, tuple[str, str, range]] = {
    "bpc": ("docs/bpc_key", "docs/bpc_ex", range(1, 16)),
    "ipc": ("docs/ipc_key", "docs/ipc_ex", range(16, 30)),
}

# ---------------------------------------------------------------- vocabulary

POS_WORDS = {
    "noun", "ind", "verb", "pron", "adj", "pp", "prp", "ptp", "app", "card",
    "ordin", "idiom", "sandhi", "prefix", "suffix", "consonant", "proper",
    "caus", "pass", "interr", "comp", "comparative", "as", "agent", "-", "",
}  # fmt: skip
TENSES = ("pr", "aor", "fut", "opt", "imp", "imperf", "perf", "cond")
SIMPLE_GRAMMAR = {
    "adv", "conj", "neg", "emph", "abs", "ger", "inf", "interr", "prep",
    "quote", "quotation mark", "question marker", "excl", "cond", "disj",
    "impers", "ind", "idiom", "prohib", "gen abs", "loc abs", "-", "",
} | POS_WORDS | set(TENSES)  # fmt: skip
COMPOUND_ALLOWED = {
    "tappurisa", "kammadhāraya", "bahubbīhi", "dvanda", "abyayībhāva", "digu",
    "dutiyā", "tatiyā", "catutthī", "pañcamī", "chaṭṭhī", "sattamī",
}  # fmt: skip
COMPOUND_TRIGGER = re.compile(
    "tapp|kammadh|bahubb|dvand|abyay|avyay|digu|chaṭṭ|sattam|dutiy|tatiy|catut|pañcam"
)
PALI_ASCII = set("abcdeghijklmnoprstuvyABCDEGHIJKLMNOPRSTUVY")

_G = r"(?:masc|fem|nt|x|1st|2nd|3rd)"
_C = r"(?:nom|acc|instr|dat|abl|gen|loc|voc)"
_N = r"(?:sg|pl|dual)"
_P = r"(?:1st|2nd|3rd)"
_T = "(?:" + "|".join(TENSES) + ")"
_M = r"(?:caus|pass|reflx)"
_POS = "(?:" + "|".join(sorted(w for w in POS_WORDS if w.isalpha())) + ")"
INFLECTION = re.compile(
    rf"^(?:{_POS}\.)?(?:{_G}(?:\.?/{_G})*\.)?{_C}(?:/{_C})*\.{_N}(?:/{_N})*$"
)
VERB = re.compile(rf"^(?:{_M}\.)*{_T}\.(?:{_M}\.)*{_P}(?:/{_P})*\.{_N}(?:/{_N})*$")
STEM = re.compile(r"^(?:masc|fem|nt|x)\.?$")
ROOT_FORMAT = re.compile(r"^[^\s√]*√\S+[･×]\d+ [^()]+ \([^()]+\).*$")
ROOT_APPLIES = re.compile(r"[･×]\d")

# ---------------------------------------------------------------- data model


@dataclass
class Finding:
    course: str
    file: str
    line: int
    check: str
    message: str
    severity: str = "error"

    def __str__(self) -> str:
        return f"{self.file}:{self.line} {self.check}: {self.message}"


@dataclass
class Row:
    course: str
    file: str
    line: int
    section: str
    item: int
    occ: int
    cells: list[str]
    sentence: str = ""
    translation: str = ""

    @property
    def word(self) -> str:
        return clean_word(self.cells[0])

    @property
    def pos(self) -> str:
        return self.cells[1]

    @property
    def grammar(self) -> str:
        return self.cells[2] if len(self.cells) > 2 else ""

    @property
    def headword_ids(self) -> tuple[int, ...]:
        return ()

    @property
    def dpd_root(self) -> tuple[str, str] | None:
        """(`√root`, group) of a 5-cell row's root cell, else None."""
        if len(self.cells) != 5:
            return None
        m = ROOT_CELL.search(self.cells[4].replace("\\*", "*"))
        return ("√" + m.group(1), m.group(2)) if m else None


@dataclass
class Doc:
    course: str
    file: str
    main: list[int] = field(default_factory=list)
    extra: list[int] = field(default_factory=list)
    rows: list[Row] = field(default_factory=list)
    problems: list[Finding] = field(default_factory=list)


# ---------------------------------------------------------------- parsing

ITEM_RE = re.compile(r"^(\d+)\\?\.\s")
EXTRA_RE = re.compile(r"^##.*Extra")
BOLD_RE = re.compile(r"^\*\*(.+)\*\*\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")


def clean_word(cell: str) -> str:
    w = FOOTNOTE_RE.sub("", cell)
    w = w.replace("**", "").replace("\\#", "")
    w = w.replace("ṁ", "ṃ")
    return w.strip().strip('.,;:!?"“”').strip()


def sentence_of(item_line: str) -> str:
    text = ITEM_RE.sub("", item_line, count=1)
    text = (
        LINK_RE.sub("", text).replace("<br>", " ").replace(" / ", " ").replace("**", "")
    )
    return re.sub(r"\s+", " ", text).strip()


def parse_doc(text: str, course: str, file: str) -> Doc:
    doc = Doc(course, file)
    section = "main"
    item = 0
    sentence = ""
    ncols = 0
    table_line = 0  # 0 = not in table, 1 = header seen, 2+ = body
    skip_table = False
    seen: Counter[tuple[str, int, str]] = Counter()
    translations: dict[tuple[str, int], list[str]] = {}
    sentence_cont = False
    for no, line in enumerate(text.splitlines(), start=1):
        if not line.startswith("|"):
            table_line = 0
            if EXTRA_RE.match(line) and section == "main":
                section, item, sentence = "extra", 0, ""
                sentence_cont = False
                continue
            m = ITEM_RE.match(line)
            if m:
                item = int(m.group(1))
                sentence = sentence_of(line)
                sentence_cont = True
                (doc.main if section == "main" else doc.extra).append(item)
                continue
            if sentence_cont and line[:1] in (" ", "\t"):
                sentence = f"{sentence} {sentence_of(line)}".strip()
                continue
            sentence_cont = False
            b = BOLD_RE.match(line.strip())
            if b and item:
                translations.setdefault((section, item), []).append(b.group(1))
            continue
        table_line += 1
        cells = split_cells(line)
        if table_line == 1:
            ncols = len(cells)
            skip_table = ncols == 2 or (course == "ipc" and ncols == 4)
            continue
        if table_line == 2 or skip_table:
            continue
        if len(cells) != ncols:
            doc.problems.append(
                Finding(
                    course, file, no, "table", f"{len(cells)} cells, expected {ncols}"
                )
            )
            continue
        row = Row(course, file, no, section, item, 0, cells, sentence)
        seen[(section, item, row.word)] += 1
        row.occ = seen[(section, item, row.word)]
        doc.rows.append(row)
    for row in doc.rows:
        row.translation = " ".join(translations.get((row.section, row.item), []))
    return doc


# ---------------------------------------------------------------- cell checks


def pos_problems(cell: str) -> list[str]:
    s = strip_annotations(cell).replace("<br>", " ")
    s = re.sub(r"(?<=\s)/(?=\s)", " ", s)
    tokens = [t for t in re.split(r"\s+or\s+|[,;+.\s]+", s)]
    return [t for t in tokens if t not in POS_WORDS]


def grammar_problems(cell: str) -> list[str]:
    s = strip_annotations(cell)
    s = re.sub(
        r"\+\s*(?:end\s?quote|quotation marks?|nom|acc|instr|dat|abl|gen|loc|voc)\b",
        "",
        s,
    )
    bad: list[str] = []
    for alt in re.split(r"<br>|(?<=\s)/(?=\s)|\s+or\s+|[,;]", s):
        for part in alt.split("+"):
            part = part.strip()
            if part == "or" or part in SIMPLE_GRAMMAR:
                continue
            if INFLECTION.match(part) or VERB.match(part) or STEM.match(part):
                continue
            bad.append(part)
    return bad


def root_problems(cell: str, force: bool = False) -> list[str] | None:
    """Return None if the cell is not a root cell, else a (possibly empty) problem list."""
    s = cell.replace("\\*", "*").strip()
    if not s:
        return None
    applies = force or ROOT_APPLIES.search(s) or (s.startswith("√") and " + " not in s)
    if not applies:
        return None
    return [] if ROOT_FORMAT.match(s) else [s]


def compound_problems(cell: str) -> list[str]:
    words = re.findall(r"[^\W\d_]+", re.sub(r"√\S*", "", cell))
    return [
        w for w in words if COMPOUND_TRIGGER.search(w) and w not in COMPOUND_ALLOWED
    ]


def stray_problems(cell: str, kind: str) -> list[str]:
    bad: list[str] = []
    if re.search(r" {3,}", cell):
        bad.append("3+ consecutive spaces")
    if kind == "pali":
        s = strip_annotations(cell).replace("<br>", " ").replace(" / ", " ")
        letters = {c for c in s if c.isascii() and c.isalpha()} - PALI_ASCII
        if letters:
            bad.append("ASCII letters " + "".join(sorted(letters)))
    return bad


# ---------------------------------------------------------------- doc checks


def check_numbering(key: Doc, ex: Doc) -> list[Finding]:
    found = []
    for name, k, e in (("main", key.main, ex.main), ("extra", key.extra, ex.extra)):
        if k != e:
            found.append(
                Finding(
                    key.course,
                    key.file,
                    1,
                    "numbering",
                    f"{name}: key has {len(k)} items, exercise has {len(e)}; "
                    f"key-only {sorted(set(k) - set(e))}, ex-only {sorted(set(e) - set(k))}"
                    if set(k) != set(e)
                    else f"{name}: key order {k} differs from exercise order {e}",
                )
            )
    return found


def check_numbering_all(course: str) -> list[Finding]:
    found: list[Finding] = []
    for key, ex in load_pairs(course):
        found += key.problems + check_numbering(key, ex)
    return found


def check_pos(rows: list[Row]) -> list[Finding]:
    found = []
    for r in rows:
        for bad in pos_problems(r.cells[1]):
            found.append(
                Finding(
                    r.course,
                    r.file,
                    r.line,
                    "pos",
                    f"'{bad}' in '{r.cells[1]}' ({r.word})",
                )
            )
    return found


def check_grammar(rows: list[Row]) -> list[Finding]:
    found = []
    for r in rows:
        for bad in grammar_problems(r.cells[2]):
            found.append(
                Finding(
                    r.course,
                    r.file,
                    r.line,
                    "grammar",
                    f"'{bad}' in '{r.cells[2]}' ({r.word})",
                )
            )
    return found


def check_root(rows: list[Row]) -> list[Finding]:
    found = []
    for r in rows:
        if len(r.cells) != 5:
            continue
        probs = root_problems(r.cells[4], force=r.course == "bpc")
        if probs:
            found.append(
                Finding(r.course, r.file, r.line, "root", f"'{r.cells[4]}' ({r.word})")
            )
    return found


def check_compound(rows: list[Row]) -> list[Finding]:
    found = []
    for r in rows:
        if r.course != "ipc" or len(r.cells) != 5:
            continue
        for bad in compound_problems(r.cells[4]):
            found.append(
                Finding(
                    r.course,
                    r.file,
                    r.line,
                    "compound",
                    f"'{bad}' in '{r.cells[4]}' ({r.word})",
                )
            )
    return found


def check_stray(rows: list[Row]) -> list[Finding]:
    found = []
    for r in rows:
        for i, cell in enumerate(r.cells):
            for bad in stray_problems(cell, "pali" if i == 0 else ""):
                found.append(
                    Finding(r.course, r.file, r.line, "stray", f"{bad} in '{cell}'")
                )
    return found


def norm_word(w: str) -> str:
    s = w.lower().replace("ṁ", "ṃ")
    s = re.sub(r"[*'‘’\-\\#\[\]()<>.,;:!?\"“”]", "", s)
    s = re.sub(r"[ṃm]$", "", s)
    return s.translate(str.maketrans("āīū", "aiu"))


def check_words(rows: list[Row]) -> list[Finding]:
    """Warnings: row words missing from the sentence and sentence words without a row."""
    found: list[Finding] = []
    items: dict[tuple[str, str, str, int], list[Row]] = {}
    for r in rows:
        if r.item and not r.cells[0].startswith("\\#"):
            items.setdefault((r.course, r.file, r.section, r.item), []).append(r)
    for rs in items.values():
        sentence = rs[0].sentence
        sent_words = [w for w in re.split(r"[\s/]+", sentence) if norm_word(w)]
        sent_join = "".join(norm_word(w) for w in sent_words)
        row_join = "".join(norm_word(r.word) for r in rs)
        for r in rs:
            n = norm_word(r.word)
            if n and n not in sent_join:
                found.append(
                    Finding(
                        r.course,
                        r.file,
                        r.line,
                        "words",
                        f"row '{r.word}' not in sentence",
                        "warning",
                    )
                )
        for w in sent_words:
            n = norm_word(w)
            if n and n not in row_join:
                found.append(
                    Finding(
                        rs[0].course,
                        rs[0].file,
                        rs[0].line,
                        "words",
                        f"sentence word '{w}' has no row",
                        "warning",
                    )
                )
    return found


# ---------------------------------------------------------------- loading


def read_doc(course: str, directory: str, n: int) -> Doc:
    path = ROOT_DIR / directory / f"{n}_class.md"
    return parse_doc(
        path.read_text(encoding="utf-8"), course, f"{directory}/{n}_class.md"
    )


_CACHE: dict[str, list[tuple[Doc, Doc]]] = {}


def load_pairs(course: str) -> list[tuple[Doc, Doc]]:
    if course not in _CACHE:
        key_dir, ex_dir, classes = COURSES[course]
        _CACHE[course] = [
            (read_doc(course, key_dir, n), read_doc(course, ex_dir, n)) for n in classes
        ]
    return _CACHE[course]


def course_rows(course: str) -> list[Row]:
    return [r for key, _ in load_pairs(course) for r in key.rows]


# ---------------------------------------------------------------- 10b: DPD check

DEFAULT_DPD = Path("/Users/deva/Documents/dpd-db/dpd.db")
DEFAULT_REPORT = Path("temp/key_dpd_report.tsv")
REPORT_COLUMNS = [
    "row_key", "course", "file", "line", "section", "item", "occ", "word", "pos",
    "grammar", "root", "gloss", "sentence", "translation", "check", "bucket",
    "dpd_readings",
]  # fmt: skip
ROOT_CELL = re.compile(r"√([^\s･×]+)[･×](\d+)")


def row_key(row: Row) -> str:
    return f"{row.course}/{Path(row.file).name}/{row.section}/{row.item}/{row.word}/{row.occ}"


def report_line(f: DpdFinding[Row]) -> list[str]:
    r = f.row
    root = r.cells[4] if len(r.cells) > 4 else ""
    return [
        row_key(r), r.course, r.file, str(r.line), r.section, str(r.item), str(r.occ),
        r.word, r.cells[1], r.cells[2], root, r.cells[3], r.sentence, r.translation,
        f.check, f.bucket, ";".join(str(x) for x in f.readings),
    ]  # fmt: skip


def sort_key(f: DpdFinding[Row]) -> tuple[str, int, int, int, int, str]:
    r = f.row
    num = int(re.match(r"\d+", Path(r.file).name).group())  # type: ignore[union-attr]
    return (r.course, num, 0 if r.section == "main" else 1, r.item, r.line, f.check)


def write_report(findings: list[DpdFinding[Row]], path: Path) -> None:
    rows = [report_line(f) for f in sorted(findings, key=sort_key)]
    write_tsv(path, REPORT_COLUMNS, rows)


def run_dpd(courses: list[str], db_path: Path, report_path: Path) -> int:
    pr.green_tmr("open DPD database")
    if not db_path.exists():
        pr.no(str(db_path))
        return 1
    db = open_db(db_path, example_matches)
    pr.yes("ok")
    all_findings: list[DpdFinding[Row]] = []
    for course in courses:
        pr.green_tmr(f"{course} DPD check")
        rows = course_rows(course)
        findings, counts = classify_rows(rows, db, "tag")
        all_findings += findings
        pr.yes(f"{len(rows)} rows")
        for bucket in BUCKETS:
            pr.summary(f"  {bucket}", counts[bucket])
    pr.green_tmr("write report")
    write_report(all_findings, report_path)
    pr.yes(str(report_path))
    return 0


# ---------------------------------------------------------------- main


def report(
    course: str, step: str, found: list[Finding], show_all: bool, gating: bool = True
) -> int:
    pr.green_tmr(f"{course} {step}")
    if found and gating:
        pr.no(f"{len(found)}")
    else:
        pr.yes(f"{len(found)}")
    print_all = gating or show_all
    if found and print_all:
        for f in found:
            pr.amber(str(f))
    return len(found) if gating else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course", choices=["bpc", "ipc", "all"], default="all")
    ap.add_argument("--warnings", action="store_true", help="list warning items")
    ap.add_argument(
        "--dpd", nargs="?", const=str(DEFAULT_DPD), default=None, metavar="PATH"
    )
    ap.add_argument("--report", default=str(DEFAULT_REPORT))
    args = ap.parse_args()
    courses = list(COURSES) if args.course == "all" else [args.course]
    errors = 0
    for course in courses:
        rows = course_rows(course)
        errors += report(course, "numbering", check_numbering_all(course), False)
        errors += report(course, "pos vocabulary", check_pos(rows), False)
        errors += report(course, "grammar vocabulary", check_grammar(rows), False)
        errors += report(course, "root format", check_root(rows), False)
        if course == "ipc":
            errors += report(course, "compound spelling", check_compound(rows), False)
        errors += report(course, "stray characters", check_stray(rows), False)
        report(
            course,
            "word coverage (warn)",
            check_words(rows),
            args.warnings,
            gating=False,
        )
    if args.dpd is not None:
        errors += run_dpd(courses, Path(args.dpd), Path(args.report))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
