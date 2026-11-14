"""Verify BPC/IPC answer keys against their exercises and a tag vocabulary (10a), optionally against the DPD database (10b)."""

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from tools.printer import printer as pr

ROOT_DIR = Path(__file__).resolve().parent.parent
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
FOOTNOTE_RE = re.compile(r"\[\^\w+\]")


def split_cells(line: str) -> list[str]:
    s = line.strip()
    s = s[1:] if s.startswith("|") else s
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


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


def strip_annotations(cell: str) -> str:
    s = FOOTNOTE_RE.sub("", cell)
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*\)", "", s)
        s = re.sub(r"\[[^\[\]]*\]", "", s)
    return s


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
GENDERS = {"masc", "fem", "nt", "x", "1st", "2nd", "3rd"}
CASES = {"nom", "acc", "instr", "dat", "abl", "gen", "loc", "voc"}
NUMBERS = {"sg", "pl", "dual"}
PERSONS = {"1st", "2nd", "3rd"}
NONINFLECTING = {"abs", "ger", "inf", "ind"}
SKIP_WORD_CHARS = ("'", "‘", "’", " ", "-", "<br>", "(", "[")
PLUS_CASE = re.compile(
    r"\+\s*(?:end\s?quote|quotation marks?|nom|acc|instr|dat|abl|gen|loc|voc)\b"
)
ROOT_CELL = re.compile(r"√([^\s･×]+)[･×](\d+)")


@dataclass(frozen=True)
class Tag:
    kind: str  # infl | verb | simple
    genders: frozenset[str] = frozenset()
    cases: frozenset[str] = frozenset()
    persons: frozenset[str] = frozenset()
    numbers: frozenset[str] = frozenset()
    tense: str = ""
    reflx: bool = False


@dataclass(frozen=True)
class Reading:
    lemma: str
    pos: str
    grammar: str

    def __str__(self) -> str:
        return " ".join(x for x in (self.lemma, self.pos, self.grammar) if x)


@dataclass
class DpdFinding:
    row: Row
    check: str
    bucket: str
    readings: list[Reading] = field(default_factory=list)


def slot(text: str) -> frozenset[str]:
    return frozenset(t for t in text.split("/") if t)


def parse_key_tag(cell: str) -> Tag | None:
    """Parse a single key Grammar tag; None if the cell is not one checkable tag."""
    s = PLUS_CASE.sub("", strip_annotations(cell)).strip()
    if not s or re.search(r"<br>|\s+or\s+|[,;+\s]", s):
        return None
    if s in ("abs", "ger", "inf"):
        return Tag("simple", tense=s)
    s = re.sub(r"^(?:" + "|".join(sorted(POS_WORDS - {"", "-"})) + r")\.", "", s)
    s = s.replace("./", "/")
    if VERB.match(s):
        toks = s.split(".")
        mods = {t for t in toks if t in ("caus", "pass", "reflx")}
        rest = [t for t in toks if t not in ("caus", "pass", "reflx")]
        return Tag(
            "verb",
            persons=slot(rest[1]),
            numbers=slot(rest[2]),
            tense=rest[0],
            reflx="reflx" in mods,
        )
    if INFLECTION.match(s):
        toks = s.split(".")
        genders = slot(toks[0]) if len(toks) == 3 else frozenset()
        return Tag(
            "infl", genders=genders, cases=slot(toks[-2]), numbers=slot(toks[-1])
        )
    return None


def reading_matches(tag: Tag, r: Reading) -> bool:
    if tag.kind == "simple":
        if tag.tense == "inf":
            return r.pos == "inf"
        return r.pos in ("abs", "ger")
    toks = r.grammar.split()
    if not toks:
        return False
    is_verb = any(t in TENSES for t in toks)
    if tag.kind == "verb":
        if not is_verb:
            return False
        tense = next(t for t in toks if t in TENSES)
        person = next((t for t in toks if t in PERSONS), "")
        number = next((t for t in toks if t in NUMBERS), "")
        return (
            tense == tag.tense
            and ("reflx" in toks) == tag.reflx
            and person in tag.persons
            and number in tag.numbers
        )
    if is_verb:
        return False
    number = (
        "dual" if "dual" in toks else next((t for t in toks if t in ("sg", "pl")), "")
    )
    case = next((t for t in toks if t in CASES), "")
    gender = next((t for t in toks if t in GENDERS), "")
    if case not in tag.cases or number not in tag.numbers:
        return False
    if tag.genders and gender and "x" not in tag.genders and gender != "x":
        return gender in tag.genders
    return True


def eligible_word(word: str) -> bool:
    return bool(word) and not any(c in word for c in SKIP_WORD_CHARS)


def key_pos_tokens(cell: str) -> set[str]:
    s = strip_annotations(cell).replace("<br>", " ")
    s = re.sub(r"(?<=\s)/(?=\s)", " ", s)
    return {t for t in re.split(r"\s+or\s+|[,;+.\s]+", s) if t}


def pos_agrees(key_pos: set[str], dpd_pos: str) -> bool:
    return dpd_pos in key_pos or (
        dpd_pos in ("abs", "ger", "inf") and "verb" in key_pos
    )


class DpdDb:
    """Read-only access to the DPD tables used by the 10b check."""

    def __init__(self, con: sqlite3.Connection) -> None:
        self.con = con
        self._forms: dict[str, list[Reading] | None] = {}
        self._form_roots: dict[str, set[str]] = {}
        self._hw: dict[int, tuple[str, str, str]] = {}
        self.root_groups: dict[str, set[int]] = {}
        for root, group in con.execute("select root, root_group from dpd_roots"):
            self.root_groups.setdefault(bare_root(root), set()).add(int(group))

    def _headword(self, hid: int) -> tuple[str, str, str]:
        if hid not in self._hw:
            row = self.con.execute(
                "select lemma_1, pos, root_key from dpd_headwords where id=?", (hid,)
            ).fetchone()
            self._hw[hid] = tuple(row) if row else ("", "", "")  # type: ignore[assignment]
        return self._hw[hid]

    def lookup(self, word: str) -> list[Reading] | None:
        """Readings for a form (None if absent); also caches the form's root keys."""
        for form in dict.fromkeys(
            [
                word,
                word.lower(),
                re.sub(r"m$", "ṃ", word),
                re.sub(r"m$", "ṃ", word.lower()),
            ]
        ):
            if form in self._forms:
                found = self._forms[form]
            else:
                row = self.con.execute(
                    "select headwords, grammar from lookup where lookup_key=?", (form,)
                ).fetchone()
                found = None
                if row:
                    found = []
                    roots: set[str] = set()
                    for lemma, pos, gram in json.loads(row[1] or "[]"):
                        found.append(Reading(lemma, pos, gram))
                    for hid in json.loads(row[0] or "[]"):
                        lemma, pos, root_key = self._headword(hid)
                        if pos in NONINFLECTING:
                            found.append(Reading(lemma, pos, ""))
                        if root_key:
                            roots.add(bare_root(root_key))
                    self._form_roots[form] = roots
                self._forms[form] = found
            if found is not None:
                self._last_form = form
                return found
        return None

    def form_roots(self, word: str) -> set[str]:
        self.lookup(word)
        return self._form_roots.get(getattr(self, "_last_form", ""), set())


def bare_root(root: str) -> str:
    return re.sub(r"\s+\d+$", "", root.strip())


def classify_row(row: Row, db: DpdDb) -> list[DpdFinding]:
    """Return non-CONFIRMED, non-SKIPPED findings for one key row."""
    out: list[DpdFinding] = []
    word = row.word
    ok_word = eligible_word(word)
    readings: list[Reading] | None = None
    if ok_word:
        readings = db.lookup(word)
        tag = parse_key_tag(row.cells[2]) if len(row.cells) > 2 else None
        if tag is not None:
            if readings is None:
                out.append(DpdFinding(row, "form", "NOT-FOUND"))
            else:
                matching = [r for r in readings if reading_matches(tag, r)]
                if not matching:
                    out.append(DpdFinding(row, "form", "IMPOSSIBLE", readings))
                else:
                    kp = key_pos_tokens(row.cells[1])
                    cand = {r for r in readings if pos_agrees(kp, r.pos)} or set(
                        readings
                    )
                    if len(cand) > 1:
                        out.append(
                            DpdFinding(row, "form", "AMBIGUOUS", sorted(cand, key=str))
                        )
    if len(row.cells) == 5:
        m = ROOT_CELL.search(row.cells[4].replace("\\*", "*"))
        if m:
            root, group = "√" + m.group(1), int(m.group(2))
            groups = db.root_groups.get(root)
            bad = groups is None or group not in groups
            if not bad and ok_word and readings is not None:
                roots = db.form_roots(word)
                bad = bool(roots) and root not in roots
            if bad:
                out.append(DpdFinding(row, "root", "ROOT-MISMATCH", readings or []))
    return out


def status_of(row: Row) -> str:
    """SKIPPED / CHECKED classification for the console summary counts."""
    if not eligible_word(row.word):
        return "SKIPPED"
    tag = parse_key_tag(row.cells[2]) if len(row.cells) > 2 else None
    return "SKIPPED" if tag is None else "CHECKED"


def row_key(row: Row) -> str:
    return f"{row.course}/{Path(row.file).name}/{row.section}/{row.item}/{row.word}/{row.occ}"


def report_line(f: DpdFinding) -> list[str]:
    r = f.row
    root = r.cells[4] if len(r.cells) > 4 else ""
    vals = [
        row_key(r), r.course, r.file, str(r.line), r.section, str(r.item), str(r.occ),
        r.word, r.cells[1], r.cells[2], root, r.cells[3], r.sentence, r.translation,
        f.check, f.bucket, ";".join(str(x) for x in f.readings),
    ]  # fmt: skip
    return [re.sub(r"[\t\r\n]+", " ", v) for v in vals]


def sort_key(f: DpdFinding) -> tuple[str, int, int, int, int, str]:
    r = f.row
    num = int(re.match(r"\d+", Path(r.file).name).group())  # type: ignore[union-attr]
    return (r.course, num, 0 if r.section == "main" else 1, r.item, r.line, f.check)


def write_report(findings: list[DpdFinding], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(REPORT_COLUMNS)]
    lines += ["\t".join(report_line(f)) for f in sorted(findings, key=sort_key)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_db(path: Path) -> DpdDb:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    return DpdDb(con)


def run_dpd(courses: list[str], db_path: Path, report_path: Path) -> int:
    pr.green_tmr("open DPD database")
    if not db_path.exists():
        pr.no(str(db_path))
        return 1
    db = open_db(db_path)
    pr.yes("ok")
    all_findings: list[DpdFinding] = []
    for course in courses:
        pr.green_tmr(f"{course} DPD check")
        rows = course_rows(course)
        counts: Counter[str] = Counter()
        for row in rows:
            fs = classify_row(row, db)
            all_findings += fs
            for f in fs:
                counts[f.bucket] += 1
            if not fs:
                st = status_of(row)
                counts["SKIPPED" if st == "SKIPPED" else "CONFIRMED"] += 1
        pr.yes(f"{len(rows)} rows")
        for bucket in (
            "IMPOSSIBLE",
            "AMBIGUOUS",
            "NOT-FOUND",
            "ROOT-MISMATCH",
            "CONFIRMED",
            "SKIPPED",
        ):
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
