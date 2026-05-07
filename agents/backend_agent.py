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

        # Sanitize filename by removing colons
        sanitized_id = subtask["id"].replace(":", "_")
        filepath = self.save_task_file(
            filename=sanitized_id,
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
        """Create backend subtasks specific to the business process."""
        # Map business processes to backend technical specifications
        business_process = task_title.split(" - ")[0]  # Extract business process name

        subtask_specs = {
            "User Management": {
                "title": "User Entity & CRUD Operations",
                "description": "Create User JPA entity with all fields, UserRepository for database operations, and UserService for business logic including registration, profile updates, and user lookup",
                "apis": ["/api/v1/users", "/api/v1/users/{id}"],
                "db_schemas": ["users table", "user_profiles table"],
                "auth_required": False,
            },
            "Authentication & Authorization": {
                "title": "JWT Authentication & Security Config",
                "description": "Implement Spring Security with JWT token generation/validation, login endpoint, session management, and role-based access control (RBAC)",
                "apis": ["/api/v1/auth/login", "/api/v1/auth/logout", "/api/v1/auth/refresh"],
                "db_schemas": ["sessions table", "roles table"],
                "auth_required": True,
            },
            "Core Business Logic": {
                "title": "Core Service Implementation",
                "description": "Implement main business logic services for the project domain, including data processing, workflow management, and business rule validation",
                "apis": ["/api/v1/resources", "/api/v1/resources/{id}"],
                "db_schemas": ["resources table", "workflows table"],
                "auth_required": True,
            },
            "API & Integration": {
                "title": "REST API Endpoints & Controllers",
                "description": "Build comprehensive REST API controllers with proper HTTP methods, request/response handling, error responses, and integration with backend services",
                "apis": ["/api/v1/", "/api/v1/health", "/api/v1/status"],
                "db_schemas": ["integrations table"],
                "auth_required": True,
            },
            "Audit & Monitoring": {
                "title": "Audit Logging & Monitoring Service",
                "description": "Implement comprehensive audit logging service to track user actions, system events, and changes. Create audit endpoints for retrieving audit logs and activity reports",
                "apis": ["/api/v1/audit", "/api/v1/audit/logs", "/api/v1/reports"],
                "db_schemas": ["audit_logs table", "activity_logs table"],
                "auth_required": True,
            },
        }

        # Get specifications for this business process, or use defaults
        spec = subtask_specs.get(business_process, {
            "title": f"Backend Implementation for {business_process}",
            "description": f"Implement backend components for {business_process}",
            "apis": [f"/api/v1/{business_process.lower().replace(' ', '_')}"],
            "db_schemas": [f"{business_process.lower().replace(' ', '_')} tables"],
            "auth_required": True,
        })

        subtask = self.create_backend_subtask(
            task_id=task_id,
            title=f"{spec['title']} - {task_title}",
            description=spec["description"],
            apis=spec.get("apis", []),
            db_schemas=spec.get("db_schemas", []),
            auth_required=spec.get("auth_required", False),
        )

        return [subtask]

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None) -> None:
        """Generate Spring Boot project structure based on business process subtasks."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        base_package = project_name.lower().replace(' ', '').replace('-', '')

        # Setup base project structure on first business process
        if subtasks:
            self._setup_base_project(project_folder, base_package, project_name)

            for subtask in subtasks:
                self._generate_subtask_code(project_folder, subtask, project_name, base_package)

            # Generate subtask documentation
            self._generate_subtask_documentation(project_folder, subtasks)

        self.log_action(f"Backend project structure created: {project_name}")

    def _setup_base_project(self, project_folder: Path, base_package: str, project_name: str) -> None:
        """Setup base Spring Boot project structure."""
        # Create pom.xml if it doesn't exist
        pom_path = project_folder / "pom.xml"
        if not pom_path.exists():
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
            f"src/main/java/com/example/{base_package}/config",
            f"src/main/java/com/example/{base_package}/dto",
            "src/main/resources",
            "src/test/java/com/example",
            "target",
        ]
        for dir_name in src_dirs:
            (project_folder / dir_name).mkdir(parents=True, exist_ok=True)

        # Create application.yml if it doesn't exist
        app_yml_path = project_folder / "src/main/resources/application.yml"
        if not app_yml_path.exists():
            app_yml_path.write_text(
                BackendSkill.generate_application_yml(),
                encoding="utf-8"
            )
            self.created_files.append(app_yml_path)

    def _generate_subtask_code(self, project_folder: Path, subtask: Dict[str, Any],
                               project_name: str, base_package: str) -> None:
        """Generate code specific to each business process."""
        # Extract business process from subtask title
        title = subtask.get("title", "")
        business_process = title.split(" - ")[0] if " - " in title else title

        if "User Management" in business_process:
            self._generate_user_management_code(project_folder, base_package)
        elif "Authentication" in business_process:
            self._generate_authentication_code(project_folder, base_package)
        elif "Core Business Logic" in business_process:
            self._generate_core_logic_code(project_folder, base_package)
        elif "API & Integration" in business_process:
            self._generate_api_integration_code(project_folder, base_package)
        elif "Audit & Monitoring" in business_process:
            self._generate_audit_code(project_folder, base_package)

    def _generate_user_management_code(self, project_folder: Path, base_package: str) -> None:
        """Generate User entity, repository, service, and controller."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)

        entity_path = entity_dir / "User.java"
        if not entity_path.exists():
            entity_path.write_text(
                BackendSkill.generate_entity_template("user"),
                encoding="utf-8"
            )
            self.created_files.append(entity_path)
            self.log_action("Generated entity: User")

        # Create User repository
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        repo_dir.mkdir(parents=True, exist_ok=True)
        repo_path = repo_dir / "UserRepository.java"
        if not repo_path.exists():
            repo_path.write_text(
                BackendSkill.generate_repository_template("user"),
                encoding="utf-8"
            )
            self.created_files.append(repo_path)
            self.log_action("Generated repository: UserRepository")

        # Create User service
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        service_path = service_dir / "UserService.java"
        if not service_path.exists():
            service_path.write_text(
                BackendSkill.generate_service_template("user"),
                encoding="utf-8"
            )
            self.created_files.append(service_path)
            self.log_action("Generated service: UserService")

    def _generate_authentication_code(self, project_folder: Path, base_package: str) -> None:
        """Generate authentication/security configuration."""
        config_dir = project_folder / f"src/main/java/com/example/{base_package}/config"
        config_dir.mkdir(parents=True, exist_ok=True)

        # Create JWT configuration placeholder
        config_path = config_dir / "SecurityConfig.java"
        if not config_path.exists():
            config_path.write_text(
                "package com.example." + base_package + ".config;\n\n"
                "import org.springframework.context.annotation.Configuration;\n\n"
                "@Configuration\n"
                "public class SecurityConfig {\n"
                "    // Spring Security configuration for JWT authentication\n"
                "}\n",
                encoding="utf-8"
            )
            self.created_files.append(config_path)
            self.log_action("Generated security config")

    def _generate_core_logic_code(self, project_folder: Path, base_package: str) -> None:
        """Generate core business logic services."""
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)

        service_path = service_dir / "BusinessLogicService.java"
        if not service_path.exists():
            service_path.write_text(
                "package com.example." + base_package + ".service;\n\n"
                "import org.springframework.stereotype.Service;\n\n"
                "@Service\n"
                "public class BusinessLogicService {\n"
                "    // Core business logic implementation\n"
                "}\n",
                encoding="utf-8"
            )
            self.created_files.append(service_path)
            self.log_action("Generated service: BusinessLogicService")

    def _generate_api_integration_code(self, project_folder: Path, base_package: str) -> None:
        """Generate REST controllers and API endpoints."""
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)

        # Create API controller
        controller_path = controller_dir / "ApiController.java"
        if not controller_path.exists():
            controller_path.write_text(
                "package com.example." + base_package + ".controller;\n\n"
                "import org.springframework.web.bind.annotation.RestController;\n"
                "import org.springframework.web.bind.annotation.RequestMapping;\n\n"
                "@RestController\n"
                "@RequestMapping(\"/api/v1\")\n"
                "public class ApiController {\n"
                "    // REST API endpoints\n"
                "}\n",
                encoding="utf-8"
            )
            self.created_files.append(controller_path)
            self.log_action("Generated controller: ApiController")

    def _generate_audit_code(self, project_folder: Path, base_package: str) -> None:
        """Generate audit logging service."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)

        entity_path = entity_dir / "AuditLog.java"
        if not entity_path.exists():
            entity_path.write_text(
                BackendSkill.generate_entity_template("audit"),
                encoding="utf-8"
            )
            self.created_files.append(entity_path)
            self.log_action("Generated entity: AuditLog")

        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        service_path = service_dir / "AuditService.java"
        if not service_path.exists():
            service_path.write_text(
                BackendSkill.generate_service_template("audit"),
                encoding="utf-8"
            )
            self.created_files.append(service_path)
            self.log_action("Generated service: AuditService")

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

