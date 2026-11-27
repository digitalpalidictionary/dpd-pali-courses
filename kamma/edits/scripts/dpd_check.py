"""Shared DPD check for the course and study-tools key verifiers (tag parsing, DPD readings, buckets); edit it here, it is linked into study-tools."""

import json
import re
import sqlite3
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

# ---------------------------------------------------------------- vocabulary

TENSES = ("pr", "aor", "fut", "opt", "imp", "imperf", "perf", "cond")
GENDERS = {"masc", "fem", "nt", "x", "1st", "2nd", "3rd", "1", "2", "3"}
CASES = {"nom", "acc", "instr", "ins", "dat", "abl", "gen", "loc", "voc"}
NUMBERS = {"sg", "pl", "dual"}
PERSONS = {"1st", "2nd", "3rd", "1", "2", "3"}
MODIFIERS = {"caus", "pass", "refl", "reflx", "reflex"}
POS_WORDS = {
    "noun", "ind", "verb", "pron", "adj", "pp", "prp", "ptp", "app", "card",
    "ordin", "ord", "idiom", "sandhi", "prefix", "suffix", "consonant", "proper",
    "caus", "pass", "interr", "comp", "comparative", "compar", "as", "agent", "-",
    "", "adv", "conj", "neg", "emph", "emphat", "fpp", "abbrev", "inf", "ger",
    "abs", "refl", "reflx", "reflex", "vb", "abstr",
}  # fmt: skip
SIMPLE_GRAMMAR = {
    "adv", "conj", "neg", "emph", "emphat", "abs", "ger", "inf", "interr", "prep",
    "quote", "quotation mark", "question marker", "excl", "cond", "disj",
    "impers", "ind", "idiom", "prohib", "gen abs", "loc abs", "-", "", "sandhi",
    "abs/ger", "ger/abs", "abs.caus", "ger.caus",
} | POS_WORDS | set(TENSES)  # fmt: skip
# Tokens that make a pat/tsv grammar cell a grammar shape rather than a bare lemma.
DPD_TAG_TOKENS = (
    SIMPLE_GRAMMAR | GENDERS | CASES | NUMBERS | PERSONS | MODIFIERS
    | {"sandhi", "comp", "comps", "in", "of", "from", "or", "person", "act",
       "taddhita", "onom", "impersonal"}
)  # fmt: skip
# DPD reads `instr` and `1st/2nd/3rd`, while the tag tables also use `ins` and digits.
NORM = {"ins": "instr", "1": "1st", "2": "2nd", "3": "3rd"}
NONINFLECTING = {"abs", "ger", "inf", "ind"}
FOOTNOTE_RE = re.compile(r"\[\^\w+\]")
PLUS_CASE = re.compile(
    r"\+\s*(?:end\s?quote|quotation marks?|nom|acc|instr|ins|dat|abl|gen|loc|voc)\b"
)

_G = "(?:" + "|".join(sorted(GENDERS)) + ")"
_C = "(?:" + "|".join(sorted(CASES)) + ")"
_N = "(?:" + "|".join(sorted(NUMBERS)) + ")"
_P = "(?:" + "|".join(sorted(PERSONS)) + ")"
_T = "(?:" + "|".join(TENSES) + ")"
_M = "(?:" + "|".join(sorted(MODIFIERS)) + ")"
_POS = "(?:" + "|".join(sorted(w for w in POS_WORDS if w.isalpha())) + ")"
INFLECTION = re.compile(
    rf"^(?:{_POS}\.)?(?:{_G}(?:\.?/{_G})*\.)?{_C}(?:/{_C})*\.{_N}(?:/{_N})*\??$"
)
VERB = re.compile(rf"^(?:{_M}\.)*{_T}\.(?:{_M}\.)*{_P}(?:/{_P})*\.{_N}(?:/{_N})*\??$")

SKIP_WORD_CHARS = ("'", "‘", "’", " ", "-", "<br>", "(", "[")
NOUN_POS = {"masc", "nt", "fem"}
VERB_POS = {"pr", "aor", "fut", "imp", "opt", "perf", "cond", "imperf", "cs"}
HOMONYM_RE = re.compile(r" \d+(?:\.\d+)?$")

# Console order of the buckets.
BUCKETS = (
    "IMPOSSIBLE",
    "AMBIGUOUS",
    "NOT-FOUND",
    "ROOT-MISMATCH",
    "EXAMPLE-CONFLICT",
    "CONFIRMED",
    "SKIPPED",
)

# ---------------------------------------------------------------- cells


def strip_annotations(cell: str, braces: bool = True) -> str:
    """Drop footnotes and (…)/[…] notes, and {…} unless braces=False (the courses' gate keeps braces so they are flagged)."""
    s = FOOTNOTE_RE.sub("", cell)
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*\)", "", s)
        s = re.sub(r"\[[^\[\]]*\]", "", s)
        if braces:
            s = re.sub(r"\{[^{}]*\}", "", s)
    return s


def split_cells(line: str) -> list[str]:
    s = line.strip()
    s = s[1:] if s.startswith("|") else s
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def key_pos_tokens(cell: str) -> set[str]:
    """The POS words of a key/table POS cell (annotations dropped, `or`, `/`, `.`, `+`, `>` split)."""
    s = strip_annotations(cell).replace("<br>", " ")
    s = re.sub(r"(?<=\s)/(?=\s)", " ", s)
    return {t for t in re.split(r"\s+or\s+|[,;:+./\\>\s]+", s) if t}


def eligible_word(word: str) -> bool:
    return bool(word) and not any(c in word for c in SKIP_WORD_CHARS)


def bare_root(root: str) -> str:
    return re.sub(r"\s+\d+$", "", root.strip())


def headword_key_pos(pos: str) -> str:
    """DPD headword pos (masc/pr/...) as the key's POS word (noun/verb/...)."""
    return "noun" if pos in NOUN_POS else "verb" if pos in VERB_POS else pos


# ---------------------------------------------------------------- tags and readings


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


def slot(text: str) -> frozenset[str]:
    return frozenset(NORM.get(t, t) for t in text.split("/") if t)


def norm_token(token: str) -> str:
    return NORM.get(token, token)


def parse_tag(cell: str, dialect: str) -> Tag | None:
    """Parse one checkable grammar cell; dialect "tag" (dotted tags) or "dpd" (`masc nom sg of ...`); None when the cell is an alternative or free text."""
    if dialect == "dpd":
        s = re.sub(r"^in comps?,?\s*", "", strip_annotations(cell)).strip()
        s = re.sub(r"\b(?:of|from)\s+.*$", "", s).strip()
        s = re.sub(r",\s*(?:comp|comps|verb|vb|neg|agent|abstr)\s*$", "", s)
        s = s.strip().strip(",;")
        if not s or re.search(r"[,;+]|\bsandhi\b|\s+or\s+", s):
            return None
        tokens = [t for t in s.split() if t in DPD_TAG_TOKENS]
        if not tokens:
            return None
        gender = norm_token(next((t for t in tokens if t in GENDERS), ""))
        case = norm_token(next((t for t in tokens if t in CASES), ""))
        number = next((t for t in tokens if t in NUMBERS), "")
        tense = next((t for t in tokens if t in TENSES), "")
        person = norm_token(next((t for t in tokens if t in PERSONS), ""))
        if tense and person and number:
            return Tag(
                "verb",
                persons=frozenset({person}) if person else frozenset(),
                numbers=frozenset({number}),
                tense=tense,
            )
        if case and number:
            genders = frozenset({gender}) if gender else frozenset()
            return Tag(
                "infl", genders=genders, cases=frozenset({case}),
                numbers=frozenset({number}),
            )  # fmt: skip
        simple = next(
            (t for t in tokens if t in ("abs", "ger", "inf", "pp", "prp", "ptp")),
            "",
        )
        return Tag("simple", tense=simple) if simple else None

    s = PLUS_CASE.sub("", strip_annotations(cell)).strip()
    if not s or re.search(r"<br>|\s+or\s+|[,;+\s]", s):
        return None
    if s in ("abs", "ger", "inf"):
        return Tag("simple", tense=s)
    # A leading reflexive marker is a verb modifier, not a POS word: keep it for VERB.
    pos_prefix = sorted(POS_WORDS - {"", "-", "refl", "reflx", "reflex"})
    s = re.sub(r"^(?:" + "|".join(pos_prefix) + r")\.", "", s)
    s = s.replace("./", "/")
    if VERB.match(s):
        toks = s.split(".")
        mods = {t for t in toks if t in MODIFIERS}
        rest = [t for t in toks if t not in MODIFIERS]
        return Tag(
            "verb",
            persons=slot(rest[1]),
            numbers=slot(rest[2]),
            tense=rest[0],
            reflx=bool(mods & {"refl", "reflx", "reflex"}),
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
        if tag.tense in ("pp", "prp", "ptp"):
            return r.pos == tag.tense
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


def pos_agrees(key_pos: set[str], dpd_pos: str) -> bool:
    return dpd_pos in key_pos or (
        dpd_pos in ("abs", "ger", "inf") and "verb" in key_pos
    )


# ---------------------------------------------------------------- DPD database


class DpdDb:
    """Read-only access to the DPD tables used by the DPD check; `matches` is the example matcher (sbs_sync.example_matches)."""

    def __init__(
        self, con: sqlite3.Connection, matches: Callable[[str, str], bool]
    ) -> None:
        self.con = con
        self.matches = matches
        self._forms: dict[str, list[Reading] | None] = {}
        self._form_roots: dict[str, set[str]] = {}
        self._hw: dict[int, tuple[str, str, str]] = {}
        self._form_ids: dict[str, list[int]] = {}
        self._examples: dict[int, tuple[str, str]] = {}
        self._last_form = ""
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
        self._last_form = ""
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
                    self._form_ids[form] = json.loads(row[0] or "[]")
                    for hid in self._form_ids[form]:
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

    def example_headwords(
        self, word: str, sentence: str, extra_ids: Iterable[int] = ()
    ) -> list[tuple[str, str]]:
        """(lemma_1, pos) of the form's headwords, then of extra_ids, whose example_1/example_2 quotes `sentence`."""
        if self.lookup(word) is None:
            return []
        ids = list(self._form_ids.get(self._last_form, []))
        ids += [i for i in extra_ids if i not in ids]
        out: list[tuple[str, str]] = []
        for hid in ids:
            if hid not in self._examples:
                row = self.con.execute(
                    "select example_1, example_2 from dpd_headwords where id=?", (hid,)
                ).fetchone()
                self._examples[hid] = (row[0] or "", row[1] or "") if row else ("", "")
            if any(e and self.matches(e, sentence) for e in self._examples[hid]):
                lemma, pos, _root = self._headword(hid)
                if (lemma, pos) not in out:
                    out.append((lemma, pos))
        return out

    def form_roots(self, word: str) -> set[str]:
        self.lookup(word)
        return self._form_roots.get(self._last_form, set())


def open_db(path: Path, matches: Callable[[str, str], bool]) -> DpdDb:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    return DpdDb(con, matches)


# ---------------------------------------------------------------- classification


class DpdRow(Protocol):
    """What the DPD check reads from a table row; both verifiers' Row classes provide it."""

    @property
    def word(self) -> str: ...
    @property
    def pos(self) -> str: ...
    @property
    def grammar(self) -> str: ...
    @property
    def sentence(self) -> str: ...
    @property
    def headword_ids(self) -> tuple[int, ...]: ...
    @property
    def dpd_root(self) -> tuple[str, str] | None: ...


@dataclass
class DpdFinding[R: DpdRow]:
    row: R
    check: str
    bucket: str
    readings: list[Reading] = field(default_factory=list)
    roots: list[str] = field(default_factory=list)


def example_conflict(
    row: DpdRow,
    readings: list[Reading],
    example_hws: list[tuple[str, str]],
    dialect: str,
) -> list[Reading] | None:
    """The example headwords' readings if the row agrees with none of them, else None."""
    kp = key_pos_tokens(row.pos)
    tag = parse_tag(row.grammar, dialect)
    preferred: list[Reading] = []
    for lemma, pos in example_hws:
        base = HOMONYM_RE.sub("", lemma)
        grams = [r for r in readings if r.lemma == base and r.grammar]
        agrees = pos_agrees(kp, headword_key_pos(pos)) and (
            tag is None or not grams or any(reading_matches(tag, r) for r in grams)
        )
        if agrees:
            return None
        for r in grams or [Reading(lemma, pos, "")]:
            if r not in preferred:
                preferred.append(r)
    return preferred


def classify_row[R: DpdRow](row: R, db: DpdDb, dialect: str) -> list[DpdFinding[R]]:
    """Return non-CONFIRMED, non-SKIPPED findings for one row, in the order form, example, root.

    A form that DPD has no reading for (absent, or a lookup row with no readings) is NOT-FOUND.
    """
    out: list[DpdFinding[R]] = []
    word = row.word
    ok_word = eligible_word(word)
    readings: list[Reading] | None = None
    if ok_word:
        readings = db.lookup(word)
        tag = parse_tag(row.grammar, dialect)
        if tag is not None:
            if not readings:
                out.append(DpdFinding(row, "form", "NOT-FOUND"))
            else:
                matching = [r for r in readings if reading_matches(tag, r)]
                if not matching:
                    out.append(DpdFinding(row, "form", "IMPOSSIBLE", readings))
                else:
                    kp = key_pos_tokens(row.pos)
                    cand = {r for r in readings if pos_agrees(kp, r.pos)} or set(
                        readings
                    )
                    if len(cand) > 1:
                        out.append(
                            DpdFinding(row, "form", "AMBIGUOUS", sorted(cand, key=str))
                        )
    if ok_word and row.sentence and readings is not None:
        example_hws = db.example_headwords(word, row.sentence, row.headword_ids)
        if example_hws:
            preferred = example_conflict(row, readings, example_hws, dialect)
            if preferred is not None:
                out.append(DpdFinding(row, "example", "EXAMPLE-CONFLICT", preferred))
    root_cell = row.dpd_root
    if root_cell is not None:
        name, group = root_cell
        groups = db.root_groups.get(name)
        bad = groups is None
        if groups is not None and group:
            bad = not group.isdigit() or int(group) not in groups
        if not bad and ok_word and readings is not None:
            roots = db.form_roots(word)
            bad = bool(roots) and name not in roots
        if bad:
            expected = sorted(db.form_roots(word)) if ok_word else []
            out.append(
                DpdFinding(row, "root", "ROOT-MISMATCH", readings or [], expected)
            )
    return out


def status_of(row: DpdRow, dialect: str) -> str:
    """SKIPPED / CHECKED classification for the console summary counts."""
    if not eligible_word(row.word):
        return "SKIPPED"
    return "SKIPPED" if parse_tag(row.grammar, dialect) is None else "CHECKED"


def classify_rows[R: DpdRow](
    rows: Sequence[R], db: DpdDb, dialect: str
) -> tuple[list[DpdFinding[R]], Counter[str]]:
    """Classify every row; the counter holds one count per bucket (rows without findings count as CONFIRMED or SKIPPED)."""
    findings: list[DpdFinding[R]] = []
    counts: Counter[str] = Counter()
    for row in rows:
        fs = classify_row(row, db, dialect)
        findings += fs
        for f in fs:
            counts[f.bucket] += 1
        if not fs:
            st = status_of(row, dialect)
            counts["SKIPPED" if st == "SKIPPED" else "CONFIRMED"] += 1
    return findings, counts


# ---------------------------------------------------------------- report file


def write_tsv(path: Path, columns: list[str], rows: Iterable[list[str]]) -> None:
    """Write a TSV: header, then one line per row; tabs and newlines inside a value become a space."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(columns)]
    lines += ["\t".join(re.sub(r"[\t\r\n]+", " ", v) for v in r) for r in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
