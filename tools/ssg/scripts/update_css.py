from tools.ssg.scripts.paths import SSGPaths

def update_css(paths: SSGPaths):
    """Save the CSS Variables to the ssg/stylesheets folder."""
    
    if not paths.source_dpd_variables_css.exists():
        print(f"Warning: {paths.source_dpd_variables_css} not found.")
        return

    # Ensure stylesheets directory exists
    paths.stylesheets_dir.mkdir(parents=True, exist_ok=True)

    # Copy variables
    content = paths.source_dpd_variables_css.read_text()
    paths.dpd_variables_css.write_text(content)
    print(f"Updated: {paths.dpd_variables_css}")

    # Also copy main dpd.css if it exists
    if paths.source_dpd_css.exists():
        paths.dpd_css.write_text(paths.source_dpd_css.read_text())
        print(f"Updated: {paths.dpd_css}")

    # Also copy extra.css if it exists
    if paths.source_extra_css.exists():
        paths.extra_css.write_text(paths.source_extra_css.read_text())
        print(f"Updated: {paths.extra_css}")

def main():
    paths = SSGPaths()
    update_css(paths)

if __name__ == "__main__":
    main()
