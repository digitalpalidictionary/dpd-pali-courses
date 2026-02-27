import os

def get_nav_items(directory):
    items = []
    # Sort files to ensure 1_, 2_ etc are in order
    files = sorted([f for f in os.listdir(directory) if f.endswith('.md') and f != 'index.md'])
    for f in files:
        label = f.replace('.md', '').replace('_', ' ').title()
        # Keep it simple for mkdocs: list of {label: path}
        items.append({label: os.path.join(directory, f)})
    return items

def generate_class_nav(base_dir):
    classes = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('class_')], 
                     key=lambda x: int(x.split('_')[1]))
    nav = []
    for cls in classes:
        cls_dir = os.path.join(base_dir, cls)
        cls_label = f"Class {cls.split('_')[1]}"
        items = get_nav_items(cls_dir)
        # Put index.md first as the main class page
        nav_entry = {cls_label: [os.path.join(cls_dir, 'index.md')] + items}
        nav.append(nav_entry)
    return nav

import json
print("BPC CLASSES:")
print(json.dumps(generate_class_nav('docs/bpc'), indent=2))

print("\nIPC CLASSES:")
print(json.dumps(generate_class_nav('docs/ipc'), indent=2))
