"""
Helper script to update mkdocs.yaml based on course folder structure.
Automatically generates the navigation section using headings from Markdown files.
"""
import os
import re
import yaml

from tools.printer import printer as pr

def get_first_heading(file_path):
    """Extracts the first level 1 heading and strips numbers/IDs."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    h = line.replace('# ', '').strip()
                    h = re.sub(r'^\d+[\.\s\)]*\s*', '', h)
                    h = re.sub(r'\{:.*\}', '', h).strip()
                    return h
    except Exception:
        pass
    return None

def get_files_sorted(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.md') and f != 'index.md']
    def sort_key(f):
        parts = f.split('_')
        if parts[0].isdigit():
            return (0, int(parts[0]))
        return (1, f)
    return sorted(files, key=sort_key)

def build_class_nav(base_dir):
    folders = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('class_')], 
                     key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else 0)
    nav = []
    section_index = os.path.join(base_dir, 'index.md').replace('docs/', '')
    if os.path.exists(os.path.join('docs', section_index)):
        nav.append({'Lessons Index': section_index})

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        items = []
        index_path = os.path.join(folder_path, 'index.md')
        if os.path.exists(index_path):
            items.append({'Index': index_path.replace('docs/', '')})
        for f in get_files_sorted(folder_path):
            file_path = os.path.join(folder_path, f)
            h = get_first_heading(file_path)
            items.append({(h if h else f.replace('.md', '').title()): file_path.replace('docs/', '')})
        if len(items) == 1:
            nav.append({f"Class {folder.split('_')[1]}": list(items[0].values())[0]})
        else:
            nav.append({f"Class {folder.split('_')[1]}": items})
    return nav

def build_file_nav(directory):
    nav = []
    index_path = os.path.join(directory, 'index.md')
    if os.path.exists(index_path):
        nav.append({'Index': index_path.replace('docs/', '')})
    for f in get_files_sorted(directory):
        file_path = os.path.join(directory, f)
        h = get_first_heading(file_path)
        nav.append({(h if h else f.replace('.md', '').title()): file_path.replace('docs/', '')})
    return nav

def build_anki_nav():
    """Build navigation for Anki documentation."""
    return [
        {'Anki Decks': 'anki/index.md'},
        {'How to Update': 'anki/updating.md'},
        {'Suspend Extra Cards': 'anki/suspend-extra.md'},
        {'Advanced CSV Update': 'anki/csv-update.md'}
    ]

def build_reference_nav():
    nav = []
    abbrev_path = 'docs/generated/abbreviations.md'
    if os.path.exists(abbrev_path):
        nav.append({'Abbreviations': 'generated/abbreviations.md'})
    
    vocab_dir = 'docs/generated/vocab'
    if os.path.exists(vocab_dir):
        vocab_items = []
        index_path = os.path.join(vocab_dir, 'index.md')
        if os.path.exists(index_path):
            vocab_items.append({'Vocabulary Index': 'generated/vocab/index.md'})
        
        files = [f for f in os.listdir(vocab_dir) if f.endswith('.md') and f != 'index.md']
        def vocab_sort_key(f):
            match = re.search(r'class-(\d+)', f)
            return int(match.group(1)) if match else f
        
        files.sort(key=vocab_sort_key)
        for f in files:
            class_num = int(f.split('-')[1].split('.')[0])
            vocab_items.append({f"Class {class_num}": f"generated/vocab/{f}"})
        if vocab_items:
            nav.append({'Vocabulary': vocab_items})
    return nav


# Pre-processing MD content to handle numbering
def pre_process_content(content):
    # Protect footnotes from being renumbered by the 'footnotes' extension
    # We transform [^12] into a format that the extension won't touch but our JS/PDF script can fix.
    
    # 1. References [^12] -> <sup class="manual-fn-ref" data-fn="12">12</sup>
    content = re.sub(r'\[\^(\d+)\](?!:)', r'<sup class="manual-fn-ref" data-fn="\1">\1</sup>', content)
    
    # 2. Definitions [^12]: text -> <div class="manual-fn-def" data-fn="12">text</div>
    def repl_def(match):
        return f"\n<div class='manual-fn-def' data-fn='{match.group(1)}'>{match.group(2).strip()}</div>\n"
    content = re.sub(r'^\[\^(\d+)\]:\s*(.*)$', repl_def, content, flags=re.MULTILINE)
    
    return content

# Base config
config = {
    'site_name': 'DPD Pāḷi Courses',
    'docs_dir': 'docs',
    'site_dir': 'site',
    'theme': {
        'name': 'material',
        'language': 'en',
        'custom_dir': 'identity',
        'palette': [
            {'media': '(prefers-color-scheme: light)', 'scheme': 'default', 'primary': 'brown', 'accent': 'orange', 'toggle': {'icon': 'material/brightness-7', 'name': 'Switch to dark mode'}},
            {'media': '(prefers-color-scheme: dark)', 'scheme': 'slate', 'primary': 'brown', 'accent': 'orange', 'toggle': {'icon': 'material/brightness-4', 'name': 'Switch to light mode'}}
        ],
        'features': ['navigation.tabs', 'navigation.tabs.sticky', 'navigation.top', 'navigation.indexes', 'content.code.copy', 'hide.generator']
    },
    'extra_css': ['dpd.css', 'dpd-variables.css', 'extra.css'],
    'extra_javascript': ['footnotes.js', 'search_order.js', 'tablesort.min.js', 'tablesort.number.js', 'tablesort_init.js', 'theme-images.js'],
    'markdown_extensions': [
        'attr_list',
        {'toc': {
            'permalink': True,
            'baselevel': 2
        }},
        {'pymdownx.highlight': {'anchor_linenums': True}},
        'pymdownx.inlinehilite',
        'pymdownx.snippets',
        'pymdownx.superfences',
        'tables',
        'md_in_html',
        'nl2br'
        ],
        'hooks': [
        'tools/footnote_hook.py',
        'tools/nav_hook.py'
        ],
        'nav': [

        {'Home': 'index.md'},
        {'About': 'about.md'},
        {'Downloads': 'downloads.md'},
        {'Literature': 'literature.md'},
        {'Beginner Course (BPC)': [{'Lessons': build_class_nav('docs/bpc')}, {'Exercises': build_file_nav('docs/bpc_ex')}, {'Answer Keys': build_file_nav('docs/bpc_key')}]},
        {'Intermediate Course (IPC)': [{'Lessons': build_class_nav('docs/ipc')}, {'Exercises': build_file_nav('docs/ipc_ex')}, {'Answer Keys': build_file_nav('docs/ipc_key')}]},
        {'Study Tools': [{'Anki Decks': build_anki_nav()}]},
        {'Reference': build_reference_nav()}
    ],
    'plugins': ['search']
}

pr.green("Generating mkdocs.yaml")
with open('mkdocs.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, sort_keys=False, allow_unicode=True)
pr.yes("ok")
