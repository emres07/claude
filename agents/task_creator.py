"""Task Creator Agent - Creates main tasks from requirements."""

from typing import Any, Dict, List

from .base_agent import BaseAgent


class TaskCreatorAgent(BaseAgent):
    """Agent responsible for creating main tasks."""

    def __init__(self):
        """Initialize Task Creator Agent."""
        super().__init__(
            agent_id="task_creator",
            name="Task Creator Agent",
            role="task_creator",
            output_folder="tasks",
            skills=[
                "task_definition",
                "scope_management",
                "requirement_analysis",
            ],
        )

    def create_main_task(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        domains: List[str] = None,
        acceptance_criteria: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a main task that will be distributed to other agents."""
        if domains is None:
            domains = ["backend", "frontend", "database"]
        if acceptance_criteria is None:
            acceptance_criteria = []

        task = self.create_task(
            title=title,
            description=description,
            priority=priority,
            task_type="main_task",
        )

        task["domains"] = domains
        task["acceptance_criteria"] = acceptance_criteria
        task["subtasks"] = []

        return task

    def save_task(self, task: Dict[str, Any]) -> str:
        """Save main task to file."""
        task_id = task["id"]

        # Build markdown content
        content = self.generate_metadata(task["title"], task["description"])
        content += f"## Priority\n{task['priority'].upper()}\n\n"
        content += f"## Domains\n" + "\n".join(
            [f"- {domain}" for domain in task["domains"]]
        )
        content += "\n\n"

        if task["acceptance_criteria"]:
            content += "## Acceptance Criteria\n"
            for criterion in task["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
            content += "\n"

        content += "## Subtasks\n"
        if task["subtasks"]:
            for subtask in task["subtasks"]:
                content += f"- [{subtask['domain']}] {subtask['title']}\n"
        else:
            content += "*(To be created by specialized agents)*\n"

        content += f"\n## Status\n{task['status']}\n"

        filepath = self.save_task_file(
            filename=f"{task_id}_main",
            content=content,
            task_id=None,
        )

        self.log_action(f"Created main task: {task['title']}")
        return str(filepath)

    def create_tasks_from_project(
        self,
        project_name: str,
        project_description: str,
        priority: str = "medium",
        domains: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """Break down a project into project phases as main tasks."""
        if domains is None:
            domains = ["backend", "frontend", "database"]

        tasks = []

        # Define project phases
        phases = [
            {
                "phase": "Phase 1",
                "title": "Setup & Configuration",
                "description": "Project initialization, configuration, and environment setup",
                "criteria": [
                    "Project structure created",
                    "Build tools configured",
                    "Dependencies installed",
                    "Configuration files set up",
                ],
            },
            {
                "phase": "Phase 2",
                "title": "Core Entity/Component Structure",
                "description": "Create core entities, database tables, and UI components",
                "criteria": [
                    "Core entities/models defined",
                    "Database tables created",
                    "Base components built",
                    "Data structures validated",
                ],
            },
            {
                "phase": "Phase 3",
                "title": "Business Logic & Services",
                "description": "Implement business logic, services, and core functionality",
                "criteria": [
                    "Business logic implemented",
                    "Service layer created",
                    "Data validation working",
                    "Error handling in place",
                ],
            },
            {
                "phase": "Phase 4",
                "title": "API & Integration",
                "description": "Build REST APIs, controllers, and frontend integration",
                "criteria": [
                    "API endpoints implemented",
                    "Frontend-backend integration complete",
                    "Feature components integrated",
                    "Routing configured",
                ],
            },
            {
                "phase": "Phase 5",
                "title": "Security, Testing & Documentation",
                "description": "Implement security, add tests, and create documentation",
                "criteria": [
                    "Security implemented",
                    "Unit tests written",
                    "Integration tests passing",
                    "Documentation complete",
                ],
            },
        ]

        # Create a task for each phase
        for phase_data in phases:
            phase_task = self.create_main_task(
                title=f"{phase_data['phase']}: {phase_data['title']} - {project_name}",
                description=f"{phase_data['description']}. {project_description}",
                priority=priority,
                domains=domains,  # Each phase task includes all domains
                acceptance_criteria=phase_data["criteria"],
            )
            tasks.append(phase_task)

        self.log_action(f"Created {len(tasks)} phase tasks from project: {project_name}")
        return tasks

    def distribute_task(self, task: Dict[str, Any]) -> Dict[str, List[str]]:
        """Distribute task to relevant domain agents."""
        distribution = {
            "backend": [],
            "frontend": [],
            "database": [],
        }

        for domain in task.get("domains", []):
            if domain in distribution:
                distribution[domain].append(task["id"])

        self.log_action(
            f"Distributed task {task['id']} to domains: {list(distribution.keys())}"
        )
        return distribution
