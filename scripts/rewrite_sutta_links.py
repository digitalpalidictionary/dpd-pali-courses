"""Rewrite dead find.dhamma.gift/bw sutta links in docs/ to their s.dhamma.gift equivalents."""

import argparse
import re
import sys
from pathlib import Path

from tools.printer import printer as pr

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
OLD_BASE = "https://find.dhamma.gift/bw/"
NEW_BASE = "https://s.dhamma.gift"
VIN = "/vin/tv/pli-tv"

LINK_RE = re.compile(r"\[([^\]]*)\]\((https://find\.dhamma\.gift/bw/[^)\s]*)\)")

# Pātimokkha section ids on /vin/tv/pli-tv-bu-pm/ (pm5 = Aniyata)
PM_SECTIONS = {"pr": 3, "sg": 4, "np": 6, "pc": 7, "pd": 8, "sk": 9}
# Vinaya rule books: old code -> new code (old "sn" is new "ss")
VB_BOOKS = {"pj": "pj", "sn": "ss", "np": "np", "pc": "pc"}

# (pattern on the part after /bw/, template for the part after s.dhamma.gift)
SIMPLE_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"mn/mn(\d+)\.html"), r"/mn/mn\1/index.html"),
    (re.compile(r"dn/dn(\d+)\.html"), r"/dn/dn\1/index.html"),
    (re.compile(r"sn/sn(\d+)\.(\d+)\.html"), r"/sn/sn\1/index.html#sn\1.\2"),
    (re.compile(r"an/an(\d+)\.(\d+)\.html"), r"/an/an\1/index.html#an\1.\2"),
    (re.compile(r"snp/snp(\d+)\.(\d+)\.html"), r"/kn/snp/index.html#snp\1.\2"),
    (re.compile(r"ud/ud(\d+)\.(\d+)\.html"), r"/kn/ud/index.html#ud\1.\2"),
    (re.compile(r"kp/kp(\d+)\.html"), r"/kn/kp/index.html#kp\1"),
    (re.compile(r"dhp/dhp(\d+)-\d+\.html"), r"/kn/dhp/index.html#dhp\1"),
    (re.compile(r"it/it\.html"), "/kn/iti/index.html"),
    (re.compile(r"tha/tha(\d+)\.html"), r"/kn/thag/index.html#thag\1.1"),
    (re.compile(r"thi/thi(\d+)\.html"), r"/kn/thig/index.html#thig\1.1"),
    # old mislink: labelled "VIN PAT AN 1" (Aniyata 1) but pointed at AN book 1
    (re.compile(r"an/an1\.html"), f"{VIN}-bu-pm/index.html#pli-tv-bu-pm5"),
    # Aniyata rules: the new page has no plain per-rule id, so page only
    (re.compile(r"vi/bu-vb-an\d+\.html"), f"{VIN}-bu-vb-as/index.html"),
]
VB_RE = re.compile(r"vi/bu-vb-(pj|sn|np|pc)(\d+)\.html")
PM_RE = re.compile(r"vi/bu-pt\.html#(pr|sg|np|pc|pd|sk)")
KD_RE = re.compile(r"vi/kd\.html")
KD_TEXT_RE = re.compile(r"VIN([45])\.(\d+)\b")


def map_url(old: str, text: str = "") -> str | None:
    """Return the s.dhamma.gift URL for an old find.dhamma.gift URL, or None if unmapped."""
    if not old.startswith(OLD_BASE):
        return None
    rest = old[len(OLD_BASE) :]
    for pattern, template in SIMPLE_RULES:
        if pattern.fullmatch(rest):
            return NEW_BASE + pattern.sub(template, rest)
    if m := VB_RE.fullmatch(rest):
        book = VB_BOOKS[m.group(1)]
        return (
            f"{NEW_BASE}{VIN}-bu-vb-{book}/index.html#pli-tv-bu-vb-{book}{m.group(2)}"
        )
    if m := PM_RE.fullmatch(rest):
        return f"{NEW_BASE}{VIN}-bu-pm/index.html#pli-tv-bu-pm{PM_SECTIONS[m.group(1)]}"
    if KD_RE.fullmatch(rest) and (m := KD_TEXT_RE.search(text)):
        chapter = int(m.group(2)) + (10 if m.group(1) == "5" else 0)
        return f"{NEW_BASE}{VIN}-kd{chapter}/index.html"
    return None


def rewrite_text(src: str) -> tuple[str, int, list[str]]:
    """Rewrite all old links in src; return (new text, replaced count, unmapped old URLs)."""
    count = 0
    unmapped: list[str] = []

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        new = map_url(m.group(2), m.group(1))
        if new is None:
            unmapped.append(m.group(2))
            return m.group(0)
        count += 1
        return f"[{m.group(1)}]({new})"

    return LINK_RE.sub(repl, src), count, unmapped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write", action="store_true", help="apply changes (default: dry run)"
    )
    args = parser.parse_args()

    pr.green_tmr("rewriting sutta links" + ("" if args.write else " (dry run)"))
    total = 0
    files = 0
    unmapped: list[tuple[Path, str]] = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        src = path.read_text(encoding="utf-8")
        if "find.dhamma.gift" not in src:
            continue
        out, count, bad = rewrite_text(src)
        unmapped.extend((path, u) for u in bad)
        total += count
        if count and args.write:
            path.write_text(out, encoding="utf-8")
            files += 1
    leftover = sum(
        p.read_text(encoding="utf-8").count("find.dhamma.gift")
        for p in DOCS_DIR.rglob("*.md")
    )
    if unmapped or (args.write and leftover):
        pr.no(f"{len(unmapped)} unmapped")
        for path, url in unmapped:
            pr.amber(f"{path.relative_to(ROOT_DIR)}: {url}")
        if args.write and leftover:
            pr.amber(f"{leftover} find.dhamma.gift strings remain")
        return 1
    pr.yes(total)
    pr.summary("files written", files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
