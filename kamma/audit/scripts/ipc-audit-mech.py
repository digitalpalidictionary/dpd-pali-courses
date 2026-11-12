"""Read-only mechanical checks over docs/ipc for the IPC audit (table columns, links, anchors, index titles, headings, footnotes, stray characters).

Usage: uv run python kamma/audit/ipc-audit-mech.py <external_links_output.tsv>
Run from the repo root. Recreated from the 2026-11-10 session; not re-run after saving.
"""

import re
import sys
import unicodedata
from pathlib import Path

root = Path("docs/ipc")
files = sorted(root.rglob("*.md"))
print("FILES", len(files), "LINES", sum(len(f.read_text().splitlines()) for f in files))
print("== table column mismatches")
for f in files:
    lines = f.read_text().splitlines()
    exp = None
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("|"):
            n = len(re.sub(r"\\\|", "", line.strip()).strip("|").split("|"))
            if exp is None:
                exp = n
            elif n != exp:
                print(f"{f}:{i} cols {n} != {exp}: {line[:80]}")
        else:
            exp = None
print("== links")
ext = set()
for f in files:
    for i, line in enumerate(f.read_text().splitlines(), 1):
        for m in re.finditer(r"\[([^\]]*)\]\(([^)\s]+)\)", line):
            t = m.group(2)
            if t.startswith("http"):
                ext.add((t, str(f), i))
                continue
            if t.startswith("mailto"):
                continue
            p, _, a = t.partition("#")
            tgt = (f.parent / p).resolve() if p else f.resolve()
            if not tgt.exists():
                print(f"BROKEN {f}:{i} -> {t}")
                continue
            if a and tgt.suffix == ".md":
                txt = tgt.read_text()
                heads = {
                    re.sub(r"[^\w\- ]", "", h.lower()).strip().replace(" ", "-")
                    for h in re.findall(r"^#+\s+(.*)$", txt, re.M)
                }
                if a not in set(re.findall(r"\{:\s*#([\w-]+)", txt)) and a not in heads:
                    print(f"ANCHOR? {f}:{i} -> {t}")
        for m in re.finditer(r"(?<!\()(?<!\<)https?://[^\s)>\]]+", line):
            ext.add((m.group(0), str(f), i))
Path(sys.argv[1]).write_text("\n".join(f"{u}\t{f}:{i}" for u, f, i in sorted(ext)))
print("external link occurrences", len(ext), "unique", len({u for u, _, _ in ext}))
print("== index vs headings")
listed = set()
for idx in [root / "index.md"] + sorted(root.glob("class_*/index.md")):
    for i, line in enumerate(idx.read_text().splitlines(), 1):
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
                print(f"{idx}:{i} link '{m.group(1)}' vs H1 '{h1}' ({m.group(2)})")
for f in files:
    if f.resolve() not in listed and f != root / "index.md":
        print("NOT LISTED", f)
print("== misc")
for f in files:
    txt = f.read_text()
    if unicodedata.normalize("NFC", txt) != txt:
        print("NON-NFC", f)
    hs = [
        (i, len(m.group(1)))
        for i, line in enumerate(txt.splitlines(), 1)
        if (m := re.match(r"^(#+)\s", line))
    ]
    if not hs or hs[0][1] != 1:
        print("NO/LATE H1", f, hs[:1])
    if sum(1 for _, n in hs if n == 1) > 1:
        print("MULTI H1", f, [i for i, n in hs if n == 1])
    prev = 0
    for i, n in hs:
        if prev and n > prev + 1:
            print(f"HEADING JUMP {f}:{i} h{prev}->h{n}")
        prev = n
    for i, line in enumerate(txt.splitlines(), 1):
        if re.search(r"<(?!http)[a-zA-Z/][^>]*>", line):
            print(f"RAW HTML {f}:{i}: {line[:70]!r}")
        if re.search(r"&\w+;| ", line):
            print(f"ENTITY/NBSP {f}:{i}")
        if "\t" in line:
            print(f"TAB {f}:{i}")
        if re.search(r"[​‌‍﻿]", line):
            print(f"ZERO-WIDTH {f}:{i}")
        if re.match(r"^#+[^#\s]", line):
            print(f"HEADING NO SPACE {f}:{i}: {line[:50]}")
        if line.count("**") % 2:
            print(f"ODD ** {f}:{i}: {line[:90]}")
    refs = set(re.findall(r"\[\^([^\]]+)\](?!:)", txt))
    defs = set(re.findall(r"^\[\^([^\]]+)\]:", txt, re.M))
    if refs ^ defs:
        print(
            "FOOTNOTE MISMATCH", f, "refs-only", refs - defs, "defs-only", defs - refs
        )
    if not txt.endswith("\n"):
        print("NO FINAL NEWLINE", f)
