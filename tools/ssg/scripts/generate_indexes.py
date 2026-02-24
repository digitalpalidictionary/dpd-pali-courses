import yaml
from pathlib import Path
from tools.ssg.scripts.paths import SSGPaths

def process_nav_items(items, docs_dir):
    if isinstance(items, str):
        return

    pages = []
    submenu_dir = None

    for entry in items:
        if isinstance(entry, str):
            path = Path(entry)
            title = path.stem
            # Use the directory containing the file
            dir_part = str(path.parent) if str(path.parent) != "." else ""
        elif isinstance(entry, dict):
            title = next(iter(entry.keys()))
            value = entry[title]
            if isinstance(value, list):
                process_nav_items(value, docs_dir)
                continue
            else:
                path = Path(value)
                dir_part = str(path.parent) if str(path.parent) != "." else ""
        else:
            continue

        if path.suffix == ".md" and path.name != "index.md":
            pages.append(
                {"title": title, "filename": path.name, "dir": dir_part}
            )
        elif path.name == "index.md":
            submenu_dir = dir_part

    if submenu_dir is not None and pages:
        target_dir = docs_dir / submenu_dir
        index_path = target_dir / "index.md"

        if not index_path.parent.exists():
            index_path.parent.mkdir(parents=True, exist_ok=True)

        content = ""
        if index_path.exists():
            content = index_path.read_text()
        
        if "1. [" not in content:
            with open(index_path, "a") as f:
                f.write("\n")
                for page in pages:
                    # If pages are in the same directory as index.md, we use just filename
                    # In mkdocs, paths in nav are relative to docs_dir.
                    f.write(f"1. [{page['title']}]({page['filename']})\n")
            print(f"Generated: {index_path}")

def generate_indexes(paths: SSGPaths):
    docs_dir = paths.docs_dir

    if not paths.mkdocs_yaml.exists():
        print(f"Warning: {paths.mkdocs_yaml} not found.")
        return

    with open(paths.mkdocs_yaml, "r") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    process_nav_items(nav, docs_dir)

def main():
    paths = SSGPaths()
    generate_indexes(paths)

if __name__ == "__main__":
    main()
