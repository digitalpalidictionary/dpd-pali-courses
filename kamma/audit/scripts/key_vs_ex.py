"""Read-only comparison of the numbered sentences in a key folder against the same-named files in an exercise folder, for an audit.

Usage, from the root of the project being audited:
    uv run python kamma/audit/scripts/key_vs_ex.py <key folder> <exercise folder> [--glob "*_class.md"]
"""

import argparse
import re
from collections import Counter
from pathlib import Path

ITEM = re.compile(r"^(\d+)\\?\.\s")

ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
ap.add_argument("key", type=Path)
ap.add_argument("ex", type=Path)
ap.add_argument("--glob", default="*.md", help="key files to compare (default *.md)")
args = ap.parse_args()

for d in (args.key, args.ex):
    if not d.is_dir():
        raise SystemExit(f"not a folder: {d}")
files = sorted(args.key.glob(args.glob))
print("FILES", len(files))


def items(p: Path) -> dict[tuple[str, int, int], tuple[int, str]]:
    out: dict[tuple[str, int, int], tuple[int, str]] = {}
    sec = "main"
    seen: Counter[tuple[str, int]] = Counter()
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.startswith("#") or re.match(r"^\*\*.*\*\*\s*$", line):
            if not ITEM.match(line):
                sec = re.sub(r"[#*]", "", line).strip().lower()
        m = ITEM.match(line)
        if m:
            k = (sec, int(m.group(1)))
            seen[k] += 1
            out[(sec, int(m.group(1)), seen[k])] = (
                i,
                ITEM.sub("", line, count=1).strip(),
            )
    return out


def flat(d: dict[tuple[str, int, int], tuple[int, str]]) -> list[tuple[int, int, str]]:
    return [(k[1], v[0], v[1]) for k, v in sorted(d.items(), key=lambda kv: kv[1][0])]


def norm(t: str) -> str:
    t = re.sub(r"\s*<br>\s*", " ", t).replace("**", "").replace("ṁ", "ṃ")
    t = re.sub(r"['’‘\"“”]", "", t)
    return re.sub(r"\s+", " ", t).strip()


print("== key vs exercise sentences")
fmt: list[str] = []
tot = diff = 0
for f in files:
    e = args.ex / f.name
    if not e.exists():
        print("NO EXERCISE FILE", e)
        continue
    ki, ei = flat(items(f)), flat(items(e))
    if len(ki) != len(ei):
        print(f"{f.name}: key items {len(ki)} vs ex items {len(ei)}")
    for (kn, kl, ks), (en, el, es) in zip(ki, ei):
        tot += 1
        if kn != en or norm(ks) != norm(es):
            diff += 1
            print(f"{f.name}:{kl} (ex:{el}) #{kn}/{en}\n   KEY {ks}\n   EX  {es}")
        if (" <br>" in ks) != (" <br>" in es) or ks.split("<br>")[
            0
        ].strip() != es.split("<br>")[0].strip():
            fmt.append(f"{f.name}:{kl} (ex:{el})")
print(
    "items compared",
    tot,
    "different after normalising quotes, bold, <br> spacing, ṁ:",
    diff,
)
print("label / <br>-spacing differences:", len(fmt), " ".join(fmt))
