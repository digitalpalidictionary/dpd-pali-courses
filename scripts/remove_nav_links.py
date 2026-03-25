"""
Script to remove <div class="nav-links">...</div> blocks from Markdown files.
This ensures Markdown sources are clean and focused on content, as required.
Navigation should be handled via MkDocs hooks or custom themes instead.
"""
import os
import re

def remove_nav_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match the <div class="nav-links"> block and everything inside it
    nav_pattern = re.compile(r'\n*<div class="nav-links">.*?</div>\s*', re.DOTALL)
    content = nav_pattern.sub('\n', content)
    
    # Match the <div class="feedback"> block and everything inside it
    feedback_pattern = re.compile(r'\n*<div class="feedback">.*?</div>\s*', re.DOTALL)
    content = feedback_pattern.sub('\n', content)

    # Aggressively remove any remaining </div> or </div> tags at the very end of the file
    # specifically if they are sitting alone after the content.
    while True:
        new_content = re.sub(r'\s*</div>\s*$', '', content, flags=re.MULTILINE)
        if new_content == content:
            break
        content = new_content
    
    if content != content: # This logic is slightly flawed in the previous turn, let's fix it
        pass
    
    # Let's just compare new vs old
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    if content.strip() != original_content.strip():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')
        return True
    return False

def main():
    docs_dir = 'docs'
    files_affected = 0
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                if remove_nav_links(path):
                    files_affected += 1
                    print(f"Removed nav links from {path}")
                    
    print(f"\nTotal files affected: {files_affected}")

if __name__ == '__main__':
    main()
