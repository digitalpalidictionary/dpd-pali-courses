import unittest
import sys
import os

# Ensure the script directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.clean_docs import TableFixer

class TestTableFixer(unittest.TestCase):
    def setUp(self):
        self.tf = TableFixer()

    def test_merge_fragment_into_preceding_table(self):
        content = """12. SN 22.3 <br>evaṃrūpo siyaṃ anāgatamaddhānaṃ

|  |  |  |  |  |
|---|---|---|---|---|
| evaṃrūpo |  |  |  |  |
| siyaṃ |  |  |  |  |

**&nbsp;**


13. anāgatam’<br>addhānaṃ

**&nbsp;**


14. MN 10.16<br>aho vata mayaṃ na maraṇadhammā assāma
"""
        fixed = self.tf.restructure_sentence_analysis(content, "docs/bpc_ex/7_class.md")
        
        self.assertIn("| evaṃrūpo |", fixed)
        self.assertIn("| siyaṃ |", fixed)
        self.assertIn("| anāgatam’<br>addhānaṃ |", fixed)
        self.assertIn("1. SN 22.3", fixed)
        self.assertIn("2. MN 10.16", fixed)
        # Ensure it's not a standalone numbered item
        self.assertNotIn("\n2. anāgatam’", fixed)

    def test_handle_marker_row_in_table(self):
        content = """1. MN 152 <br>jivhāya rasaṃ sāyitvā uppajjati manāpaṃ

|  |  |  |  |  |
|---|---|---|---|---|
| jivhāya | n | f.instr.s | by the t |  |
| ** ** |  |  |  |  |
"""
        fixed = self.tf.restructure_sentence_analysis(content, "docs/bpc_ex/7_class.md")
        self.assertNotIn("| ** ** |", fixed)
        self.assertIn("**&nbsp;**", fixed) # It gets normalized to &nbsp; by finalize_block

if __name__ == "__main__":
    unittest.main()
