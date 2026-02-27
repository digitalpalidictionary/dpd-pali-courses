import os
import re

# Define mappings from old relative media path to new absolute assets path
# Using exact string replacement to avoid any unintended regex side effects
mappings = {
    'media/3d038928799b8f96c87c5853191f4b18.png': '/assets/images/pacman-backwards.png',
    'media/d56a613230aeb071a406e67d672343ec.png': '/assets/images/pacman-forward.png',
    'media/600cdd2c0fa42269d4d2097fe97305d7.png': '/assets/images/arrow.png',
    'media/b6c1973333da5540209c01b2c66c22b6.png': '/assets/images/kahapana.png',
}

docs_dir = 'docs'

print("Updating media links...")

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.join(root, file)
            
            # Skip processing if we are not in a directory where we expect these links
            # (though the exact string match is already very safe)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            changed = False
            for old_path, new_path in mappings.items():
                if old_path in new_content:
                    new_content = new_content.replace(old_path, new_path)
                    changed = True
            
            if changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {file_path}")

print("Done.")
