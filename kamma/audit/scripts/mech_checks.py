"""Read-only mechanical checks over any folder of Markdown files for an audit (table columns, links, anchors, index titles, headings, footnotes, stray characters, convention counts).

Usage, from the root of the project being audited:
    uv run python kamma/audit/scripts/mech_checks.py <folder> [--links-out FILE] [--folder-footnotes]

--links-out FILE     write every external link with its location to FILE (tsv), for an HTTP status check
--folder-footnotes   footnote ids are numbered across the whole folder, not per file
"""

import argparse
import re
import unicodedata
from collections import Counter
from pathlib import Path

PAT = {
    "ṁ": "ṁ", "straight '": "'", "curly ’": "’", "curly ‘": "‘", 'straight "': '"',
    "curly “”": "[“”]", "<br>": "<br>", "...": r"\.\.\.", "…": "…", " - ": " - ",
    "–": "–", "—": "—", "Pāli": r"Pāli\b", "Pāḷi": "Pāḷi", "{:": r"\{:", "→": "→", ">": r"\\>",
    "lit:": r"lit:", "lit.": r"lit\.", "･": "･", "×": "×",
}  # fmt: skip
MAX_GROUPS = 40

ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
ap.add_argument("folder", type=Path)
ap.add_argument("--links-out", type=Path)
ap.add_argument("--folder-footnotes", action="store_true")
args = ap.parse_args()

root: Path = args.folder
if not root.is_dir():
    raise SystemExit(f"not a folder: {root}")
files = sorted(root.rglob("*.md"))
texts = {f: f.read_text() for f in files}


def rel(f: Path) -> str:
    return str(f.relative_to(root))


def group(f: Path) -> str:
    parts = f.relative_to(root).parts
    return parts[0] if len(parts) > 1 else f.stem


print("FILES", len(files), "LINES", sum(len(t.splitlines()) for t in texts.values()))

print("== table column mismatches")
table_rows = 0
for f in files:
    exp = None
    for i, line in enumerate(texts[f].splitlines(), 1):
        if line.strip().startswith("|"):
            table_rows += 1
            n = len(re.sub(r"\\\|", "", line.strip()).strip("|").split("|"))
            if exp is None:
                exp = n
            elif n != exp:
                print(f"{rel(f)}:{i} cols {n} != {exp}: {line[:80]}")
        else:
            exp = None
print("table rows", table_rows)

print("== links")
ext: set[tuple[str, str, int]] = set()
for f in files:
    for i, line in enumerate(texts[f].splitlines(), 1):
        for m in re.finditer(r"\[([^\]]*)\]\(([^)\s]+)\)", line):
            t = m.group(2)
            if t.startswith("http"):
                ext.add((t, rel(f), i))
                continue
            if t.startswith("mailto"):
                continue
            p, _, a = t.partition("#")
            tgt = (f.parent / p).resolve() if p else f.resolve()
            if not tgt.exists():
                print(f"BROKEN {rel(f)}:{i} -> {t}")
                continue
            if a and tgt.suffix == ".md":
                txt = tgt.read_text()
                heads = {
                    re.sub(r"[^\w\- ]", "", h.lower()).strip().replace(" ", "-")
                    for h in re.findall(r"^#+\s+(.*)$", txt, re.M)
                }
                if a not in set(re.findall(r"\{:\s*#([\w-]+)", txt)) and a not in heads:
                    print(f"ANCHOR? {rel(f)}:{i} -> {t}")
        for m in re.finditer(r"(?<!\()(?<!\<)https?://[^\s)>\]]+", line):
            ext.add((m.group(0), rel(f), i))
print("external link occurrences", len(ext), "unique", len({u for u, _, _ in ext}))
if args.links_out:
    args.links_out.write_text("\n".join(f"{u}\t{f}:{i}" for u, f, i in sorted(ext)))
    print("external links written to", args.links_out)

print("== index vs headings")
indexes = [f for f in files if f.name == "index.md"]
listed: set[Path] = set()
for idx in indexes:
    for i, line in enumerate(texts[idx].splitlines(), 1):
        for m in re.finditer(r"\[([^\]]*)\]\(([^)#\s]+\.md)(#[^)]*)?\)", line):
            tgt = (idx.parent / m.group(2)).resolve()
            if not tgt.exists():
                continue
            listed.add(tgt)
            if m.group(3):
                continue
            h = re.search(r"^#\s+(.*)$", tgt.read_text(), re.M)
            h1 = h.group(1).strip() if h else None
            if h1 != m.group(1).strip():
                print(f"{rel(idx)}:{i} link '{m.group(1)}' vs H1 '{h1}' ({m.group(2)})")
if indexes:
    for f in files:
        if f.resolve() not in listed and f != root / "index.md":
            print("NOT LISTED", rel(f))
else:
    print("no index.md in the folder")

print("== footnotes")
allrefs: list[tuple[str, str, int]] = []
alldefs: list[tuple[str, str, int]] = []
for f in files:
    refs: set[str] = set()
    defs: set[str] = set()
    for i, line in enumerate(texts[f].splitlines(), 1):
        m = re.match(r"^\[\^([^\]]+)\]:", line)
        if m:
            defs.add(m.group(1))
            alldefs.append((m.group(1), rel(f), i))
            line = line[m.end() :]
        for r in re.findall(r"\[\^([^\]]+)\]", line):
            refs.add(r)
            allrefs.append((r, rel(f), i))
    if not args.folder_footnotes and refs ^ defs:
        print(
            f"FOOTNOTE MISMATCH {rel(f)} refs-only {sorted(refs - defs)} defs-only {sorted(defs - refs)}"
        )
print("refs", len(allrefs), "defs", len(alldefs))
if args.folder_footnotes:
    rc = Counter(r for r, _, _ in allrefs)
    dc = Counter(d for d, _, _ in alldefs)
    for k in sorted(set(rc) | set(dc), key=lambda x: (len(x), x)):
        if rc[k] != 1 or dc[k] != 1:
            print(f"footnote {k}: refs {rc[k]} defs {dc[k]}")
    for (r, f1, i), (d, f2, j) in zip(allrefs, alldefs):
        if r != d or f1 != f2:
            print(f"ORDER ref {r} {f1}:{i} vs def {d} {f2}:{j}")

print("== misc")
conv: Counter[tuple[str, str]] = Counter()
double_space = 0
for f in files:
    txt = texts[f]
    if unicodedata.normalize("NFC", txt) != txt:
        print("NON-NFC", rel(f))
    if not txt.endswith("\n"):
        print("NO FINAL NEWLINE", rel(f))
    hs = [
        (i, len(m.group(1)))
        for i, line in enumerate(txt.splitlines(), 1)
        if (m := re.match(r"^(#+)\s", line))
    ]
    if not hs or hs[0][1] != 1:
        print("NO/LATE H1", rel(f), hs[:1])
    if sum(1 for _, n in hs if n == 1) > 1:
        print("MULTI H1", rel(f), [i for i, n in hs if n == 1])
    prev = 0
    for i, n in hs:
        if prev and n > prev + 1:
            print(f"HEADING JUMP {rel(f)}:{i} h{prev}->h{n}")
        prev = n
    for i, line in enumerate(txt.splitlines(), 1):
        if re.search(r"<(?!br>)(?!http)[a-zA-Z/][^>]*>", line):
            print(f"RAW HTML (not br) {rel(f)}:{i}: {line[:70]!r}")
        if re.search("&\\w+;| ", line):
            print(f"ENTITY/NBSP {rel(f)}:{i}")
        if "\t" in line:
            print(f"TAB {rel(f)}:{i}")
        if re.search("[​‌‍﻿]", line):
            print(f"ZERO-WIDTH {rel(f)}:{i}")
        if re.match(r"^#+[^#\s]", line):
            print(f"HEADING NO SPACE {rel(f)}:{i}: {line[:50]}")
        if line.count("**") % 2:
            print(f"ODD ** {rel(f)}:{i}: {line[:90]}")
        if line != line.rstrip():
            print(f"TRAILING SPACE {rel(f)}:{i}")
        if re.search("[Ѐ-ӿ]", line):
            print(f"CYRILLIC {rel(f)}:{i}: {line[:80]}")
        if re.search(r"  +\S", line.strip()):
            double_space += 1
        for k, p in PAT.items():
            conv[(k, group(f))] += len(re.findall(p, line))

groups = list(dict.fromkeys(group(f) for f in files))
print("== convention counts" + (" (per group)" if len(groups) <= MAX_GROUPS else ""))
for k in PAT:
    per = {g: conv[(k, g)] for g in groups}
    detail = (
        "  " + " ".join(f"{g}:{n}" for g, n in per.items() if n)
        if len(groups) <= MAX_GROUPS
        else ""
    )
    print(f"{k:12} total {sum(per.values()):5}{detail}")
print("double space lines", double_space)
