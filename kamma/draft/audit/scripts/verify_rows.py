"""Check that every backtick excerpt in the IPC audit rows exists in the cited docs/ipc file near the cited line."""

import re
import sys
from pathlib import Path

ROOT = Path("/Users/deva/Documents/dpd-pali-courses")
IPC = ROOT / "docs/ipc"
SCRATCH = ROOT / "kamma/draft/audit/scratch"

FILE_RE = re.compile(r"((?:class_\d+/)?[0-9a-z_]+\.md)((?::[\d–\-, ]+)?)")


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


def check(src: Path) -> tuple[int, int]:
    ok = bad = 0
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
        targets: list[tuple[Path, list[int]]] = []
        last_dir = ""
        for m in FILE_RE.finditer(loc):
            name = m.group(1)
            if "/" in name:
                last_dir = name.split("/")[0]
            elif name != "index.md" and last_dir:
                name = f"{last_dir}/{name}"
            p = IPC / name
            if p.exists():
                targets.append((p, lines_of(m.group(2))))
        if not targets:
            continue
        allnums = lines_of(
            re.sub(r"(?:class_\d+/)?[0-9a-z_]+\.md|class(?:es)? [\d–\-]+", "", loc)
        )
        targets = [(p, allnums) for p, _ in targets]
        for snip in re.findall(r"`([^`]+)`", cur):
            for frag in re.split(r"…|\.\.\.", snip):
                f = norm(frag)
                if len(f) < 3:
                    continue
                hit = near = False
                for p, nums in targets:
                    text = p.read_text().splitlines()
                    for i, t in enumerate(text, 1):
                        if f in norm(t):
                            hit = True
                            if not nums or any(abs(i - k) <= 2 for k in nums):
                                near = True
                if hit and near:
                    ok += 1
                else:
                    bad += 1
                    state = "WRONG LINE" if hit else "NOT FOUND"
                    print(f"{src.name}:{n} {state} [{loc[:60]}] «{frag.strip()}»")
    return ok, bad


if __name__ == "__main__":
    tot_ok = tot_bad = 0
    for f in sorted(
        SCRATCH.glob(sys.argv[1] if len(sys.argv) > 1 else "ipc-audit*.md")
    ):
        if "handoff" in f.name:
            continue
        o, b = check(f)
        tot_ok += o
        tot_bad += b
    print(f"OK {tot_ok}  FAIL {tot_bad}")
