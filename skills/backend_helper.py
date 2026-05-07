"""Backend Skill Helper - Provides Spring Boot project templates with Jinja2."""

from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class BackendSkill:
    """Helper for backend Spring Boot code generation with dynamic templates."""

    TEMPLATES_FILE = Path(__file__).parent / "backend_templates.md"

    @staticmethod
    def generate_pom_xml(
        project_name: str,
        artifact_id: str = None,
        group_id: str = "com.example",
        version: str = "1.0.0",
        add_security: bool = False,
        additional_dependencies: list = None
    ) -> str:
        """Generate Maven pom.xml for Spring Boot project."""
        if artifact_id is None:
            artifact_id = project_name.lower().replace(' ', '-')

        context = {
            "project_name": project_name,
            "artifact_id": artifact_id,
            "group_id": group_id,
            "version": version,
            "add_security": add_security,
            "additional_dependencies": additional_dependencies or []
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "pom_xml", context
        )
        return template

    @staticmethod
    def generate_application_yml(
        project_name: str = "Calendar App",
        db_url: str = "jdbc:oracle:thin:@localhost:1521:xe",
        db_user: str = "calendar_app",
        db_password: str = "welcome123",
        server_port: int = 8080,
        package: str = "com.example.calendarapp"
    ) -> str:
        """Generate application.yml for Spring Boot configuration."""
        context = {
            "project_name": project_name,
            "db_url": db_url,
            "db_user": db_user,
            "db_password": db_password,
            "server_port": server_port,
            "package": package
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "application_yml", context
        )
        return template

    @staticmethod
    def generate_entity_template(
        entity_name: str,
        table_name: str,
        package: str = "com.example.calendarapp",
        fields: list = None,
        description: str = None
    ) -> str:
        """Generate a JPA entity template."""
        context = {
            "entity_name": entity_name,
            "table_name": table_name,
            "package": package,
            "fields": fields or [],
            "description": description
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "jpa_entity", context
        )
        return template

    @staticmethod
    def generate_repository_template(
        entity_name: str,
        package: str = "com.example.calendarapp",
        custom_queries: list = None
    ) -> str:
        """Generate a Spring Data JPA repository template."""
        context = {
            "entity_name": entity_name,
            "package": package,
            "custom_queries": custom_queries or []
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "jpa_repository", context
        )
        return template

    @staticmethod
    def generate_service_template(
        entity_name: str,
        package: str = "com.example.calendarapp",
        custom_methods: list = None
    ) -> str:
        """Generate a Spring service template."""
        context = {
            "entity_name": entity_name,
            "package": package,
            "custom_methods": custom_methods or []
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "spring_service", context
        )
        return template

    @staticmethod
    def generate_controller_template(
        entity_name: str,
        endpoint_path: str = "",
        package: str = "com.example.calendarapp",
        custom_endpoints: list = None
    ) -> str:
        """Generate a REST controller template."""
        if not endpoint_path:
            endpoint_path = entity_name.lower()

        context = {
            "entity_name": entity_name,
            "endpoint_path": endpoint_path,
            "package": package,
            "custom_endpoints": custom_endpoints or []
        }
        template = JinjaTemplateLoader.render_template(
            str(BackendSkill.TEMPLATES_FILE), "rest_controller", context
        )
        return template
