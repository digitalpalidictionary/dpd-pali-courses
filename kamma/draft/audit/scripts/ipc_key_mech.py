"""Read-only mechanical checks over docs/ipc_key for the IPC key audit (tables, footnotes, links, key-vs-exercise sentences, convention counts)."""

import re
import unicodedata
from collections import Counter
from pathlib import Path

KEY = Path("docs/ipc_key")
EX = Path("docs/ipc_ex")
files = sorted(KEY.glob("*_class.md"))
ITEM = re.compile(r"^(\d+)\\?\.\s")

print("FILES", len(files), "LINES", sum(len(f.read_text().splitlines()) for f in files))
print("== table column mismatches")
rows = 0
for f in files:
    exp = None
    for i, line in enumerate(f.read_text().splitlines(), 1):
        if line.strip().startswith("|"):
            rows += 1
            n = len(re.sub(r"\\\|", "", line.strip()).strip("|").split("|"))
            if exp is None:
                exp = n
            elif n != exp:
                print(f"{f.name}:{i} cols {n} != {exp}: {line[:80]}")
        else:
            exp = None
print("table rows", rows)

print("== footnotes (course-wide)")
allrefs: list[tuple[str, str, int]] = []
alldefs: list[tuple[str, str, int]] = []
for f in files:
    for i, line in enumerate(f.read_text().splitlines(), 1):
        m = re.match(r"^\[\^([^\]]+)\]:", line)
        if m:
            alldefs.append((m.group(1), f.name, i))
        for r in re.findall(r"\[\^([^\]]+)\](?!:)", line):
            allrefs.append((r, f.name, i))
print("refs", len(allrefs), "defs", len(alldefs))
rc = Counter(r for r, _, _ in allrefs)
dc = Counter(d for d, _, _ in alldefs)
for k in sorted(set(rc) | set(dc), key=lambda x: (len(x), x)):
    if rc[k] != 1 or dc[k] != 1:
        print(f"footnote {k}: refs {rc[k]} defs {dc[k]}")
print("ref order:", " ".join(f"{r}@{f[:2]}" for r, f, _ in allrefs))
for (r, f, i), (d, f2, j) in zip(allrefs, alldefs):
    if r != d or f != f2:
        print(f"ORDER ref {r} {f}:{i} vs def {d} {f2}:{j}")

print("== key vs exercise sentences")


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


fmt: list[str] = []
tot = diff = 0
for f in files:
    e = EX / f.name
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

print("== misc")
conv: Counter[str] = Counter()
PAT = {
    "ṁ": "ṁ", "straight '": "'", "curly ’": "’", "curly ‘": "‘", 'straight "': '"',
    "curly “”": "[“”]", "<br>": "<br>", "...": r"\.\.\.", "…": "…", " - ": " - ",
    "–": "–", "—": "—", "Pāli": r"Pāli\b", "Pāḷi": "Pāḷi", "{:": r"\{:", "→": "→", ">": r"\\>",
    "lit:": r"lit:", "lit.": r"lit\.", "･": "･", "×": "×",
}  # fmt: skip
for f in files:
    txt = f.read_text()
    if unicodedata.normalize("NFC", txt) != txt:
        print("NON-NFC", f.name)
    if not txt.endswith("\n"):
        print("NO FINAL NEWLINE", f.name)
    for i, line in enumerate(txt.splitlines(), 1):
        if re.search(r"<(?!br>)(?!http)[a-zA-Z/][^>]*>", line):
            print(f"RAW HTML (not br) {f.name}:{i}: {line[:70]!r}")
        if re.search(r"&\w+;| ", line):
            print(f"ENTITY/NBSP {f.name}:{i}")
        if "\t" in line:
            print(f"TAB {f.name}:{i}")
        if re.search(r"[​‌‍﻿]", line):
            print(f"ZERO-WIDTH {f.name}:{i}")
        if line.count("**") % 2:
            print(f"ODD ** {f.name}:{i}: {line[:90]}")
        if line != line.rstrip():
            print(f"TRAILING SPACE {f.name}:{i}")
        if re.search(r"[Ѐ-ӿ]", line):
            print(f"CYRILLIC {f.name}:{i}: {line[:80]}")
        if re.search(r"  +\S", line.strip()):
            conv["double space"] += 1
        for k, p in PAT.items():
            conv[f"{k} | {f.name[:2]}"] += len(re.findall(p, line))
print("== convention counts (per class)")
for k in PAT:
    per = {f.name[:2]: conv[f"{k} | {f.name[:2]}"] for f in files}
    print(
        f"{k:12} total {sum(per.values()):5}  "
        + " ".join(f"{c}:{n}" for c, n in per.items() if n)
    )
print("double space lines", conv["double space"])
