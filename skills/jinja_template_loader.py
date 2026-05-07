"""Jinja2 Template Loader - Renders templates with dynamic variables."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import re


class JinjaTemplateLoader:
    """Load and render Jinja2 templates from markdown files."""

    _env = None
    _templates_cache = {}

    @classmethod
    def _init_env(cls, template_dir: str):
        """Initialize Jinja2 environment."""
        if cls._env is None:
            cls._env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )

    @staticmethod
    def extract_code_block(markdown_content: str, block_name: str) -> str:
        """Extract code from markdown code block by name."""
        pattern = rf'<!-- {block_name} -->(.*?)<!-- /{block_name} -->'
        match = re.search(pattern, markdown_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"Code block '{block_name}' not found in markdown")

    @classmethod
    def load_template_content(cls, markdown_file: str, block_name: str) -> str:
        """Load raw template content from markdown file."""
        path = Path(markdown_file)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return cls.extract_code_block(content, block_name)

    @classmethod
    def render_template(cls, markdown_file: str, block_name: str, context: dict = None) -> str:
        """Render template with Jinja2."""
        if context is None:
            context = {}

        # Load raw template content
        template_content = cls.load_template_content(markdown_file, block_name)

        # Remove markdown code block markers
        template_content = re.sub(r'```\w+\n', '', template_content)
        template_content = template_content.replace('```', '')

        # Create Jinja2 template from string
        from jinja2 import Template
        template = Template(template_content)

        # Render with context
        return template.render(context)

    @classmethod
    def render_simple(cls, markdown_file: str, block_name: str, **kwargs) -> str:
        """Simple render with keyword arguments."""
        return cls.render_template(markdown_file, block_name, kwargs)
