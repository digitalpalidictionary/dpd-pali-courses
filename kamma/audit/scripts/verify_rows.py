"""Check that every backtick excerpt in the `Current` cell of audit rows exists in the cited source file within 2 lines of the cited line.

Usage, from the root of the project being audited:
    uv run python kamma/audit/scripts/verify_rows.py <source root> <audit file> [<audit file> …]

<source root> is the folder the Location paths are relative to (e.g. docs/ipc_key, or . for repo-relative paths).
Audit files are slice files (6 columns, Cat first) or a final file (5 columns).
"""

import re
import sys
from pathlib import Path

FILE_RE = re.compile(r"(?:[\w\-.]+/)*[\w\-.]+\.(?:md|tsv|csv|txt)")
NEAR = 2


def norm(s: str) -> str:
    s = s.replace("¦", "|").replace("\\|", "|")
    s = re.sub(r"\s*\|\s*", "|", s)
    return re.sub(r"\s+", " ", s).strip()


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def lines_of(spec: str) -> list[int]:
    out: list[int] = []
    for part in re.findall(r"\d+(?:[–\-]\d+)?", spec):
        a, _, b = (
            re.split(r"([–\-])", part)
            if re.search(r"[–\-]", part)
            else (part, "", part)
        )
        out.extend(range(int(a), int(b) + 1))
    return out


def resolve(root: Path, name: str, last_dir: str) -> Path | None:
    """A bare file name after a `dir/file` in the same cell is looked up in that dir too."""
    for cand in (root / name, root / last_dir / name):
        if cand.is_file():
            return cand
    return None


def check(root: Path, src: Path) -> tuple[int, int, int]:
    ok = bad = unresolved = 0
    for n, line in enumerate(src.read_text().splitlines(), 1):
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        c = cells(line)
        if len(c) == 6:
            loc, cur = c[1], c[2]
        elif len(c) == 5:
            loc, cur = c[0], c[1]
        else:
            continue
        if loc in ("Location", "Cat"):
            continue
        targets: list[Path] = []
        last_dir = ""
        for m in FILE_RE.finditer(loc):
            name = m.group()
            p = resolve(root, name, last_dir)
            if "/" in name:
                last_dir = name.rsplit("/", 1)[0]
            if p:
                targets.append(p)
        if not targets:
            unresolved += 1
            continue
        # every number in the cell that is not part of a file name counts as a cited line
        nums = lines_of(FILE_RE.sub("", loc))
        for snip in re.findall(r"`([^`]+)`", cur):
            for frag in re.split(r"…|\.\.\.", snip):
                f = norm(frag)
                if len(f) < 3:
                    continue
                hit = near = False
                for p in targets:
                    for i, t in enumerate(p.read_text().splitlines(), 1):
                        if f in norm(t):
                            hit = True
                            if not nums or any(abs(i - k) <= NEAR for k in nums):
                                near = True
                if hit and near:
                    ok += 1
                else:
                    bad += 1
                    state = "WRONG LINE" if hit else "NOT FOUND"
                    print(f"{src.name}:{n} {state} [{loc[:60]}] «{frag.strip()}»")
    return ok, bad, unresolved


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    source_root = Path(sys.argv[1])
    if not source_root.is_dir():
        raise SystemExit(f"not a folder: {source_root}")
    tot_ok = tot_bad = tot_unres = 0
    for name in sys.argv[2:]:
        o, b, u = check(source_root, Path(name))
        tot_ok += o
        tot_bad += b
        tot_unres += u
    print(f"OK {tot_ok}  FAIL {tot_bad}  (rows with no source file found: {tot_unres})")
    sys.exit(1 if tot_bad else 0)
