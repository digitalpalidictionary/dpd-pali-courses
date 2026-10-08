"""
Script to synchronize CSS variables from source configurations to the SSG stylesheets.
"""
from tools.paths import SSGPaths
from tools.printer import printer as pr

def update_css(paths: SSGPaths) -> bool:
    """Save the CSS Variables to the ssg/stylesheets folder."""

    if not paths.source_dpd_variables_css.exists():
        return False

    # Ensure identity directory exists
    paths.identity_dir.mkdir(parents=True, exist_ok=True)

    # Copy variables
    content = paths.source_dpd_variables_css.read_text()
    if content != paths.dpd_variables_css.read_text():
        paths.dpd_variables_css.write_text(content)

    # Also copy main dpd.css if it exists
    if paths.source_dpd_css.exists() and paths.source_dpd_css != paths.dpd_css:
        paths.dpd_css.write_text(paths.source_dpd_css.read_text())

    # Also copy extra.css if it exists
    if paths.source_extra_css.exists() and paths.source_extra_css != paths.extra_css:
        paths.extra_css.write_text(paths.source_extra_css.read_text())
    return True

def main():
    pr.green_tmr("Updating CSS")
    paths = SSGPaths()
    if update_css(paths):
        pr.yes("ok")
    else:
        pr.no("not found")
        pr.amber(str(paths.source_dpd_variables_css))

if __name__ == "__main__":
    main()
