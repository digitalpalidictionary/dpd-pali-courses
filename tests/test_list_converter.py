import unittest
import sys
import os

# Ensure the script directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.clean_docs import TableFixer

class TestListConverter(unittest.TestCase):
    def setUp(self):
        self.tf = TableFixer()

    def test_convert_flat_list_to_table(self):
        # This input simulates the block from docs/bpc_ex/6_class.md
        input_text = """4. VIN PAT SA 12 <br>“mā maṃ āyasmanto kiñci avacuttha kalyāṇaṃ vā pāpakaṃ vā”

mā

maṃ

āyasmanto

kiñci

pron

nt.acc.sg

avacuttha

kalyāṇaṃ

adj

vā

pāpakaṃ

adj

vā
"""
        
        result = self.tf.restructure_sentence_analysis(input_text, 'docs/bpc_ex/6_class.md')
        
        # Check that the table has the correct number of rows for each word, including duplicates
        self.assertEqual(result.count("| vā |"), 2)
        self.assertIn("| kiñci | pron | nt.acc.sg |", result)
        self.assertIn("| pāpakaṃ | adj |", result)
        
        # Ensure original flat list items are gone
        self.assertNotIn("\nmaṃ\n", result)
        self.assertNotIn("\npron\n", result)

if __name__ == "__main__":
    unittest.main()
