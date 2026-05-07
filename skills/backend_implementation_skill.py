"""Backend Implementation Skill - Generates fully implemented Spring Boot services."""

from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class BackendImplementationSkill:
    """Generate fully implemented Java services and controllers without TODOs."""

    TEMPLATES_FILE = Path(__file__).parent / "backend_implementation_templates.md"

    @staticmethod
    def generate_crud_service(
        entity_name: str,
        package: str,
        validation_required: bool = True,
        updateable_fields: list = None,
        custom_methods: list = None
    ) -> str:
        """Generate fully implemented CRUD service."""
        context = {
            "entity_name": entity_name,
            "package": package,
            "validation_required": validation_required,
            "updateable_fields": updateable_fields or [],
            "custom_methods": custom_methods or []
        }
        return JinjaTemplateLoader.render_template(
            str(BackendImplementationSkill.TEMPLATES_FILE), "service_crud", context
        )

    @staticmethod
    def generate_rest_api_controller(
        entity_name: str,
        package: str,
        endpoint_path: str = None,
        custom_endpoints: list = None
    ) -> str:
        """Generate fully implemented REST API controller."""
        if endpoint_path is None:
            endpoint_path = entity_name.lower()

        context = {
            "entity_name": entity_name,
            "package": package,
            "endpoint_path": endpoint_path,
            "custom_endpoints": custom_endpoints or []
        }
        return JinjaTemplateLoader.render_template(
            str(BackendImplementationSkill.TEMPLATES_FILE), "controller_rest_api", context
        )

    @staticmethod
    def generate_entity_with_validation(
        entity_name: str,
        table_name: str,
        package: str,
        fields: list = None,
        description: str = None
    ) -> str:
        """Generate entity with validation annotations."""
        context = {
            "entity_name": entity_name,
            "table_name": table_name,
            "package": package,
            "fields": fields or [],
            "description": description
        }
        return JinjaTemplateLoader.render_template(
            str(BackendImplementationSkill.TEMPLATES_FILE), "entity_with_validation", context
        )
