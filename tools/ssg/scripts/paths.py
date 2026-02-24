from pathlib import Path

class SSGPaths:
    def __init__(self, base_dir: Path = Path(".")):
        self.base_dir = base_dir.resolve()
        self.docs_dir = self.base_dir / "docs"
        self.mkdocs_yaml = self.base_dir / "mkdocs.yaml"
        self.tools_ssg_dir = self.base_dir / "tools" / "ssg"
        self.scripts_dir = self.tools_ssg_dir / "scripts"
        self.assets_dir = self.tools_ssg_dir / "assets"
        
        # CSS paths (new location)
        self.stylesheets_dir = self.tools_ssg_dir / "stylesheets"
        self.extra_css = self.stylesheets_dir / "extra.css"
        self.dpd_variables_css = self.stylesheets_dir / "dpd-variables.css"
        self.dpd_css = self.stylesheets_dir / "dpd.css"
        
        # Source assets (to be copied from website_example or created)
        self.source_assets_dir = self.assets_dir
        self.source_dpd_variables_css = self.source_assets_dir / "dpd-variables.css"
        self.source_dpd_css = self.source_assets_dir / "dpd.css"
        self.source_extra_css = self.source_assets_dir / "extra.css"
