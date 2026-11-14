"""MkDocs hook that renders the clean-markup source conventions for the website."""

from tools.clean_markup import mark_attributions, stack_table_cells

# Spaced slashes only mean "stacked" in the hand-written course sources;
# docs/generated/ comes from the dpd-db exporter and uses ` / ` as plain text.
COURSE_FOLDERS = ("bpc/", "bpc_ex/", "bpc_key/", "ipc/", "ipc_ex/", "ipc_key/")


def on_page_markdown(markdown, page, config, files):
    """Stack spaced cell slashes as <br> and right-align em-dash attributions."""
    if page.file.src_path.replace("\\", "/").startswith(COURSE_FOLDERS):
        markdown = stack_table_cells(markdown, "<br>")
    return mark_attributions(markdown)
