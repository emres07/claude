"""Frontend Implementation Skill - Generates fully implemented React components."""

from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class FrontendImplementationSkill:
    """Generate fully implemented React components without TODOs."""

    TEMPLATES_FILE = Path(__file__).parent / "frontend_implementation_templates.md"

    @staticmethod
    def generate_add_form_component(
        component_name: str,
        fields: list,
        api_endpoint: str,
        form_title: str = None,
        submit_button_text: str = "Save",
        imports: list = None
    ) -> str:
        """Generate fully implemented Add/Create form component."""
        context = {
            "component_name": component_name,
            "component_name_kebab": component_name.lower().replace('_', '-'),
            "fields": fields,  # [{name, label, type, placeholder, required, input_type}]
            "api_endpoint": api_endpoint,
            "form_title": form_title or component_name,
            "submit_button_text": submit_button_text,
            "imports": imports or []
        }
        return JinjaTemplateLoader.render_template(
            str(FrontendImplementationSkill.TEMPLATES_FILE), "component_add_form", context
        )

    @staticmethod
    def generate_list_component(
        component_name: str,
        api_endpoint: str,
        endpoint_singular: str,
        display_fields: list,
        list_title: str = None,
        imports: list = None
    ) -> str:
        """Generate fully implemented List/Table component."""
        context = {
            "component_name": component_name,
            "component_name_kebab": component_name.lower().replace('_', '-'),
            "api_endpoint": api_endpoint,
            "endpoint_singular": endpoint_singular,
            "display_fields": display_fields,  # [{name, label}]
            "list_title": list_title or component_name,
            "imports": imports or []
        }
        return JinjaTemplateLoader.render_template(
            str(FrontendImplementationSkill.TEMPLATES_FILE), "component_list", context
        )

    @staticmethod
    def generate_crud_page(
        page_name: str,
        form_component: str,
        list_component: str,
        page_title: str = None
    ) -> str:
        """Generate fully implemented CRUD operations page."""
        context = {
            "page_name": "".join([word.capitalize() for word in page_name.split('_')]),
            "page_name_lower": page_name.lower(),
            "form_component": form_component,
            "list_component": list_component,
            "page_title": page_title or page_name,
            "uses_form": True,
            "uses_list": True,
            "mode_edit_check": True
        }
        return JinjaTemplateLoader.render_template(
            str(FrontendImplementationSkill.TEMPLATES_FILE), "page_crud", context
        )

    @staticmethod
    def generate_use_api_hook() -> str:
        """Generate custom React hook for API operations."""
        return JinjaTemplateLoader.render_template(
            str(FrontendImplementationSkill.TEMPLATES_FILE), "hook_use_api", {}
        )
