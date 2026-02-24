import unittest
import re
import sys
import os

# Add scripts to path so we can import TableFixer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from clean_docs import TableFixer

class TestSequentialNumbering(unittest.TestCase):
    def setUp(self):
        self.tf = TableFixer()

    def test_lowercase_pali_sentence_extraction(self):
        """
        Targeting 29_class.md: lowercase lines like 'adiṭṭhiyā assutiyā añāṇā,' 
        should be extracted from tables.
        """
        content = """
| adiṭṭhiyā assutiyā añāṇā, | | | | |
|---|---|---|---|---|
| adiṭṭhiyā | noun | fem.instr.sg | without view |
"""
        # File is in no_numbering list
        processed = self.tf.restructure_sentence_analysis(content, "docs/ipc_key/29_class.md")
        
        # Should be extracted, NOT numbered
        self.assertIn("adiṭṭhiyā assutiyā añāṇā,", processed)
        self.assertNotIn("1. adiṭṭhiyā", processed)
        # Should be BEFORE the table
        self.assertTrue(processed.find("adiṭṭhiyā assutiyā añāṇā,") < processed.find("| adiṭṭhiyā |"))

    def test_plus_with_br_bolding(self):
        content = "suvaṇṇa + *a<br>sovaṇṇa + maya"
        processed = self.tf.restructure_sentence_analysis(content, "docs/ipc_key/25_class.md")
        self.assertIn("**suvaṇṇa + *a<br>sovaṇṇa + maya**", processed)
        self.assertNotIn("1. suvaṇṇa", processed)

    def test_sharp_ca_in_table(self):
        content = """
| assādañca | noun | masc.acc.sg | and the satisfaction |
| #assādaṃ | | | |
| ā + √sād + *e + a | | | |
| #ca | | | |
| assādato | noun | masc.abl.sg | as the satisfaction |
"""
        processed = self.tf.restructure_sentence_analysis(content, "docs/ipc_key/23_class.md")
        self.assertNotIn("1. #ca", processed)
        self.assertIn("#ca", processed)

if __name__ == '__main__':
    unittest.main()
