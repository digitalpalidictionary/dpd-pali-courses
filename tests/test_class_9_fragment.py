import unittest
import sys
import os

# Ensure the script directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.clean_docs import TableFixer

class TestTableFixerClass9(unittest.TestCase):
    def setUp(self):
        self.tf = TableFixer()

    def test_merge_ki_nu_kho_fragment(self):
        content = """14. MN 38 <br>ahesumha nu kho mayaṃ atītam'addhānaṃ

|  |  |  |  |  |
|---|---|---|---|---|
| ahesumha |  |  |  |  |
| nu kho |  |  |  |  |

**&nbsp;**


15. kiṃ nu kho

|  |  |  |  |  |
|---|---|---|---|---|
| ahesumha |  |  |  |  |
"""
        fixed = self.tf.restructure_sentence_analysis(content, "docs/bpc_ex/9_class.md")
        
        # It should merge "kiṃ nu kho" into the first table and NOT start a new exercise 15
        self.assertIn("| kiṃ nu kho |", fixed)
        self.assertNotIn("15. kiṃ nu kho", fixed)
        # There should only be one exercise number 1. (since we start from 0)
        self.assertIn("1. MN 38", fixed)

if __name__ == "__main__":
    unittest.main()
