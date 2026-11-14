"""Convert `<br>` and `{: … }` markup in the English course sources to the plain text conventions."""

import argparse
import re
import sys
from pathlib import Path

from markdown.extensions.toc import slugify

from tools.printer import printer as pr

FOLDERS = ("bpc", "bpc_ex", "bpc_key", "ipc", "ipc_ex", "ipc_key")
DOCS = Path("docs")

BR_RE = re.compile(r"\s*<br\s*/?>\s*")
ITEM_RE = re.compile(r"^(\d+\\?\.\s)")
BOLD_RE = re.compile(r"^\*\*.*\*\*$")
ALIGN_RE = re.compile(r"^\s*\{:\s*\.align-right\s*\}\s*$")
HEADING_ID_RE = re.compile(r"^(#+\s+)(.*?)\s*\{:\s*#([^}\s]+)\s*\}\s*$")
LINK_RE = re.compile(r"(\[[^\]]*\]\()([^)\s]+)(\))")

RULES: tuple[str, ...] = ("table", "item", "bold", "other", "align", "ids", "links")


class ConversionError(Exception):
    """A source file cannot be converted without changing its text."""


def source_files() -> list[Path]:
    """Every Markdown file in the six English course folders."""
    files: list[Path] = []
    for folder in FOLDERS:
        files.extend(sorted((DOCS / folder).rglob("*.md")))
    return files


def heading_ids(text: str) -> dict[str, str]:
    """Map each explicit heading id in a file to the slug Python-Markdown generates."""
    found: dict[str, str] = {}
    for line in text.split("\n"):
        m = HEADING_ID_RE.match(line)
        if m:
            found[m.group(3)] = slugify(m.group(2), "-")
    return found


def split_breaks(line: str) -> list[str]:
    """Split a line at every `<br>`, dropping empty segments."""
    segments = [s.strip() for s in BR_RE.split(line)]
    while segments and not segments[-1]:
        segments.pop()
    return segments


def drop_align_markers(lines: list[str], counts: dict[str, int]) -> list[str]:
    """Delete each `{: .align-right }` line and turn its target line into an attribution."""
    out: list[str] = []
    for line in lines:
        if not ALIGN_RE.match(line):
            out.append(line)
            continue
        target = len(out) - 1
        while target >= 0 and not out[target].strip():
            target -= 1
        if target < 0:
            raise ConversionError("align-right marker with no line above it")
        if out[target].startswith("\\- "):
            out[target] = "— " + out[target][3:]
        elif not out[target].startswith("— "):
            out[target] = "— " + out[target]
        counts["align"] += 1
    return out


def drop_heading_ids(lines: list[str], counts: dict[str, int]) -> list[str]:
    """Remove a heading's explicit `{: #id }` attribute."""
    out: list[str] = []
    for line in lines:
        m = HEADING_ID_RE.match(line)
        if m:
            out.append(m.group(1) + m.group(2))
            counts["ids"] += 1
        else:
            out.append(line)
    return out


def split_breaks_by_rule(lines: list[str], counts: dict[str, int]) -> list[str]:
    """Apply the table, item, bold and other-line `<br>` rules."""
    out: list[str] = []
    for line in lines:
        if not BR_RE.search(line):
            out.append(line)
            continue
        if line.lstrip().startswith("|"):
            counts["table"] += line.count("<br>")
            out.append(BR_RE.sub(" / ", line))
            continue
        segments = split_breaks(line)
        if not segments:
            out.append("")
            continue
        m = ITEM_RE.match(line)
        if m:
            counts["item"] += line.count("<br>")
            indent = " " * len(m.group(1))
            for segment in segments[1:]:
                if re.match(r"\d+\.\s", segment):
                    raise ConversionError(
                        f"continuation would become a list item: {segment!r}"
                    )
            out.append(segments[0])
            out.extend(indent + segment for segment in segments[1:])
            continue
        if BOLD_RE.match(line):
            counts["bold"] += line.count("<br>")
            inner = line[2:-2]
            for segment in split_breaks(inner):
                out.append(f"**{segment}**")
            continue
        counts["other"] += line.count("<br>")
        out.extend(segments)
    return out


def convert_text(text: str, counts: dict[str, int]) -> str:
    """Apply every markup rule to one file's text."""
    lines = drop_align_markers(text.split("\n"), counts)
    lines = drop_heading_ids(lines, counts)
    return "\n".join(split_breaks_by_rule(lines, counts))


def rewrite_links(
    text: str, path: Path, slug_maps: dict[Path, dict[str, str]], counts: dict[str, int]
) -> str:
    """Point links at the slug a heading will actually generate."""

    def repl(m: re.Match[str]) -> str:
        target = m.group(2)
        if "#" not in target:
            return m.group(0)
        path_part, fragment = target.split("#", 1)
        if path_part:
            dest = (path.parent / path_part).resolve()
        else:
            dest = path.resolve()
        mapping = slug_maps.get(dest)
        if not mapping or fragment not in mapping:
            return m.group(0)
        new_fragment = mapping[fragment]
        if new_fragment == fragment:
            return m.group(0)
        counts["links"] += 1
        return f"{m.group(1)}{path_part}#{new_fragment}{m.group(3)}"

    return LINK_RE.sub(repl, text)


def normalise(text: str) -> str:
    """Collapse every difference the conversion is allowed to introduce."""
    text = re.sub(r"\{:[^}]*\}", "", text)
    text = re.sub(r"<br\s*/?>", "", text)
    text = re.sub(r"\]\(([^)\s#]*)#[^)\s]*\)", r"](\1)", text)
    text = text.replace("/", "")
    text = re.sub(r"^(?:\\?-|—) ", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", "", text)
    return text.replace("**", "")


def convert_file(
    text: str,
    path: Path,
    slug_maps: dict[Path, dict[str, str]],
    counts: dict[str, int],
) -> str:
    """Convert one file and refuse the result if any text was lost."""
    new_text = convert_text(text, counts)
    new_text = rewrite_links(new_text, path, slug_maps, counts)
    if normalise(text) != normalise(new_text):
        raise ConversionError("invariant failed: text before and after differs")
    return new_text


def plan() -> tuple[dict[Path, str], dict[Path, str], dict[str, int], list[str]]:
    """Build the converted text for every file and check the no-data-loss invariant."""
    files = source_files()
    originals: dict[Path, str] = {}
    for path in files:
        originals[path] = path.read_text(encoding="utf-8")

    slug_maps = {path.resolve(): heading_ids(text) for path, text in originals.items()}

    converted: dict[Path, str] = {}
    problems: list[str] = []
    counts = dict.fromkeys(RULES, 0)
    for path, text in originals.items():
        file_counts = dict.fromkeys(RULES, 0)
        try:
            new_text = convert_file(text, path, slug_maps, file_counts)
        except ConversionError as exc:
            problems.append(f"{path}: {exc}")
            continue
        converted[path] = new_text
        for rule in RULES:
            counts[rule] += file_counts[rule]
    return converted, originals, counts, problems


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert <br> and {: .align-right } / {: #id } markup to plain text."
    )
    parser.add_argument(
        "--apply", action="store_true", help="write the changes (default: dry run)"
    )
    args = parser.parse_args()

    pr.green_tmr("Converting markup")
    converted, originals, counts, problems = plan()

    if problems:
        pr.no(f"{len(problems)} files")
        for problem in problems:
            pr.amber(problem)
        sys.exit(1)

    changed = {
        path: text for path, text in converted.items() if text != originals[path]
    }
    if args.apply:
        for path, text in changed.items():
            path.write_text(text, encoding="utf-8")
        pr.yes(f"{len(changed)} files")
    else:
        pr.yes(f"{len(changed)} files (dry run)")

    for rule in RULES:
        pr.white(f"{rule:<8}{counts[rule]:>6}")


if __name__ == "__main__":
    main()
