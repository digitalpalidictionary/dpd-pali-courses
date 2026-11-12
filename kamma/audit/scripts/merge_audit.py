"""Merge audit slice files into the final audit file, grouped by category with a summary table, as described by a small TOML config.

Usage, from the root of the project being audited:
    uv run python kamma/audit/scripts/merge_audit.py <merge.toml>

Config (paths are relative to the folder of the TOML file):
    out = "../ipc-key-audit.md"          # final file
    head = "head.md"                     # optional, hand-written: title, method, limits
    mid = "mid.md"                       # optional, hand-written: goes after the summary table
    tail = "mechdetail.md"               # optional, hand-written: goes last
    tail_title = "Mechanical detail"     # optional heading for the tail
    slices = [["16", "c16.md"], ["17–18", "c17-18.md"]]   # [summary column label, slice file], in order
    [titles]                             # optional, replaces the default categories A–I
    A = "A. …"
"""

import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

TITLES = {
    "A": "A. Pāli and grammar content errors",
    "B": "B. Tables, paradigms and lists that disagree with each other or themselves",
    "C": "C. Translation and gloss problems",
    "D": "D. English typos and grammar",
    "E": "E. Markdown defects that affect rendering",
    "F": "F. Convention drift",
    "G": "G. Links",
    "H": "H. Data to re-verify (forms, references, counts)",
    "I": "I. Further details on the material under review",
}


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def conf(row: list[str]) -> int:
    m = re.search(r"\d+", row[-1])
    return int(m.group()) if m else 0


def main(cfg_path: Path) -> None:
    base = cfg_path.parent
    cfg = tomllib.loads(cfg_path.read_text())
    titles: dict[str, str] = cfg.get("titles", TITLES)
    slices: list[tuple[str, str]] = [(str(a), str(b)) for a, b in cfg["slices"]]
    missing = [name for _, name in slices if not (base / name).is_file()]
    for key in ("head", "mid", "tail"):
        if key in cfg and not (base / cfg[key]).is_file():
            missing.append(cfg[key])
    if missing:
        raise SystemExit(f"missing files in {base}: {', '.join(missing)}")

    rows: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    skipped: list[str] = []
    for label, name in slices:
        for n, line in enumerate((base / name).read_text().splitlines(), 1):
            if not line.startswith("|") or line.startswith("| ---"):
                continue
            c = cells(line)
            if c[0] == "Cat":
                continue
            if len(c) != 6 or c[0] not in titles:
                skipped.append(f"{name}:{n}")
                continue
            rows[c[0]].append((label, [x.replace("¦", "\\|") for x in c[1:]]))

    labels = [s[0] for s in slices]
    out: list[str] = []
    if "head" in cfg:
        out += [(base / cfg["head"]).read_text().rstrip(), ""]
    out += ["## Summary", ""]
    out.append("| Category | " + " | ".join(labels) + " | Total | Conf. ≥ 8 |")
    out.append("| --- |" + " --- |" * (len(labels) + 2))
    grand = hi = 0
    for k in titles:
        per = [sum(1 for lab, _ in rows[k] if lab == x) for x in labels]
        h = sum(1 for _, r in rows[k] if conf(r) >= 8)
        grand += sum(per)
        hi += h
        out.append(
            f"| {titles[k]} | "
            + " | ".join(str(p) for p in per)
            + f" | {sum(per)} | {h} |"
        )
    tot = [sum(1 for k in titles for lab, _ in rows[k] if lab == x) for x in labels]
    out.append(
        "| **Total** | "
        + " | ".join(f"**{t}**" for t in tot)
        + f" | **{grand}** | **{hi}** |"
    )
    out.append("")
    if "mid" in cfg:
        out += [(base / cfg["mid"]).read_text().rstrip(), ""]
    for k in titles:
        out += [f"## {titles[k]}", ""]
        if not rows[k]:
            out += ["None.", ""]
            continue
        out.append("| Location | Current | Problem | Suggested | Conf. |")
        out.append("| --- | --- | --- | --- | --- |")
        for _, r in rows[k]:
            out.append("| " + " | ".join(r) + " |")
        out.append("")
    if "tail" in cfg:
        out += [f"## {cfg.get('tail_title', 'Mechanical detail')}", ""]
        out += [(base / cfg["tail"]).read_text().rstrip(), ""]
    dest = base / cfg["out"]
    dest.write_text("\n".join(out) + "\n")
    print(f"written {dest}")
    print(f"rows {grand}, conf>=8 {hi}, per slice {dict(zip(labels, tot))}")
    print({k: len(rows[k]) for k in titles})
    print({k: sum(1 for _, r in rows[k] if conf(r) >= 9) for k in titles}, "conf>=9")
    print("skipped rows:", skipped or "none")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]))
