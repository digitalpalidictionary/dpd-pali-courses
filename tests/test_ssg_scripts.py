import unittest
import shutil
import tempfile
import yaml
from pathlib import Path
from tools.ssg.scripts.generate_indexes import main as generate_indexes
from tools.ssg.scripts.update_css import update_css
from tools.ssg.scripts.paths import SSGPaths

class TestSSGScripts(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the test
        self.test_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.test_dir / "docs"
        self.docs_dir.mkdir()
        (self.docs_dir / "stylesheets").mkdir()
        
        # Create dummy source CSS
        self.assets_dir = self.test_dir / "tools" / "ssg" / "assets"
        self.assets_dir.mkdir(parents=True)
        (self.assets_dir / "dpd-variables.css").write_text(":root { --primary-color: #123456; }")
        
        # Create subdirectories and dummy markdown files
        self.bpc_dir = self.docs_dir / "bpc"
        self.bpc_dir.mkdir()
        self.class1_dir = self.bpc_dir / "class_1"
        self.class1_dir.mkdir()
        (self.class1_dir / "1_intro.md").write_text("# Intro\n")
        (self.class1_dir / "2_lesson.md").write_text("# Lesson\n")
        (self.class1_dir / "index.md").write_text("# Class 1 Index\n")
        
        # Mock mkdocs.yaml
        self.mkdocs_yaml = self.test_dir / "mkdocs.yaml"
        config = {
            "nav": [
                {"Beginner Course (BPC)": [
                    "bpc/class_1/index.md",
                    "bpc/class_1/1_intro.md",
                    "bpc/class_1/2_lesson.md"
                ]}
            ]
        }
        with open(self.mkdocs_yaml, "w") as f:
            yaml.dump(config, f)
            
        self.paths = SSGPaths(self.test_dir)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_generate_indexes(self):
        # Run the generation script
        generate_indexes(self.paths)
        
        # Verify index.md was updated
        index_path = self.class1_dir / "index.md"
        content = index_path.read_text()
        
        self.assertIn("1. [Intro](1_intro.md)", content)
        self.assertIn("1. [Lesson](2_lesson.md)", content)

    def test_update_css(self):
        # Run the update script
        update_css(self.paths)
        
        # Verify CSS was updated in tools/ssg/stylesheets folder
        css_path = self.test_dir / "tools" / "ssg" / "stylesheets" / "dpd-variables.css"
        self.assertTrue(css_path.exists())
        content = css_path.read_text()
        self.assertIn("--primary-color", content)

if __name__ == "__main__":
    unittest.main()
