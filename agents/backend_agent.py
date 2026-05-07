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

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None) -> None:
        """Generate complete Spring Boot project structure with subtask-specific code."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create subtasks folder for organization
        subtasks_folder = project_folder / "subtasks"
        subtasks_folder.mkdir(parents=True, exist_ok=True)

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

        # Create entities for standard project entities
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entities = ["user", "task", "audit"]

        for entity in entities:
            entity_path = entity_dir / f"{entity.title()}.java"
            entity_path.write_text(
                BackendSkill.generate_entity_template(entity),
                encoding="utf-8"
            )
            self.created_files.append(entity_path)
            self.log_action(f"Generated entity: {entity.title()}")

        # Create repositories for all entities
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        for entity in entities:
            repo_path = repo_dir / f"{entity.title()}Repository.java"
            repo_path.write_text(
                BackendSkill.generate_repository_template(entity),
                encoding="utf-8"
            )
            self.created_files.append(repo_path)
            self.log_action(f"Generated repository: {entity.title()}Repository")

        # Create services for all entities
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        for entity in entities:
            service_path = service_dir / f"{entity.title()}Service.java"
            service_path.write_text(
                BackendSkill.generate_service_template(entity),
                encoding="utf-8"
            )
            self.created_files.append(service_path)
            self.log_action(f"Generated service: {entity.title()}Service")

        # Create controllers for all entities
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        for entity in entities:
            controller_path = controller_dir / f"{entity.title()}Controller.java"
            controller_path.write_text(
                BackendSkill.generate_controller_template(entity),
                encoding="utf-8"
            )
            self.created_files.append(controller_path)
            self.log_action(f"Generated controller: {entity.title()}Controller")

        # Create setup script
        setup_script = project_folder / "setup.sh"
        setup_script.write_text(
            BackendSkill.generate_pom_maven_setup(),
            encoding="utf-8"
        )
        self.created_files.append(setup_script)

        # Generate subtask-specific implementations
        if subtasks:
            self._generate_subtask_implementations(project_folder, subtasks, base_package)

        self.log_action(f"Backend project structure created: {project_name}")

    def _generate_subtask_implementations(
        self, project_folder: Path, subtasks: List[Dict[str, Any]], base_package: str
    ) -> None:
        """Generate specific code for each subtask."""
        subtasks_folder = project_folder / "subtasks"

        for idx, subtask in enumerate(subtasks, 1):
            subtask_name = subtask["title"].lower().replace(" - ", "_").replace(" ", "_")
            subtask_folder = subtasks_folder / f"{idx:02d}_{subtask_name}"
            subtask_folder.mkdir(parents=True, exist_ok=True)

            # Create README for subtask
            readme_content = f"""# {subtask['title']}

## Description
{subtask['description']}

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests written
- [ ] Documentation updated
- [ ] Code reviewed

## Files Generated
Generated implementation files for this subtask.
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            # Subtask 1: Setup Spring Boot
            if idx == 1:
                self._generate_subtask_1_setup(subtask_folder, base_package)
            # Subtask 2: Entities & Repositories
            elif idx == 2:
                self._generate_subtask_2_entities_repos(subtask_folder, base_package)
            # Subtask 3: Services
            elif idx == 3:
                self._generate_subtask_3_services(subtask_folder, base_package)
            # Subtask 4: Controllers
            elif idx == 4:
                self._generate_subtask_4_controllers(subtask_folder, base_package)
            # Subtask 5: Security
            elif idx == 5:
                self._generate_subtask_5_security(subtask_folder, base_package)

    def _generate_subtask_1_setup(self, subtask_folder: Path, base_package: str) -> None:
        """Generate Spring Boot setup files with proper structure."""
        # Create pom.xml
        pom_path = subtask_folder / "pom.xml"
        pom_path.write_text(BackendSkill.generate_pom_xml("setup"), encoding="utf-8")
        self.created_files.append(pom_path)

        # Create application.yml
        resources_dir = subtask_folder / "src" / "main" / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)

        app_yml = resources_dir / "application.yml"
        app_yml.write_text(BackendSkill.generate_application_yml(), encoding="utf-8")
        self.created_files.append(app_yml)

        # Create main application class
        java_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package
        java_dir.mkdir(parents=True, exist_ok=True)

        app_class = """package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""
        app_class_path = java_dir / "Application.java"
        app_class_path.write_text(app_class, encoding="utf-8")
        self.created_files.append(app_class_path)

        self.log_action("Generated subtask 1: Setup with pom.xml and application.yml")

    def _generate_subtask_2_entities_repos(self, subtask_folder: Path, base_package: str) -> None:
        """Generate JPA entities and repositories with proper structure."""
        # Entity directory
        entity_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package / "entity"
        entity_dir.mkdir(parents=True, exist_ok=True)

        # Repository directory
        repo_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package / "repository"
        repo_dir.mkdir(parents=True, exist_ok=True)

        for entity in ["user", "task", "audit"]:
            # Create entity
            entity_path = entity_dir / f"{entity.title()}.java"
            entity_path.write_text(BackendSkill.generate_entity_template(entity), encoding="utf-8")
            self.created_files.append(entity_path)

            # Create repository
            repo_path = repo_dir / f"{entity.title()}Repository.java"
            repo_path.write_text(BackendSkill.generate_repository_template(entity), encoding="utf-8")
            self.created_files.append(repo_path)

        self.log_action("Generated subtask 2: Entities and Repositories with src structure")

    def _generate_subtask_3_services(self, subtask_folder: Path, base_package: str) -> None:
        """Generate service layer with proper structure."""
        service_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package / "service"
        service_dir.mkdir(parents=True, exist_ok=True)

        for entity in ["user", "task", "audit"]:
            service_path = service_dir / f"{entity.title()}Service.java"
            service_path.write_text(BackendSkill.generate_service_template(entity), encoding="utf-8")
            self.created_files.append(service_path)

        self.log_action("Generated subtask 3: Services with src structure")

    def _generate_subtask_4_controllers(self, subtask_folder: Path, base_package: str) -> None:
        """Generate REST controllers with proper structure."""
        controller_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package / "controller"
        controller_dir.mkdir(parents=True, exist_ok=True)

        for entity in ["user", "task", "audit"]:
            controller_path = controller_dir / f"{entity.title()}Controller.java"
            controller_path.write_text(BackendSkill.generate_controller_template(entity), encoding="utf-8")
            self.created_files.append(controller_path)

        self.log_action("Generated subtask 4: Controllers with src structure")

    def _generate_subtask_5_security(self, subtask_folder: Path, base_package: str) -> None:
        """Generate security configuration with proper structure."""
        config_dir = subtask_folder / "src" / "main" / "java" / "com" / "example" / base_package / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        security_config = """package com.example.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
            .antMatchers("/api/v1/public/**").permitAll()
            .antMatchers("/api/v1/**").authenticated()
            .and()
            .httpBasic()
            .and()
            .csrf().disable();
        return http.build();
    }
}
"""
        security_path = config_dir / "SecurityConfig.java"
        security_path.write_text(security_config, encoding="utf-8")
        self.created_files.append(security_path)

        self.log_action("Generated subtask 5: Security Configuration with src structure")
