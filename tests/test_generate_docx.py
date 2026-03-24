import unittest
import unittest.mock
import os
import re
from scripts.generate_docx import get_markdown_files, clean_markdown_content, generate_docx

class TestGenerateDocx(unittest.TestCase):
    def test_get_markdown_files(self):
        """Test that get_markdown_files returns a dictionary with the expected folders."""
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            self.skipTest("docs directory not found")
        
        f_by_dir = get_markdown_files(docs_dir)
        expected_folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
        for folder in expected_folders:
            self.assertIn(folder, f_by_dir)
            self.assertIsInstance(f_by_dir[folder], list)

    def test_clean_markdown_content(self):
        """Test that clean_markdown_content removes UI elements."""
        content = """
# Title
<div class="nav-links"><a href="prev.md">Prev</a></div>
Some text.
<div class="feedback">Feedback</div>
<a class="next" href="next.md">Next</a>
"""
        cleaned = clean_markdown_content(content)
        self.assertNotIn('nav-links', cleaned)
        self.assertNotIn('feedback', cleaned)
        self.assertNotIn('class="next"', cleaned)
        self.assertIn('# Title', cleaned)
        self.assertIn('Some text.', cleaned)

    def test_generate_docx(self):
        """Test generating a simple .docx file."""
        md_text = "# Test Title\nThis is a test paragraph."
        output_file = "test_output.docx"
        if os.path.exists(output_file):
            os.remove(output_file)
            
        try:
            generate_docx(md_text, output_file)
            self.assertTrue(os.path.exists(output_file))
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_fix_internal_links(self):
        """Test that fix_internal_links converts .md links to internal bookmarks."""
        from scripts.generate_docx import fix_internal_links
        content = '[Link](class_1/topic.md#anchor) and [External](http://google.com)'
        fixed = fix_internal_links(content)
        self.assertIn('#topic_md', fixed)
        self.assertIn('http://google.com', fixed)

    def test_main_with_data(self):
        """Test the main function with mock data."""
        from scripts.generate_docx import main
        mock_files = {'bpc': ['docs/bpc/class_1/index.md', 'docs/bpc/class_1/1_intro.md']}
        
        with unittest.mock.patch('scripts.generate_docx.get_markdown_files', return_value=mock_files):
            with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data="# Content")):
                with unittest.mock.patch('os.path.exists', return_value=True):
                    with unittest.mock.patch('scripts.generate_docx.generate_docx') as mock_gen:
                        # Patch argparse
                        with unittest.mock.patch('argparse.ArgumentParser.parse_args', return_value=unittest.mock.Namespace(folder=None)):
                            main()
                            mock_gen.assert_called()

    def test_aggregate_markdown(self):
        """Test the aggregation logic."""
        from scripts.generate_docx import aggregate_markdown
        files_data = [('class_1/topic.md', '# Topic 1\nContent 1'), ('class_2/topic.md', '# Topic 2\nContent 2')]
        aggregated = aggregate_markdown("Test Course", files_data, about_content="About", lit_content="Literature")
        self.assertIn('# Test Course', aggregated)
        self.assertIn('About', aggregated)
        self.assertIn('Literature', aggregated)
        self.assertIn('# Topic 1', aggregated)
        self.assertIn('# Topic 2', aggregated)
        self.assertIn('[]{#topic_md}', aggregated)

    def test_empty_aggregation(self):
        """Test aggregation with no files."""
        from scripts.generate_docx import aggregate_markdown
        aggregated = aggregate_markdown("Empty", [])
        self.assertEqual(aggregated, "# Empty\n\n")

if __name__ == '__main__':
    unittest.main()
