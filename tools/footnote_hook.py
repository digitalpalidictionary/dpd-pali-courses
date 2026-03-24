"""
MkDocs hook to pre-process Markdown content before building the website.
Handles footnote protection, list numbering persistence, and multiple newline preservation.
"""
import re
from bs4 import BeautifulSoup

def on_page_markdown(markdown_text, page, config, files):
    """
    Protects source footnote and list markers from renumbering.
    """
    # 1. Protect Footnote Definitions
    def repl_def(m):
        prefix = m.group(1)
        fn_num = m.group(2)
        content = m.group(3).strip()
        return f"\n<div class='manual-fn-def' data-fn='{fn_num}' markdown='1'>\n\n{prefix}{content}\n\n</div>\n\n"
    pattern = r'^([ \t*_]*)\[\^(\d+)\]:\s*(.*?)(?=\n[ \t]*\n|\n[ \t]*[-*_]{3,}|\n[ \t]*#|\n\[\^|\Z)'
    markdown_text = re.sub(pattern, repl_def, markdown_text, flags=re.MULTILINE | re.DOTALL)
    
    # 2. Protect Footnote References
    markdown_text = re.sub(r'\[\^(\d+)\]', r"<sup class='manual-fn-ref' data-fn='\1'>\1</sup>", markdown_text)
    
    # 3. Protect Ordered List Numbering
    # We find "N. " at the start of a line and wrap it in a marker
    def repl_list(m):
        num = m.group(1)
        # We put the marker BEFORE the list item
        return f"\n<div class='manual-list-start' data-start='{num}'></div>\n\n{num}. "
    
    # Use \s+ to handle multiple spaces after the dot
    markdown_text = re.sub(r'^\s*(\d+)\.\s+', repl_list, markdown_text, flags=re.MULTILINE)

    # 4. Preserve multiple newlines by converting empty lines (2+ newlines) to <br>
    # We look for 3 or more newlines (which means at least one truly empty line between paragraphs)
    # and replace them with the appropriate number of <br> tags.
    def repl_newlines(m):
        count = m.group(0).count('\n')
        # A standard paragraph break is \n\n. 
        # For each extra \n, we add a <br>.
        if count > 2:
            return '\n\n' + '<br>\n' * (count - 2)
        return m.group(0)

    markdown_text = re.sub(r'\n{3,}', repl_newlines, markdown_text)
    
    return markdown_text

def on_post_page(output, page, config):
    """
    Post-processes the rendered HTML to fix list numbering.
    """
    if 'manual-list-start' not in output:
        return output
        
    soup = BeautifulSoup(output, 'html.parser')
    for marker in soup.find_all('div', class_='manual-list-start'):
        start_val = marker.get('data-start')
        # Robustly find the next <ol> tag by skipping other markers or empty paragraphs
        next_ol = None
        curr = marker.next_sibling
        while curr:
            if curr.name == 'ol':
                next_ol = curr
                break
            if curr.name and curr.name != 'div' and curr.name != 'p': # stop if we hit another significant block
                # However, Markdown often wraps things in P, so we keep going
                pass
            if curr.name == 'div' and 'manual-list-start' in curr.get('class', []):
                break # Hit another marker
            curr = curr.next_sibling
            
        if next_ol:
            next_ol['start'] = start_val
        # Hide the marker
        marker['style'] = 'display: none;'
        
    return str(soup)
