import os
import yaml
import markdown

def convert_to_html(md_content):
    md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'attr_list', 'sane_lists'])
    return md.convert(md_content)

def build_html_document(title, files_data):
    md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'attr_list', 'sane_lists'])
    
    full_md_content = ""
    for file_path, content in files_data:
        full_md_content += f"\n\n<!-- FILE: {file_path} -->\n\n" + content + "\n\n"
        
    body_html = md.convert(full_md_content)
    toc_html = md.toc
    
    html_template = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
</head>
<body>
    <div class="toc">
        <h1>Table of Contents</h1>
        {toc_html}
    </div>
    <div class="content">
        {body_html}
    </div>
</body>
</html>
"""
    return html_template

def extract_markdown_files(nav_item, docs_dir, current_list):
    if isinstance(nav_item, str):
        if nav_item.endswith('.md'):
            current_list.append(os.path.join(docs_dir, nav_item))
    elif isinstance(nav_item, list):
        for item in nav_item:
            extract_markdown_files(item, docs_dir, current_list)
    elif isinstance(nav_item, dict):
        for key, value in nav_item.items():
            extract_markdown_files(value, docs_dir, current_list)

def get_markdown_files(docs_dir: str):
    """
    Reads the markdown files from the subdirectories in docs_dir based on mkdocs.yaml order.
    """
    mkdocs_yaml_path = "mkdocs.yaml"
    if not os.path.exists(mkdocs_yaml_path):
        # Fallback if run from a different directory
        mkdocs_yaml_path = os.path.join(os.path.dirname(__file__), "..", "mkdocs.yaml")
        
    with open(mkdocs_yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    nav = config.get("nav", [])
    
    all_files = []
    extract_markdown_files(nav, docs_dir, all_files)
    
    folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
    files_by_dir = {f: [] for f in folders}
    
    for file_path in all_files:
        rel_path = os.path.relpath(file_path, docs_dir)
        folder = rel_path.split(os.sep)[0]
        if folder in files_by_dir:
            if os.path.exists(file_path):
                files_by_dir[folder].append(file_path)
            
    return files_by_dir

def generate_pdf(html_content, output_pdf, css_paths=None):
    from weasyprint import HTML, CSS
    if css_paths is None:
        css_paths = []
    
    css_objects = [CSS(filename=path) for path in css_paths if os.path.exists(path)]
    
    html_obj = HTML(string=html_content, base_url=os.path.abspath("."))
    html_obj.write_pdf(output_pdf, stylesheets=css_objects)

def main():
    docs_dir = "docs"
    
    css_paths = [
        "tools/ssg/stylesheets/dpd-variables.css",
        "tools/ssg/stylesheets/dpd.css",
        "tools/ssg/stylesheets/extra.css"
    ]
    
    files_by_dir = get_markdown_files(docs_dir)
    
    for folder, files in files_by_dir.items():
        if not files:
            print(f"Skipping {folder}, no files found.")
            continue
            
        print(f"Processing {folder} into {folder}.pdf...")
        
        files_data = []
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            files_data.append((file_path, content))
            
        html_content = build_html_document(f"{folder.upper()} Course Materials", files_data)
        
        output_pdf = f"{folder}.pdf"
        generate_pdf(html_content, output_pdf, css_paths=css_paths)
        print(f"Successfully created {output_pdf}")

if __name__ == '__main__':
    main()
