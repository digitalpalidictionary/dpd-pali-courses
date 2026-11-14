"""Pure Markdown transforms shared by the web hook, PDF and DOCX pipelines."""

ATTRIBUTION_MARKER = "{: .align-right }"


def stack_table_cells(md: str, br: str) -> str:
    """Replace a spaced slash inside a table row with the format's line break."""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            lines[i] = line.replace(" / ", br)
    return "\n".join(lines)


def mark_attributions(md: str) -> str:
    """Append the right-align marker to an em-dash line that is its own paragraph."""
    lines = md.split("\n")
    out: list[str] = []
    for i, line in enumerate(lines):
        out.append(line)
        if not line.startswith("— "):
            continue
        if i > 0 and lines[i - 1].strip():
            continue
        is_last = i + 1 == len(lines)
        next_line = "" if is_last else lines[i + 1].strip()
        if next_line == ATTRIBUTION_MARKER:
            continue
        if is_last or not next_line:
            out.append(ATTRIBUTION_MARKER)
    return "\n".join(out)
