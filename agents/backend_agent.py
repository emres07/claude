"""Backend Agent - Creates backend subtasks and implementation plans."""

from typing import Any, Dict, List

from .base_agent import BaseAgent


class BackendAgent(BaseAgent):
    """Agent responsible for backend development subtasks."""

    def __init__(self):
        """Initialize Backend Agent."""
        super().__init__(
            agent_id="backend_agent",
            name="Backend Agent",
            role="backend_developer",
            output_folder="subtasks/backend",
            skills=[
                "backend_architecture",
                "api_design",
                "database_schema_planning",
                "authentication_planning",
            ],
        )

    def create_backend_subtask(
        self,
        task_id: str,
        title: str,
        description: str,
        apis: List[str] = None,
        db_schemas: List[str] = None,
        auth_required: bool = False,
    ) -> Dict[str, Any]:
        """Create a backend-specific subtask."""
        subtask = self.create_task(
            title=title,
            description=description,
            task_type="backend_subtask",
        )

        subtask["parent_task_id"] = task_id
        subtask["domain"] = "backend"
        subtask["apis"] = apis or []
        subtask["db_schemas"] = db_schemas or []
        subtask["auth_required"] = auth_required
        subtask["acceptance_criteria"] = []

        return subtask

    def save_subtask(self, subtask: Dict[str, Any]) -> str:
        """Save backend subtask to file."""
        content = self.generate_metadata(
            subtask["title"],
            subtask["description"],
        )

        content += f"## Domain\nBackend\n\n"
        content += f"## Parent Task\n{subtask['parent_task_id']}\n\n"

        if subtask["apis"]:
            content += "## APIs to Implement\n"
            for api in subtask["apis"]:
                content += f"- {api}\n"
            content += "\n"

        if subtask["db_schemas"]:
            content += "## Database Schemas\n"
            for schema in subtask["db_schemas"]:
                content += f"- {schema}\n"
            content += "\n"

        if subtask["auth_required"]:
            content += "## Authentication\nRequired: Yes\n\n"

        content += "## Acceptance Criteria\n"
        if subtask["acceptance_criteria"]:
            for criterion in subtask["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] API endpoints implemented\n"
            content += "- [ ] Database integration complete\n"
            content += "- [ ] Error handling implemented\n"
        content += "\n"

        content += f"## Status\n{subtask['status']}\n"

        filepath = self.save_task_file(
            filename=subtask["id"],
            content=content,
            task_id=None,
        )

        self.log_action(
            f"Created backend subtask for {subtask['parent_task_id']}: {subtask['title']}"
        )
        return str(filepath)

    def create_subtasks_from_task(
        self,
        task_id: str,
        task_title: str,
    ) -> List[Dict[str, Any]]:
        """Create multiple backend subtasks from a main task."""
        subtasks = [
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Backend API Implementation - {task_title}",
                description="Implement REST APIs for the feature",
                apis=["/api/v1/...", "/api/v1/.../detail"],
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Database Schema - {task_title}",
                description="Design and implement database schema",
                db_schemas=["users", "transactions"],
            ),
        ]

        return subtasks
