"""Merge the per-class IPC audit slices in kamma/audit/scratch into the final kamma/audit/ipc-audit.md."""

import re
from collections import defaultdict
from pathlib import Path

AUDIT = Path("/Users/deva/Documents/dpd-pali-courses/kamma/audit")
SCRATCH = AUDIT / "scratch"
SLICES = [
    ("index + 16", "ipc-audit-c16.md"),
    ("17", "ipc-audit-c17.md"),
    ("18", "ipc-audit-c18.md"),
    ("19", "ipc-audit-c19.md"),
    ("20–21", "ipc-audit-c20-21.md"),
    ("22–23", "ipc-audit-c22-23.md"),
    ("24–25", "ipc-audit-c24-25.md"),
    ("26–27", "ipc-audit-c26-27.md"),
]
TITLES = {
    "A": "A. Pāli and grammar content errors",
    "B": "B. Tables, paradigms and lists that disagree with each other or themselves",
    "C": "C. Translation and gloss problems",
    "D": "D. English typos and grammar",
    "E": "E. Markdown defects that affect rendering",
    "F": "F. Convention drift",
    "G": "G. Links",
    "H": "H. Data to re-verify (forms, references, counts)",
}


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def conf(row: list[str]) -> int:
    m = re.search(r"\d+", row[-1])
    return int(m.group()) if m else 0


rows: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
notes: list[str] = []

for label, name in SLICES:
    for line in (SCRATCH / name).read_text().splitlines():
        if line.startswith("- ") and name == "ipc-audit-c17.md":
            notes.append(line)
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        c = cells(line)
        if len(c) != 6 or c[0] == "Cat":
            continue
        rows[c[0]].append((label, [x.replace("¦", "\\|") for x in c[1:]]))

draft = (SCRATCH / "ipc-audit.md").read_text().splitlines()
start = next(i for i, x in enumerate(draft) if x.startswith("## CLASS 28"))
end = next(i for i, x in enumerate(draft) if x.startswith("## NOT AUDITED"))
cat = ""
conventions28: list[str] = []
in_conv = False
for line in draft[start:end]:
    m = re.match(r"### ([A-H])\. ", line)
    if m:
        cat, in_conv = m.group(1), False
        continue
    if line.startswith("### Conventions"):
        in_conv = True
        continue
    if in_conv and line.startswith("- "):
        conventions28.append(line)
    if cat and not in_conv and line.startswith("|") and not line.startswith("| ---"):
        c = cells(line)
        if len(c) == 5 and c[0] != "Location":
            rows[cat].append(("28", c))

m1 = next(i for i, x in enumerate(draft) if x.startswith("### M1."))
mech_detail = "\n".join(draft[m1:start]).rstrip().rstrip("-").rstrip()

labels = [s[0] for s in SLICES] + ["28"]
out: list[str] = []
out.append((SCRATCH / "ipc-audit-head.md").read_text().rstrip())
out.append("")
out.append("## Summary")
out.append("")
out.append("| Category | " + " | ".join(labels) + " | Total | Conf. ≥ 8 |")
out.append("| --- |" + " --- |" * (len(labels) + 2))
grand = hi = 0
for k in "ABCDEFGH":
    per = [sum(1 for lab, _ in rows[k] if lab == x) for x in labels]
    h = sum(1 for _, r in rows[k] if conf(r) >= 8)
    grand += sum(per)
    hi += h
    out.append(
        f"| {TITLES[k]} | " + " | ".join(str(p) for p in per) + f" | {sum(per)} | {h} |"
    )
tot = [sum(1 for k in "ABCDEFGH" for lab, _ in rows[k] if lab == x) for x in labels]
out.append(
    "| **Total** | "
    + " | ".join(f"**{t}**" for t in tot)
    + f" | **{grand}** | **{hi}** |"
)
out.append("")
out.append((SCRATCH / "ipc-audit-mid.md").read_text().rstrip())
out.append("")
for k in "ABCDEFGH":
    out.append(f"## {TITLES[k]}")
    out.append("")
    if not rows[k]:
        out.append("None beyond what is listed in the Method table.")
        out.append("")
        continue
    out.append("| Location | Current | Problem | Suggested | Conf. |")
    out.append("| --- | --- | --- | --- | --- |")
    for _, r in rows[k]:
        out.append("| " + " | ".join(r) + " |")
    out.append("")
out.append("## Mechanical detail")
out.append("")
out.append(mech_detail)
out.append("")
out.append("## Notes carried from the read")
out.append("")
out.extend(notes)
out.append("")
out.append("### Conventions observed in class 28")
out.append("")
out.extend(conventions28)
out.append("")
(AUDIT / "ipc-audit.md").write_text("\n".join(out) + "\n")
print(f"rows {grand}, conf>=8 {hi}, per slice {dict(zip(labels, tot))}")
print({k: len(rows[k]) for k in "ABCDEFGH"})
