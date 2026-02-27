import os
import re

# Define mappings from old relative media path to new absolute assets path
mappings = {
    r'media/3d038928799b8f96c87c5853191f4b18\.png': '/assets/images/pacman-backwards.png',
    r'media/d56a613230aeb071a406e67d672343ec\.png': '/assets/images/pacman-forward.png',
    r'media/600cdd2c0fa42269d4d2097fe97305d7\.png': '/assets/images/arrow.png',
    r'media/b6c1973333da5540209c01b2c66c22b6\.png': '/assets/images/kahapana.png',
}

docs_dir = 'docs'

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old_path, new_path in mappings.items():
                new_content = re.sub(old_path, new_path, new_content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {file_path}")
