"""
Script to generate index.md pages for course categories.
Creates a Table of Contents based on individual lesson headings.
"""
import re
import os
from tools.paths import SSGPaths
from tools.printer import printer as pr

def clean_title(title):
    """Normalized title cleanup."""
    if not title:
        return ""
    # Strip footnote references (e.g. [^1], [^18])
    title = re.sub(r'\[\^\d+\]', '', title)
    # Strip attribute lists (e.g. {: #anchor} or {#anchor})
    title = re.sub(r'\{.*?\}', '', title)
    title = re.sub(r'!\[.*?\]\(.*?\)', '', title)
    title = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', title)
    title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)
    title = re.sub(r'\*(.*?)\*', r'\1', title)
    title = re.sub(r'^\*+\s*', '', title)
    title = re.sub(r'\s*\*+$', '', title)
    title = title.replace("***", "").strip()
    return title

def get_first_heading(file_path):
    """Extracts the first heading or relevant line."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line == "***":
                    continue
                if line.startswith("# ") or line.startswith("## "):
                    return clean_title(line.lstrip("#").strip())
                elif line.startswith("**") and line.endswith("**"):
                    return clean_title(line)
                elif not any(line.startswith(c) for line in [line] for c in ["!", "[", "*", "#"]):
                    return clean_title(line)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def get_all_headings(file_path):
    """Extracts all ## headings."""
    headings = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("## "):
                    headings.append(clean_title(line[3:]))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return headings

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(s))]

def should_skip_in_main_index(heading, filename):
    if not heading:
        return True
    h_lower = heading.lower()
    f_lower = filename.lower()
    skip_keywords = ["review", "homeless work", "home work", "homework"]
    if any(kw in h_lower for kw in skip_keywords):
        return True
    if any(kw in f_lower for kw in skip_keywords):
        return True
    if "content" in f_lower or "title" in f_lower or "literature" in f_lower:
        return True
    return False

def get_all_pages(paths: SSGPaths):
    """Returns a flat list of all relevant pages in order, including class indexes."""
    all_pages = []
    sections = ["bpc", "ipc", "bpc_ex", "ipc_ex", "bpc_key", "ipc_key"]
    for section in sections:
        section_path = paths.docs_dir / section
        if not section_path.exists():
            continue
        top_files = sorted([f for f in section_path.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
        for f in top_files:
            all_pages.append(f)
        subdirs = sorted([d for d in section_path.iterdir() if d.is_dir() and d.name.startswith("class_")], key=natural_sort_key)
        for subdir in subdirs:
            class_index = subdir / "index.md"
            if class_index.exists():
                all_pages.append(class_index)
            class_files = sorted([f for f in subdir.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
            for f in class_files:
                all_pages.append(f)
    return all_pages

def remove_navigation_block(content):
    """Removes ANY existing navigation artifacts aggressively."""
    markers = [
        r'<div class="nav-links"',
        r'<div class="feedback"',
        r'<div class="cross"',
        r'^---\s*$',
        r'\[Previous:',
        r'\[←',
        r'\[Go to Exercises\]',
        r'\[Go to Answer Key\]',
        r'Provide feedback on this page'
    ]
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        if any(re.search(m, line, re.IGNORECASE) for m in markers):
            break
        clean_lines.append(line)
    return '\n'.join(clean_lines).strip()

def get_html_rel_path(file_path, target_path):
    rel = os.path.relpath(target_path, file_path.parent)
    prefix = "" if file_path.name == "index.md" else "../"
    if rel.endswith("index.md"):
        dir_rel = rel[:-8]
        if dir_rel == "" or dir_rel == ".":
            return prefix or "./"
        return prefix + dir_rel
    return prefix + rel.replace(".md", "/")

def update_page_navigation(file_path, prev_page, next_page, all_headings, docs_dir):
    # DO NOT INJECT NAV LINKS INTO MD SOURCES
    # All navigation should be handled by MkDocs hooks/theme.
    pass

def generate_section_index(section_path, title):
    index_path = section_path / "index.md"
    subdirs = sorted([d for d in section_path.iterdir() if d.is_dir() and d.name.startswith("class_")], key=natural_sort_key)
    content = [f"# {title}\n"]
    if subdirs:
        for subdir in subdirs:
            class_num_match = re.search(r'\d+', subdir.name)
            if not class_num_match:
                continue
            class_num = class_num_match.group()
            class_label = f"Class {class_num}"
            content.append(f"## [{class_label}]({subdir.name}/index.md)")
            if class_num == "1":
                lesson_file = subdir / "1_class.md"
                if lesson_file.exists():
                    sub_headings = get_all_headings(lesson_file)
                    for sh in sub_headings:
                        content.append(f"- {sh}")
            files = sorted([f for f in subdir.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
            for f in files:
                topic_heading = get_first_heading(f)
                if topic_heading and not should_skip_in_main_index(topic_heading, f.name):
                    rel_path = f.relative_to(section_path)
                    content.append(f"- [{topic_heading}]({rel_path})")
            content.append("")
            generate_class_index(subdir, class_label)
    else:
        files = sorted([f for f in section_path.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
        for f in files:
            heading = get_first_heading(f)
            if heading:
                content.append(f"- [{heading}]({f.name})")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

def generate_class_index(class_path, class_title):
    if class_path.name == "class_1":
        return
    index_path = class_path / "index.md"
    files = sorted([f for f in class_path.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
    content = [f"# {class_title}\n"]
    for f in files:
        heading = get_first_heading(f)
        if heading:
            content.append(f"- [{heading}]({f.name})")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

def main(paths=None):
    pr.green("Generating index pages")
    if paths is None:
        paths = SSGPaths()
    sections = {
        "bpc": "Beginner Pāḷi Course (BPC)",
        "ipc": "Intermediate Pāḷi Course (IPC)",
        "bpc_ex": "BPC Exercises",
        "bpc_key": "BPC Keys",
        "ipc_ex": "IPC Exercises",
        "ipc_key": "IPC Keys"
    }
    for folder, title in sections.items():
        section_path = paths.docs_dir / folder
        if section_path.exists():
            generate_section_index(section_path, title)
    
    all_pages = get_all_pages(paths)
    all_headings = {p: get_first_heading(p) for p in all_pages}
    
    # Track class index pages specifically for class-to-class flow
    class_indexes = [p for p in all_pages if p.name == "index.md" and "class_" in p.parent.name]
    
    for i, page in enumerate(all_pages):
        prev_page = all_pages[i-1] if i > 0 else None
        next_page = all_pages[i+1] if i < len(all_pages)-1 else None
        
        # Override for Class Index pages: They should link to Previous/Next Class Index
        if page in class_indexes:
            idx = class_indexes.index(page)
            prev_page = class_indexes[idx-1] if idx > 0 else None
            next_page = class_indexes[idx+1] if idx < len(class_indexes)-1 else None
        
        if prev_page and prev_page.relative_to(paths.docs_dir).parts[0] != page.relative_to(paths.docs_dir).parts[0]:
            prev_page = None
        if next_page and next_page.relative_to(paths.docs_dir).parts[0] != page.relative_to(paths.docs_dir).parts[0]:
            next_page = None
            
        update_page_navigation(page, prev_page, next_page, all_headings, paths.docs_dir)

    pr.yes("ok")

if __name__ == "__main__":
    main()
