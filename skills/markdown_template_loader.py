"""Markdown Template Loader - Reads code templates from markdown files."""

import re
from pathlib import Path


class MarkdownTemplateLoader:
    """Load code templates from markdown code blocks."""

    @staticmethod
    def extract_code_block(markdown_content: str, block_name: str) -> str:
        """Extract code from markdown code block by name."""
        # Pattern: <!-- block_name --> ... <!-- /block_name -->
        pattern = rf'<!-- {block_name} -->(.*?)<!-- /{block_name} -->'
        match = re.search(pattern, markdown_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"Code block '{block_name}' not found in markdown")

    @staticmethod
    def load_template(markdown_file: str, block_name: str) -> str:
        """Load template from markdown file."""
        path = Path(markdown_file)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return MarkdownTemplateLoader.extract_code_block(content, block_name)
