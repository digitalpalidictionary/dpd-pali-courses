
"""
Unit tests for the sutta alignment logic used in add_sutta_links.py.
"""
import unittest
import re

def add_sutta_links_logic(content):
    # Regex to match sutta references.
    # Patterns observed:
    # [SN12.61](...)
    # [VIN PAT SA 10](...)
    # [SNP13](...) (modif)
    # *[AN8.53](...)*
    # *VIN PAT NID* *modified*
    
    # We look for lines starting with typical prefixes: AN, SN, MN, DN, DHP, SNP, VIN, KHP, etc.
    # They might be wrapped in [] or ** or *
    
    lines = content.split('\n')
    new_lines = []
    
    # Prefix list
    prefixes = ['AN', 'SN', 'MN', 'DN', 'DHP', 'SNP', 'VIN', 'KHP', 'ITI', 'UD', 'Vism']
    prefix_pattern = '|'.join(prefixes)
    
    # Regex explanation:
    # ^\s*          - start of line and optional whitespace
    # [\[\*\_]*     - optional opening markdown characters [, *, _
    # (?:{prefix_pattern}) - one of the sutta prefixes
    # .*            - the rest of the reference
    # $             - end of line
    sutta_line_regex = re.compile(rf'^\s*[\[\*\_]*(?:{prefix_pattern})', re.IGNORECASE)
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Avoid processing nav-links or headings
        if sutta_line_regex.match(line) and not line.startswith('#') and 'nav-links' not in line:
            # Found a sutta reference line.
            # Wrap it in <div class="align-right">
            
            # Ensure we don't wrap it twice if already wrapped
            if '<div class="align-right">' not in line:
                # Prepare the line
                clean_line = line.strip()
                wrapped_line = f'<div class="align-right">\n\n{clean_line}\n\n</div>'
                
                # Check if previous line is empty, if not add one
                if new_lines and new_lines[-1].strip() != '':
                    new_lines.append('')
                
                new_lines.append(wrapped_line)
                
                # Check if next line is empty, if not add one (handled in next iteration or end)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1

    # Final pass to ensure spacing
    final_content = '\n'.join(new_lines)
    # Ensure no triple newlines
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
    return final_content

class TestSuttaLinks(unittest.TestCase):
    def test_basic_link(self):
        content = "Sentence 1.\n\n[SN12.61](https://example.com)\n\nSentence 2."
        expected = "Sentence 1.\n\n<div class=" + '"align-right"' + ">\n\n[SN12.61](https://example.com)\n\n</div>\n\nSentence 2."
        self.assertEqual(add_sutta_links_logic(content), expected)

    def test_italic_link(self):
        content = "Sentence 1.\n\n*[AN8.53](https://example.com)*\n\nSentence 2."
        expected = "Sentence 1.\n\n<div class=" + '"align-right"' + ">\n\n*[AN8.53](https://example.com)*\n\n</div>\n\nSentence 2."
        self.assertEqual(add_sutta_links_logic(content), expected)

    def test_vinaya_no_link(self):
        content = "Sentence 1.\n\n*VIN PAT NID* *modified*\n\nSentence 2."
        expected = "Sentence 1.\n\n<div class=" + '"align-right"' + ">\n\n*VIN PAT NID* *modified*\n\n</div>\n\nSentence 2."
        self.assertEqual(add_sutta_links_logic(content), expected)

    def test_no_extra_space(self):
        content = "Sentence 1.\n[SN12.61](https://example.com)\nSentence 2."
        # Should add empty lines
        expected = "Sentence 1.\n\n<div class=" + '"align-right"' + ">\n\n[SN12.61](https://example.com)\n\n</div>\n\nSentence 2."
        self.assertEqual(add_sutta_links_logic(content), expected)

if __name__ == "__main__":
    unittest.main()
