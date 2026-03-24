
"""
MkDocs hook to automatically generate navigation buttons (Prev, Next, Exercises, Feedback).
Allows removal of hardcoded navigation HTML from Markdown source files.
"""
import os
import re
from mkdocs.utils import get_relative_url

def on_page_markdown(markdown, page, config, files):
    """
    Remove hardcoded nav-links from markdown if they exist.
    They will be re-added in HTML during on_post_page.
    """
    # Remove <div class="nav-links">...</div>
    # Using re.DOTALL to match across newlines
    markdown = re.sub(r'<div class="nav-links">.*?</div>\s*$', '', markdown, flags=re.DOTALL)
    return markdown

def on_post_page(output, page, config):
    """
    Append navigation buttons to the bottom of the page.
    """
    # Skip for index pages if desired, or handle differently.
    # Usually, we want them everywhere.
    
    # 1. Get Previous and Next page from MkDocs internal nav
    prev_page = page.previous_page
    next_page = page.next_page
    
    nav_html = '<div class="nav-links">\n'
    
    # Prev button
    if prev_page:
        prev_url = get_relative_url(prev_page.url, page.url)
        # Try to get a nice label from title
        label = prev_page.title if prev_page.title else "Previous"
        nav_html += f'  <a href="{prev_url}" class="prev">← {label}</a>\n'
    
    # Next button
    if next_page:
        next_url = get_relative_url(next_page.url, page.url)
        label = next_page.title if next_page.title else "Next"
        nav_html += f'  <a href="{next_url}" class="next">{label} →</a>\n'

    # Cross-link to Exercises if applicable
    # We can detect if we are in bpc/class_X and link to bpc_ex/X_class.md
    # Or use metadata from the page if available.
    
    # Logic for DPD courses specifically:
    # If path is docs/bpc/class_N/something.md -> Exercises are bpc_ex/N_class.md
    match = re.search(r'bpc/class_(\d+)', page.file.src_path)
    if match:
        class_num = match.group(1)
        ex_url = get_relative_url(f"bpc_ex/{class_num}_class/", page.url)
        nav_html += f'  <div class="cross"><a href="{ex_url}">Go to Exercises</a></div>\n'
    
    match_ipc = re.search(r'ipc/class_(\d+)', page.file.src_path)
    if match_ipc:
        class_num = match_ipc.group(1)
        ex_url = get_relative_url(f"ipc_ex/{class_num}_class/", page.url)
        nav_html += f'  <div class="cross"><a href="{ex_url}">Go to Exercises</a></div>\n'

    # Feedback link
    # We can construct the Google Form link with pre-filled path
    form_base = "https://docs.google.com/forms/d/e/1FAIpQLSeCZ01pgGSYZDO7c1p7L5ciQfg1gEPIEx1g0RgPaCxSY_fQcg/viewform"
    entry_course = "entry.957833742"
    entry_page = "entry.390426412"
    
    course_name = "Beginner Pāḷi Course (BPC)" if "bpc" in page.file.src_path else "Intermediate Pāḷi Course (IPC)"
    page_path = page.file.src_path.replace(".md", "")
    
    import urllib.parse
    params = {
        entry_course: course_name,
        entry_page: page_path
    }
    feedback_url = f"{form_base}?{urllib.parse.urlencode(params)}"
    
    nav_html += f'  <div class="feedback"><a href="{feedback_url}" target="_blank">Provide feedback on this page</a></div>\n'
    nav_html += '</div>'
    
    # Insert before </body> or just append
    if '</body>' in output:
        return output.replace('</body>', f'{nav_html}</body>')
    else:
        # For snippets or partials, just append
        return output + nav_html
