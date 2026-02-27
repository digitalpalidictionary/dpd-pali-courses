import os
import yaml

def get_files_sorted(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.md') and f != 'index.md']
    # Extract number for sorting if possible, handle strings gracefully
    def sort_key(f):
        parts = f.split('_')
        if parts[0].isdigit():
            return (0, int(parts[0]))
        return (1, f)
    return sorted(files, key=sort_key)

def get_class_folders(directory):
    folders = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and d.startswith('class_')]
    return sorted(folders, key=lambda x: int(x.split('_')[1]))

def build_class_nav(base_dir):
    folders = get_class_folders(base_dir)
    nav = []
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        label = f"Class {folder.split('_')[1]}"
        items = []
        # Index first, strip 'docs/' prefix for mkdocs.yaml
        items.append(os.path.join(base_dir, folder, 'index.md').replace('docs/', ''))
        for f in get_files_sorted(folder_path):
            file_label = f.replace('.md', '').replace('_', ' ').title()
            items.append({file_label: os.path.join(base_dir, folder, f).replace('docs/', '')})
        nav.append({label: items})
    return nav

def build_file_nav(directory):
    nav = []
    nav.append(os.path.join(directory, 'index.md').replace('docs/', ''))
    for f in get_files_sorted(directory):
        label = f.replace('.md', '').replace('_', ' ').title()
        nav.append({label: os.path.join(directory, f).replace('docs/', '')})
    return nav

# Base config
config = {
    'site_name': 'DPD Pāḷi Courses',
    'docs_dir': 'docs',
    'site_dir': 'site',
    'theme': {
        'name': 'material',
        'language': 'en',
        'custom_dir': 'tools/ssg/stylesheets',
        'palette': [
            {
                'scheme': 'default',
                'primary': 'brown',
                'accent': 'orange',
                'toggle': {'icon': 'material/brightness-7', 'name': 'Switch to dark mode'}
            },
            {
                'scheme': 'slate',
                'primary': 'brown',
                'accent': 'orange',
                'toggle': {'icon': 'material/brightness-4', 'name': 'Switch to light mode'}
            }
        ],
        'features': [
            'navigation.tabs',
            'navigation.tabs.sticky',
            'navigation.top',
            'navigation.indexes',
            'content.code.copy'
        ]
    },
    'extra_css': ['dpd.css', 'dpd-variables.css', 'extra.css'],
    'markdown_extensions': [
        'attr_list',
        {'pymdownx.highlight': {'anchor_linenums': True}},
        'pymdownx.inlinehilite',
        'pymdownx.snippets',
        'pymdownx.superfences',
        'tables'
    ],
    'nav': [
        {'Home': 'index.md'},
        {'Beginner Course (BPC)': [
            {'Introduction': [
                {'BPC Home': 'bpc/index.md'},
                {'Title Page': 'bpc/0.1_title.md'},
                {'Literature': 'bpc/0.2_literature.md'},
                {'Table of Contents': 'bpc/0.3_content.md'}
            ]},
            {'Lessons': build_class_nav('docs/bpc')},
            {'Exercises': build_file_nav('docs/bpc_ex')},
            {'Answer Keys': build_file_nav('docs/bpc_key')}
        ]},
        {'Intermediate Course (IPC)': [
            {'Introduction': [
                {'IPC Home': 'ipc/index.md'},
                {'Title Page': 'ipc/0.1_title.md'},
                {'Table of Contents': 'ipc/0.2_content.md'}
            ]},
            {'Lessons': build_class_nav('docs/ipc')},
            {'Exercises': build_file_nav('docs/ipc_ex')},
            {'Answer Keys': build_file_nav('docs/ipc_key')}
        ]}
    ],
    'plugins': ['search']
}

# Dump to file
with open('mkdocs.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, sort_keys=False, allow_unicode=True)
