import re
import os
import urllib.parse
from pathlib import Path
from tools.ssg.scripts.paths import SSGPaths

def clean_title(title):
    """Normalized title cleanup."""
    if not title:
        return ""
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
                if line.startswith("# "):
                    return clean_title(line[2:])
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

def get_feedback_link(file_rel_path):
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSeCZ01pgGSYZDO7c1p7L5ciQfg1gEPIEx1g0RgPaCxSY_fQcg/viewform"
    parts = list(file_rel_path.parts)
    course = "Beginner Pāḷi Course (BPC)"
    if any(p in parts[0] for p in ["ipc", "ipc_ex", "ipc_key"]):
        course = "Intermediate Pāḷi Course (IPC)"
    page_name = str(file_rel_path).replace(".md", "")
    if page_name.endswith("/index"):
        page_name = page_name[:-5]
    elif page_name == "index":
        page_name = ""
    params = {"usp": "pp_url", "entry.135905709": course, "entry.2980976": page_name}
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"

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
    heading = all_headings.get(file_path)
    if not heading:
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = remove_navigation_block(content)
    file_rel = file_path.relative_to(docs_dir)
    prev_link = ""
    if prev_page:
        prev_heading = all_headings.get(prev_page, "Previous")
        html_rel = get_html_rel_path(file_path, prev_page)
        prev_link = f'<a href="{html_rel}" class="prev">← {prev_heading}</a>'
    next_link = ""
    if next_page:
        next_heading = all_headings.get(next_page, "Next")
        html_rel = get_html_rel_path(file_path, next_page)
        next_link = f'<a href="{html_rel}" class="next">{next_heading} →</a>'
    cross_link = ""
    parts = list(file_rel.parts)
    if parts[0] == "bpc" and len(parts) > 1 and "class_" in parts[1]:
        class_num = re.search(r'\d+', parts[1])
        if class_num:
            ex_path = docs_dir / "bpc_ex" / f"{class_num.group()}_class.md"
            if ex_path.exists():
                html_rel = get_html_rel_path(file_path, ex_path)
                cross_link = f'<a href="{html_rel}">Go to Exercises</a>'
    elif parts[0] == "bpc_ex":
        class_num_match = re.search(r'\d+', parts[0] if len(parts) == 1 else parts[1])
        if class_num_match:
            key_path = docs_dir / "bpc_key" / f"{class_num_match.group()}_class.md"
            if key_path.exists():
                html_rel = get_html_rel_path(file_path, key_path)
                cross_link = f'<a href="{html_rel}">Go to Answer Key</a>'
    elif parts[0] == "ipc" and len(parts) > 1 and "class_" in parts[1]:
        class_num = re.search(r'\d+', parts[1])
        if class_num:
            ex_path = docs_dir / "ipc_ex" / f"{class_num.group()}_class.md"
            if ex_path.exists():
                html_rel = get_html_rel_path(file_path, ex_path)
                cross_link = f'<a href="{html_rel}">Go to Exercises</a>'
    elif parts[0] == "ipc_ex":
        class_num_match = re.search(r'\d+', parts[0] if len(parts) == 1 else parts[1])
        if class_num_match:
            key_path = docs_dir / "ipc_key" / f"{class_num_match.group()}_class.md"
            if key_path.exists():
                html_rel = get_html_rel_path(file_path, key_path)
                cross_link = f'<a href="{html_rel}">Go to Answer Key</a>'
    feedback_url = get_feedback_link(file_rel)
    feedback_link = f'<a href="{feedback_url}" target="_blank">Provide feedback on this page</a>'
    if prev_link or next_link or cross_link:
        nav_html = '\n\n<div class="nav-links">\n'
        if prev_link:
            nav_html += f'  {prev_link}\n'
        if next_link:
            nav_html += f'  {next_link}\n'
        if cross_link:
            nav_html += f'  <div class="cross">{cross_link}</div>\n'
        nav_html += f'  <div class="feedback">{feedback_link}</div>\n'
        nav_html += '</div>\n'
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.write(nav_html)

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
    index_path = class_path / "index.md"
    files = sorted([f for f in class_path.glob("*.md") if f.name != "index.md"], key=lambda x: natural_sort_key(x.name))
    content = [f"# {class_title}\n"]
    for f in files:
        heading = get_first_heading(f)
        if heading:
            content.append(f"1. [{heading}]({f.name})")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

def main():
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

if __name__ == "__main__":
    main()
