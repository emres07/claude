"""Backend Agent - Creates backend subtasks and generates Spring Boot Java code."""

from typing import Any, Dict, List
from pathlib import Path

from .base_agent import BaseAgent
from skills.backend_skills import BackendSkill


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
                "java",
                "spring_boot",
                "hibernate",
                "maven",
                "clean_code",
                "api_design",
            ],
        )
        self.code_folder = Path("backend")
        self.code_folder.mkdir(parents=True, exist_ok=True)

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
                description="Implement REST APIs with Spring Boot",
                apis=["/api/v1/...", "/api/v1/.../detail"],
                auth_required=True,
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Database Schema & Hibernate Mapping - {task_title}",
                description="Design schema and create Hibernate entities",
                db_schemas=["users", "transactions"],
            ),
        ]

        return subtasks

    def generate_project_structure(self, project_name: str) -> None:
        """Generate complete Spring Boot project structure."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create pom.xml
        pom_path = project_folder / "pom.xml"
        pom_path.write_text(
            BackendSkill.generate_pom_xml(project_name),
            encoding="utf-8"
        )
        self.created_files.append(pom_path)
        self.log_action(f"Generated pom.xml for {project_name}")

        # Create source directories
        base_package = project_name.lower().replace(' ', '').replace('-', '')
        src_dirs = [
            f"src/main/java/com/example/{base_package}",
            f"src/main/java/com/example/{base_package}/entity",
            f"src/main/java/com/example/{base_package}/repository",
            f"src/main/java/com/example/{base_package}/service",
            f"src/main/java/com/example/{base_package}/controller",
            "src/main/resources",
            "src/test/java/com/example",
            "target",
        ]

        for dir_name in src_dirs:
            (project_folder / dir_name).mkdir(parents=True, exist_ok=True)

        # Create application.yml
        app_yml_path = project_folder / "src/main/resources/application.yml"
        app_yml_path.write_text(
            BackendSkill.generate_application_yml(),
            encoding="utf-8"
        )
        self.created_files.append(app_yml_path)

        # Create sample entity
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        user_entity_path = entity_dir / "User.java"
        user_entity_path.write_text(
            BackendSkill.generate_entity_template("user"),
            encoding="utf-8"
        )
        self.created_files.append(user_entity_path)

        # Create sample repository
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        user_repo_path = repo_dir / "UserRepository.java"
        user_repo_path.write_text(
            BackendSkill.generate_repository_template("user"),
            encoding="utf-8"
        )
        self.created_files.append(user_repo_path)

        # Create sample service
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        user_service_path = service_dir / "UserService.java"
        user_service_path.write_text(
            BackendSkill.generate_service_template("user"),
            encoding="utf-8"
        )
        self.created_files.append(user_service_path)

        # Create sample controller
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        user_controller_path = controller_dir / "UserController.java"
        user_controller_path.write_text(
            BackendSkill.generate_controller_template("user"),
            encoding="utf-8"
        )
        self.created_files.append(user_controller_path)

        # Create setup script
        setup_script = project_folder / "setup.sh"
        setup_script.write_text(
            BackendSkill.generate_pom_maven_setup(),
            encoding="utf-8"
        )
        self.created_files.append(setup_script)

        self.log_action(f"Backend project structure created: {project_name}")
