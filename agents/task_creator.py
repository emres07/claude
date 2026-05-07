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
        task_id = task["id"].replace(":", "_").replace("/", "_")

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
        """Break down a project into business process tasks."""
        if domains is None:
            domains = ["backend", "frontend", "database"]

        tasks = []

        # Define common business processes
        business_processes = [
            {
                "title": "User Management",
                "description": "Implement user registration, profile management, and user data handling",
                "criteria": [
                    "User registration workflow implemented",
                    "User profile management complete",
                    "User data validation working",
                    "User deletion/deactivation supported",
                ],
            },
            {
                "title": "Authentication & Authorization",
                "description": "Implement user login, authentication, session management, and access control",
                "criteria": [
                    "Authentication mechanism implemented",
                    "Session/token management working",
                    "Authorization rules enforced",
                    "Password security implemented",
                ],
            },
            {
                "title": "Core Business Logic",
                "description": "Implement main business logic, workflow automation, and data processing",
                "criteria": [
                    "Core business workflows implemented",
                    "Data processing logic working",
                    "Validation rules applied",
                    "Error handling in place",
                ],
            },
            {
                "title": "API & Integration",
                "description": "Build REST APIs, third-party integrations, and service connections",
                "criteria": [
                    "API endpoints implemented",
                    "Third-party integrations complete",
                    "Frontend-backend integration working",
                    "Data synchronization functional",
                ],
            },
            {
                "title": "Audit & Monitoring",
                "description": "Implement audit logging, monitoring, reporting, and compliance tracking",
                "criteria": [
                    "Audit logging implemented",
                    "User activity tracking working",
                    "Reports and analytics available",
                    "Compliance requirements met",
                ],
            },
        ]

        # Create a task for each business process
        for process_data in business_processes:
            bp_task = self.create_main_task(
                title=f"{process_data['title']} - {project_name}",
                description=f"{process_data['description']}. {project_description}",
                priority=priority,
                domains=domains,  # Each business process task includes all domains
                acceptance_criteria=process_data["criteria"],
            )
            tasks.append(bp_task)

        self.log_action(f"Created {len(tasks)} business process tasks from project: {project_name}")
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
