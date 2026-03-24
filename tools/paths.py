"""
Centralized path management for the Static Site Generator (SSG) scripts.
"""
from pathlib import Path

class SSGPaths:
    def __init__(self, base_dir: Path = Path(".")):
        self.base_dir = base_dir.resolve()
        self.docs_dir = self.base_dir / "docs"
        self.mkdocs_yaml = self.base_dir / "mkdocs.yaml"
        self.identity_dir = self.base_dir / "identity"
        self.scripts_dir = self.base_dir / "scripts"
        
        # CSS paths (in identity)
        self.extra_css = self.identity_dir / "extra.css"
        self.dpd_variables_css = self.identity_dir / "dpd-variables.css"
        self.dpd_css = self.identity_dir / "dpd.css"
        
        # Source CSS files (same as above for backward compatibility/clarity in update_css)
        self.source_dpd_variables_css = self.dpd_variables_css
        self.source_dpd_css = self.dpd_css
        self.source_extra_css = self.extra_css

        # Output paths for indexes
        self.bpc_index = self.docs_dir / "bpc" / "index.md"
        self.ipc_index = self.docs_dir / "ipc" / "index.md"
