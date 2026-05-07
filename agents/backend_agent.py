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
                title=f"Setup Spring Boot Project - {task_title}",
                description="Initialize Spring Boot 3.x project with Maven, dependencies, and configuration",
                apis=["project initialization", "Maven configuration", "Application properties"],
                auth_required=False,
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Create Entities & Repositories - {task_title}",
                description="Design JPA entities and create Spring Data JPA repositories",
                db_schemas=["entity mapping", "repository interfaces", "custom queries"],
                auth_required=False,
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Implement Services & Business Logic - {task_title}",
                description="Create service layer with business logic and transaction management",
                apis=["business logic", "CRUD operations", "data validation"],
                auth_required=False,
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Build REST Controllers & APIs - {task_title}",
                description="Implement REST controllers with proper endpoints and request handling",
                apis=["/api/v1/users", "/api/v1/tasks", "/api/v1/audit"],
                auth_required=True,
            ),
            self.create_backend_subtask(
                task_id=task_id,
                title=f"Add Security & Exception Handling - {task_title}",
                description="Implement Spring Security, authentication, and global exception handling",
                apis=["authentication", "authorization", "error handling"],
                auth_required=True,
            ),
        ]

        return subtasks

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None,
                                  subtask_indices: List[int] = None) -> None:
        """Generate Spring Boot project structure based on subtasks."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        base_package = project_name.lower().replace(' ', '').replace('-', '')

        # Only generate code for subtasks passed in
        if subtasks:
            for i, subtask in enumerate(subtasks):
                # Use provided indices or default to enumerate indices
                idx = subtask_indices[i] if subtask_indices and i < len(subtask_indices) else i + 1
                self._generate_subtask_code(project_folder, subtask, idx, project_name, base_package)

        # Generate subtask documentation
        if subtasks:
            self._generate_subtask_documentation(project_folder, subtasks)

        self.log_action(f"Backend project structure created: {project_name}")

    def _generate_subtask_code(self, project_folder: Path, subtask: Dict[str, Any],
                               subtask_idx: int, project_name: str, base_package: str) -> None:
        """Generate code specific to each subtask."""
        entities = ["user", "task", "audit"]

        if subtask_idx == 1:
            # Subtask 1: Setup Spring Boot Project - pom.xml, config, directories
            pom_path = project_folder / "pom.xml"
            pom_path.write_text(
                BackendSkill.generate_pom_xml(project_name),
                encoding="utf-8"
            )
            self.created_files.append(pom_path)
            self.log_action(f"Generated pom.xml for {project_name}")

            # Create source directories
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

            # Create setup script
            setup_script = project_folder / "setup.sh"
            setup_script.write_text(
                BackendSkill.generate_pom_maven_setup(),
                encoding="utf-8"
            )
            self.created_files.append(setup_script)

        elif subtask_idx == 2:
            # Subtask 2: Create Entities & Repositories
            entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
            entity_dir.mkdir(parents=True, exist_ok=True)

            for entity in entities:
                entity_path = entity_dir / f"{entity.title()}.java"
                entity_path.write_text(
                    BackendSkill.generate_entity_template(entity),
                    encoding="utf-8"
                )
                self.created_files.append(entity_path)
                self.log_action(f"Generated entity: {entity.title()}")

            # Create repositories
            repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
            repo_dir.mkdir(parents=True, exist_ok=True)

            for entity in entities:
                repo_path = repo_dir / f"{entity.title()}Repository.java"
                repo_path.write_text(
                    BackendSkill.generate_repository_template(entity),
                    encoding="utf-8"
                )
                self.created_files.append(repo_path)
                self.log_action(f"Generated repository: {entity.title()}Repository")

        elif subtask_idx == 3:
            # Subtask 3: Implement Services & Business Logic
            service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
            service_dir.mkdir(parents=True, exist_ok=True)

            for entity in entities:
                service_path = service_dir / f"{entity.title()}Service.java"
                service_path.write_text(
                    BackendSkill.generate_service_template(entity),
                    encoding="utf-8"
                )
                self.created_files.append(service_path)
                self.log_action(f"Generated service: {entity.title()}Service")

        elif subtask_idx == 4:
            # Subtask 4: Build REST Controllers & APIs
            controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
            controller_dir.mkdir(parents=True, exist_ok=True)

            for entity in entities:
                controller_path = controller_dir / f"{entity.title()}Controller.java"
                controller_path.write_text(
                    BackendSkill.generate_controller_template(entity),
                    encoding="utf-8"
                )
                self.created_files.append(controller_path)
                self.log_action(f"Generated controller: {entity.title()}Controller")

        elif subtask_idx == 5:
            # Subtask 5: Add Security & Exception Handling
            # This could include SecurityConfig, GlobalExceptionHandler, etc.
            # For now, we'll create placeholder security infrastructure
            pass

    def _generate_subtask_documentation(
        self, project_folder: Path, subtasks: List[Dict[str, Any]]
    ) -> None:
        """Generate documentation for each subtask (code is in main folder)."""
        subtasks_folder = project_folder / "subtasks"
        subtasks_folder.mkdir(parents=True, exist_ok=True)

        for idx, subtask in enumerate(subtasks, 1):
            subtask_name = (subtask["title"].lower()
                          .replace(" - ", "_")
                          .replace(" ", "_")
                          .replace("&", "")
                          .replace(":", ""))
            subtask_folder = subtasks_folder / f"{idx:02d}_{subtask_name}"
            subtask_folder.mkdir(parents=True, exist_ok=True)

            # Create detailed README for each subtask
            readme_content = f"""# {subtask['title']}

## Subtask #{idx}

### Description
{subtask['description']}

### What Was Generated
All code for this subtask has been generated in the main project folder:
- `src/main/java/com/example/todolastapp/` - Source code
- `pom.xml` - Maven configuration
- `src/main/resources/application.yml` - Application settings

### APIs Generated
{chr(10).join([f"- {api}" for api in subtask.get('apis', [])])}

### Database Schemas
{chr(10).join([f"- {schema}" for schema in subtask.get('db_schemas', [])])}

### Acceptance Criteria
- [x] Code generated automatically
- [ ] Code reviewed
- [ ] Tests written
- [ ] Integration tested

### Next Steps
1. Review generated code in main project folder
2. Customize as needed
3. Write unit tests
4. Run: `mvn clean install`
5. Start: `mvn spring-boot:run`

### Files to Review
- Look at the main project folder for all generated files
- All Java files follow Spring Boot best practices
- Entity mappings include proper relationships
- Services include business logic and error handling
- Controllers include REST endpoints with proper annotations
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            self.log_action(f"Generated documentation for subtask {idx}: {subtask['title']}")

