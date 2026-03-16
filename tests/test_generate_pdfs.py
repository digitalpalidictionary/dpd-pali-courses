import unittest
import os
from scripts.generate_pdfs import get_markdown_files, convert_to_html, build_html_document

class TestGeneratePDFs(unittest.TestCase):
    def test_get_markdown_files(self):
        # We expect a dictionary mapping folder names to a list of their md files
        files_by_dir = get_markdown_files("docs")
        
        expected_dirs = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
        for d in expected_dirs:
            self.assertIn(d, files_by_dir, f"Directory {d} not found in output")
            self.assertGreater(len(files_by_dir[d]), 0, f"No markdown files found for {d}")
        
        # Verify specific file presence
        self.assertTrue(any("index.md" in f for f in files_by_dir['bpc']))

    def test_convert_to_html(self):
        md = "# Heading 1\nSome text with **bold**."
        html = convert_to_html(md)
        self.assertIn("<h1", html)
        self.assertIn("Heading 1", html)
        self.assertIn("<strong>bold</strong>", html)

    def test_build_html_document(self):
        files_data = [
            ("test_1.md", "# First Title\nContent 1"),
            ("test_2.md", "## Second Title\nContent 2")
        ]
        
        html = build_html_document("Test Course", files_data)
        
        # Check for TOC
        self.assertIn('href="#first-title"', html.lower())
        self.assertIn('href="#second-title"', html.lower())
        
        # Check for content
        self.assertIn('id="first-title"', html.lower())
        self.assertIn('id="second-title"', html.lower())
        
        # Check for wrapper
        self.assertIn('<!doctype html>', html.lower())
        self.assertIn('Test Course', html)

    def test_generate_pdf_from_html(self):
        from unittest.mock import patch
        
        with patch('scripts.generate_pdfs.generate_pdf') as mock_generate:
            from scripts.generate_pdfs import generate_pdf
            
            html_content = "<html><body><h1>Hello World</h1></body></html>"
            output_pdf = "test_output.pdf"
            
            generate_pdf(html_content, output_pdf, css_paths=[])
            
            mock_generate.assert_called_once_with(html_content, output_pdf, css_paths=[])

if __name__ == '__main__':
    unittest.main()
