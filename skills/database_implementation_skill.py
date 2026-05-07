"""Database Implementation Skill - Generates fully implemented Oracle procedures."""

from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class DatabaseImplementationSkill:
    """Generate fully implemented Oracle database code without TODOs."""

    TEMPLATES_FILE = Path(__file__).parent / "database_implementation_templates.md"

    @staticmethod
    def generate_table_full_definition(
        table_name: str,
        columns: list = None,
        indexes: list = None,
        unique_constraints: list = None,
        workflow_name: str = None
    ) -> str:
        """Generate complete table with columns, indexes, and constraints."""
        context = {
            "table_name": table_name,
            "columns": columns or [],  # [{name, oracle_type, constraints}]
            "indexes": indexes or [],  # [{field}]
            "unique_constraints": unique_constraints or [],
            "workflow_name": workflow_name
        }
        return JinjaTemplateLoader.render_template(
            str(DatabaseImplementationSkill.TEMPLATES_FILE), "table_full_definition", context
        )

    @staticmethod
    def generate_crud_package_complete(
        table_name: str,
        columns: list = None,
        custom_procedures: list = None
    ) -> str:
        """Generate complete CRUD package with all operations."""
        context = {
            "table_name": table_name,
            "columns": columns or [],  # [{name, oracle_type}]
            "custom_procedures": custom_procedures or []
        }
        return JinjaTemplateLoader.render_template(
            str(DatabaseImplementationSkill.TEMPLATES_FILE), "crud_package_complete", context
        )

    @staticmethod
    def generate_audit_trigger_advanced(
        table_name: str,
        columns: list = None
    ) -> str:
        """Generate advanced audit trigger with column tracking."""
        context = {
            "table_name": table_name,
            "columns": columns or []
        }
        return JinjaTemplateLoader.render_template(
            str(DatabaseImplementationSkill.TEMPLATES_FILE), "audit_trigger_advanced", context
        )
