"""Frontend Agent - Creates frontend subtasks and UI implementation plans."""

from typing import Any, Dict, List

from .base_agent import BaseAgent


class FrontendAgent(BaseAgent):
    """Agent responsible for frontend development subtasks."""

    def __init__(self):
        """Initialize Frontend Agent."""
        super().__init__(
            agent_id="frontend_agent",
            name="Frontend Agent",
            role="frontend_developer",
            output_folder="subtasks/frontend",
            skills=[
                "ui_ux_design",
                "component_architecture",
                "state_management",
                "responsive_design",
            ],
        )

    def create_frontend_subtask(
        self,
        task_id: str,
        title: str,
        description: str,
        components: List[str] = None,
        pages: List[str] = None,
        responsive: bool = True,
    ) -> Dict[str, Any]:
        """Create a frontend-specific subtask."""
        subtask = self.create_task(
            title=title,
            description=description,
            task_type="frontend_subtask",
        )

        subtask["parent_task_id"] = task_id
        subtask["domain"] = "frontend"
        subtask["components"] = components or []
        subtask["pages"] = pages or []
        subtask["responsive"] = responsive
        subtask["acceptance_criteria"] = []

        return subtask

    def save_subtask(self, subtask: Dict[str, Any]) -> str:
        """Save frontend subtask to file."""
        content = self.generate_metadata(
            subtask["title"],
            subtask["description"],
        )

        content += f"## Domain\nFrontend\n\n"
        content += f"## Parent Task\n{subtask['parent_task_id']}\n\n"

        if subtask["pages"]:
            content += "## Pages to Create\n"
            for page in subtask["pages"]:
                content += f"- {page}\n"
            content += "\n"

        if subtask["components"]:
            content += "## Components to Build\n"
            for component in subtask["components"]:
                content += f"- {component}\n"
            content += "\n"

        if subtask["responsive"]:
            content += "## Responsive Design\nRequired: Yes\n\n"

        content += "## Acceptance Criteria\n"
        if subtask["acceptance_criteria"]:
            for criterion in subtask["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] All components implemented\n"
            content += "- [ ] Responsive design working\n"
            content += "- [ ] Connected to backend APIs\n"
            content += "- [ ] User testing passed\n"
        content += "\n"

        content += f"## Status\n{subtask['status']}\n"

        filepath = self.save_task_file(
            filename=subtask["id"],
            content=content,
            task_id=None,
        )

        self.log_action(
            f"Created frontend subtask for {subtask['parent_task_id']}: {subtask['title']}"
        )
        return str(filepath)

    def create_subtasks_from_task(
        self,
        task_id: str,
        task_title: str,
    ) -> List[Dict[str, Any]]:
        """Create multiple frontend subtasks from a main task."""
        subtasks = [
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"UI Components - {task_title}",
                description="Build reusable UI components",
                components=["Button", "Form", "Card", "Modal"],
            ),
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"Pages - {task_title}",
                description="Implement feature pages",
                pages=["Dashboard", "Details", "Settings"],
            ),
        ]

        return subtasks
