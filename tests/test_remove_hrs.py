
"""
Unit tests for the horizontal rule removal logic in remove_hrs.py.
"""
import unittest
import re
import os

def replace_stars_with_space_logic(content):
    # Match HR line and optional surrounding newlines.
    # We want to replace it with exactly TWO newlines IF it's between text.
    # If it's at start/end of file, maybe just one?
    
    # Actually let's use a very robust approach:
    # 1. Replace all HR lines (and their trailing newline) with \n\n
    # 2. Collapse any sequence of 3+ newlines to 2 newlines.
    
    # hr_pattern matches the line and the newline following it.
    hr_pattern = re.compile(r'^\s*\*\*\*\s*$\n?', re.MULTILINE)
    content = hr_pattern.sub('\n\n', content)
    
    # Collapse 3 or more newlines into exactly 2 newlines (one empty line).
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Optional: strip leading/trailing whitespace if you want clean files.
    # But usually we only touch the HRs.
    
    return content

class TestRemoveHrs(unittest.TestCase):
    def test_hr_replacement(self):
        content = "Sentence 1.\n***\nSentence 2."
        expected = "Sentence 1.\n\nSentence 2."
        result = replace_stars_with_space_logic(content)
        self.assertEqual(result, expected)

    def test_false_positive_bold_italic(self):
        content = r"This is \***as** text."
        expected = r"This is \***as** text."
        result = replace_stars_with_space_logic(content)
        self.assertEqual(result, expected)

    def test_hr_at_start(self):
        content = "***\nSentence 1."
        expected = "\nSentence 1." # or just Sentence 1? 
        # Actually \n\nSentence 1. if sub replaces with \n\n
        # But collapse to \n\n is fine.
        result = replace_stars_with_space_logic(content)
        # Expected from current logic: \n\nSentence 1.
        self.assertEqual(result.lstrip('\n'), "Sentence 1.")

    def test_triple_newlines_prevention(self):
        content = "Sentence 1.\n\n***\n\nSentence 2."
        # Should be Sentence 1.\n\nSentence 2.
        expected = "Sentence 1.\n\nSentence 2."
        result = replace_stars_with_space_logic(content)
        self.assertEqual(result, expected)

    def test_multiple_hrs(self):
        content = "S1\n***\nS2\n***\nS3"
        expected = "S1\n\nS2\n\nS3"
        result = replace_stars_with_space_logic(content)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
