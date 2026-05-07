"""Frontend Skill Helper - Provides Next.js project templates with Jinja2."""

import json
from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class FrontendSkill:
    """Helper for frontend Next.js code generation with dynamic templates."""

    TEMPLATES_FILE = Path(__file__).parent / "frontend_templates.md"

    @staticmethod
    def generate_package_json(project_name: str, version: str = "1.0.0", dependencies: dict = None) -> str:
        """Generate package.json for Next.js project."""
        context = {
            "project_name": project_name,
            "version": version,
            "dependencies": dependencies or {}
        }
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "package_json", context
        )
        return template

    @staticmethod
    def generate_tsconfig() -> str:
        """Generate tsconfig.json for TypeScript."""
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "tsconfig", {}
        )
        return template

    @staticmethod
    def generate_eslint_config() -> str:
        """Generate .eslintrc.json configuration."""
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "eslint_config", {}
        )
        return template

    @staticmethod
    def generate_next_config() -> str:
        """Generate next.config.js."""
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "next_config", {}
        )
        return template

    @staticmethod
    def generate_component_template(
        component_name: str,
        props: list = None,
        state_vars: list = None,
        imports: list = None,
        error_handling: bool = True
    ) -> str:
        """Generate a React component template."""
        component_class_name = "".join([word.capitalize() for word in component_name.split('_')])
        component_kebab = component_name.lower().replace('_', '-')

        context = {
            "component_name": component_class_name,
            "component_name_kebab": component_kebab,
            "props": props or [],
            "state_vars": state_vars or [],
            "imports": imports or [],
            "error_handling": error_handling
        }
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "component_template", context
        )
        return template

    @staticmethod
    def generate_page_template(
        page_name: str,
        use_query: bool = True,
        imports: list = None
    ) -> str:
        """Generate a Next.js page template."""
        page_class_name = "".join([word.capitalize() for word in page_name.split('_')])
        page_name_lower = page_name.lower()

        context = {
            "page_name": page_class_name,
            "page_name_lower": page_name_lower,
            "use_query": use_query,
            "imports": imports or []
        }
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "page_template", context
        )
        return template

    @staticmethod
    def generate_api_service(service_name: str = "api") -> str:
        """Generate API service template."""
        context = {
            "service_name": service_name
        }
        template = JinjaTemplateLoader.render_template(
            str(FrontendSkill.TEMPLATES_FILE), "api_service", context
        )
        return template
