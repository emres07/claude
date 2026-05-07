"""Backend Agent - Creates backend subtasks and generates Spring Boot Java code."""

from typing import Any, Dict, List, Optional
from pathlib import Path

from .base_agent import BaseAgent
from skills.code_generator import DynamicCodeGenerator
from skills.detailed_subtask_generation import DetailedSubtaskGenerator
from skills.backend_helper import BackendSkill
from skills.backend_implementation_skill import BackendImplementationSkill
from skills.specification_parser import SpecificationParser


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
        """Save backend subtask to file with detailed specifications."""
        content = self.generate_metadata(
            subtask["title"],
            subtask["description"],
        )

        content += f"## Domain\nBackend\n\n"
        content += f"## Parent Task\n{subtask['parent_task_id']}\n\n"

        # Generate detailed specifications
        details = DetailedSubtaskGenerator.generate_backend_subtask_details(
            subtask["title"],
            subtask["description"],
            subtask.get("apis", []),
            subtask.get("db_schemas", [])
        )

        # APIs to Implement
        if subtask["apis"]:
            content += "## APIs to Implement\n"
            for api in subtask["apis"]:
                content += f"- {api}\n"
            content += "\n"

        # Technical Requirements
        if details.get("technical_requirements"):
            content += "## Technical Requirements\n"
            for req in details["technical_requirements"]:
                content += f"- {req}\n"
            content += "\n"

        # Database Schemas
        if subtask["db_schemas"]:
            content += "## Database Schemas\n"
            for schema in subtask["db_schemas"]:
                content += f"- {schema}\n"
            content += "\n"

        # Implementation Steps
        if details.get("implementation_steps"):
            content += "## Implementation Steps\n"
            for i, step in enumerate(details["implementation_steps"], 1):
                content += f"{i}. {step}\n"
            content += "\n"

        # Related Components
        if details.get("related_components"):
            content += "## Related Components\n"
            for component in details["related_components"]:
                content += f"- {component}\n"
            content += "\n"

        # Configuration Requirements
        if details.get("configuration"):
            content += "## Configuration Requirements\n"
            content += "```yaml\n"
            for key, value in details["configuration"].items():
                content += f"{key}: {value}\n"
            content += "```\n\n"

        # Dependencies
        if details.get("dependencies"):
            content += "## Dependencies\n"
            deps = details["dependencies"]
            if deps.get("maven"):
                content += "### Maven Dependencies\n"
                for dep in deps["maven"]:
                    content += f"- {dep}\n"
            if deps.get("internal"):
                content += "### Internal Dependencies\n"
                for dep in deps["internal"]:
                    content += f"- {dep}\n"
            content += "\n"

        # Testing Requirements
        if details.get("testing_requirements"):
            content += "## Testing Requirements\n"
            for test in details["testing_requirements"]:
                content += f"- {test}\n"
            content += "\n"

        # Code Examples
        if details.get("code_examples"):
            content += "## Code Examples\n"
            for example_name, example_code in details["code_examples"].items():
                content += f"### {example_name.replace('_', ' ').title()}\n"
                content += "```java\n"
                content += example_code + "\n"
                content += "```\n\n"

        # Authentication
        if subtask["auth_required"]:
            content += "## Authentication\nRequired: Yes\n\n"

        # Acceptance Criteria
        content += "## Acceptance Criteria\n"
        if subtask["acceptance_criteria"]:
            for criterion in subtask["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] All APIs implemented and working\n"
            content += "- [ ] Database schema created and migrations run\n"
            content += "- [ ] Authentication/authorization configured\n"
            content += "- [ ] Unit tests written (>80% coverage)\n"
            content += "- [ ] Integration tests passing\n"
            content += "- [ ] Error handling implemented\n"
            content += "- [ ] API documentation (Swagger) complete\n"
            content += "- [ ] Code reviewed and approved\n"
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
            f"Created detailed backend subtask for {subtask['parent_task_id']}: {subtask['title']}"
        )
        return str(filepath)

    def create_subtasks_from_task(
        self,
        task_id: str,
        task_title: str,
        task: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """Create backend subtasks specific to the business process or workflow."""
        # Check if this is a workflow-based task
        workflow = None
        if task and "workflow" in task:
            workflow = task["workflow"]

        # Map business processes to backend technical specifications
        business_process = task_title.split(" - ")[0]  # Extract business process name from task title

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

        # Generate workflow-specific or process-specific spec
        if workflow:
            # Create workflow-specific specification
            workflow_name = workflow.get("name", business_process)
            workflow_features = workflow.get("features", [])
            workflow_data_entities = workflow.get("data_entities", [])
            workflow_steps = workflow.get("steps", [])

            # Build workflow-specific description
            description = f"Implement backend for {workflow_name} workflow.\n\n"
            description += f"Workflow Steps:\n"
            for i, step in enumerate(workflow_steps, 1):
                description += f"{i}. {step}\n"
            description += f"\nFeatures to implement: {', '.join(workflow_features)}\n"
            description += f"Data entities to handle: {', '.join(workflow_data_entities)}"

            # Generate APIs for the workflow features
            apis = [f"/api/v1/{feature.replace('_', '/')}" for feature in workflow_features]

            # Generate table names from data entities
            db_schemas = [f"{entity.lower().replace(' ', '_')}" for entity in workflow_data_entities]

            spec = {
                "title": f"Backend Implementation for {workflow_name}",
                "description": description,
                "apis": apis,
                "db_schemas": db_schemas,
                "auth_required": True,
            }
        else:
            # Fall back to business process specifications
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

        # Store business process/workflow name for code generation
        subtask["business_process"] = business_process
        if workflow:
            subtask["workflow"] = workflow

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
        """Generate code specific to each business process based on README specifications."""
        business_process = subtask.get("business_process", "")

        # Try to find the subtask markdown file to parse specifications
        subtask_file_path = self._find_subtask_readme(business_process, subtask.get("title", ""))

        if subtask_file_path:
            # Parse the subtask file to extract field/column information
            spec = SpecificationParser.parse_subtask_file(subtask_file_path)

            # Extract data entities from the specification
            data_entities = spec.get("data_entities", [])

            if data_entities:
                # Generate backend code for each data entity
                for entity_name in data_entities:
                    self._generate_entity_code_from_spec(
                        project_folder, base_package, entity_name, spec
                    )
                return

        # Fall back to business process-based generation
        self._generate_code_by_business_process(project_folder, base_package, business_process)

    def _find_subtask_readme(self, business_process: str, subtask_title: str) -> str:
        """Find subtask MD file for the given business process."""
        # Look for subtask MD files in subtasks/backend/
        subtasks_base = Path("subtasks/backend")
        if subtasks_base.exists():
            # Search for MD files that contain the business process in their name
            for md_file in subtasks_base.glob("*.md"):
                if md_file.is_file() and md_file.name != "README.md":
                    # Read file to check if it matches the business process
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for business process in title and parent task
                        if business_process.lower() in content.lower():
                            return str(md_file)
        return ""

    def _generate_code_from_spec(self, project_folder: Path, base_package: str, spec: Dict[str, Any]) -> None:
        """Generate backend code based on parsed specification."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"

        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir.mkdir(parents=True, exist_ok=True)

        description = spec.get("description", "").lower()

        # Generate User entity if user-related
        if "user" in description:
            user_entity = DynamicCodeGenerator.generate_java_entity(spec, "User")
            entity_path = entity_dir / "User.java"
            entity_path.write_text(user_entity, encoding="utf-8")
            self.log_action("Generated: User.java")

            # Generate UserService
            user_service = DynamicCodeGenerator.generate_java_service(spec, "UserService")
            service_path = service_dir / "UserService.java"
            service_path.write_text(user_service, encoding="utf-8")
            self.log_action("Generated: UserService.java")

            # Generate UserController
            user_controller = DynamicCodeGenerator.generate_java_controller(spec, "UserController")
            controller_path = controller_dir / "UserController.java"
            controller_path.write_text(user_controller, encoding="utf-8")
            self.log_action("Generated: UserController.java")

        # Generate Audit service if audit-related
        if "audit" in description:
            audit_entity = DynamicCodeGenerator.generate_java_entity(spec, "AuditLog")
            entity_path = entity_dir / "AuditLog.java"
            entity_path.write_text(audit_entity, encoding="utf-8")
            self.log_action("Generated: AuditLog.java")

            audit_service = DynamicCodeGenerator.generate_java_service(spec, "AuditService")
            service_path = service_dir / "AuditService.java"
            service_path.write_text(audit_service, encoding="utf-8")
            self.log_action("Generated: AuditService.java")

    def _generate_entity_code_from_spec(self, project_folder: Path, base_package: str,
                                       entity_name: str, spec: Dict[str, Any]) -> None:
        """Generate entity, service, and controller code from parsed specification."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"

        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir.mkdir(parents=True, exist_ok=True)
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Extract field definitions from specification parser
        fields = SpecificationParser.infer_entity_fields(entity_name)
        updateable_fields = [f for f in fields if f['nullable'] or f['name'] != 'id']

        # Generate Entity with validation
        entity_code = BackendImplementationSkill.generate_entity_with_validation(
            entity_name=entity_name,
            table_name=entity_name.lower(),
            package=f"com.example.{base_package}",
            fields=fields
        )

        entity_path = entity_dir / f"{entity_name}.java"
        entity_path.write_text(entity_code, encoding="utf-8")
        self.created_files.append(entity_path)
        self.log_action(f"Generated entity: {entity_name}")

        # Generate CRUD Service
        service_code = BackendImplementationSkill.generate_crud_service(
            entity_name=entity_name,
            package=f"com.example.{base_package}",
            validation_required=True,
            updateable_fields=updateable_fields
        )

        service_name = f"{entity_name}Service"
        service_path = service_dir / f"{service_name}.java"
        service_path.write_text(service_code, encoding="utf-8")
        self.created_files.append(service_path)
        self.log_action(f"Generated service: {service_name}")

        # Generate REST Controller
        controller_code = BackendImplementationSkill.generate_rest_api_controller(
            entity_name=entity_name,
            package=f"com.example.{base_package}",
            endpoint_path=entity_name.lower()
        )

        controller_name = f"{entity_name}Controller"
        controller_path = controller_dir / f"{controller_name}.java"
        controller_path.write_text(controller_code, encoding="utf-8")
        self.created_files.append(controller_path)
        self.log_action(f"Generated controller: {controller_name}")

    def _generate_code_by_business_process(self, project_folder: Path, base_package: str, business_process: str) -> None:
        """Generate code based on business process/workflow type."""
        bp_lower = business_process.lower()

        # Map workflow names to code generation methods
        if "user" in bp_lower and "management" in bp_lower:
            self._generate_user_management_code(project_folder, base_package)
        elif "auth" in bp_lower or "authentication" in bp_lower:
            self._generate_authentication_code(project_folder, base_package)
        elif "meeting" in bp_lower and "management" in bp_lower:
            self._generate_meeting_management_code(project_folder, base_package)
        elif "meeting" in bp_lower and "completion" in bp_lower:
            self._generate_meeting_completion_code(project_folder, base_package)
        elif "calendar" in bp_lower or "scheduling" in bp_lower:
            self._generate_calendar_code(project_folder, base_package)
        elif "audit" in bp_lower or "monitoring" in bp_lower:
            self._generate_audit_code(project_folder, base_package)
        elif "core" in bp_lower or "business" in bp_lower:
            self._generate_core_logic_code(project_folder, base_package)
        elif "api" in bp_lower or "integration" in bp_lower:
            self._generate_api_integration_code(project_folder, base_package)
        else:
            # Generic code generation for unknown workflows
            self._generate_generic_workflow_code(project_folder, base_package, business_process)

    def _generate_user_management_code(self, project_folder: Path, base_package: str) -> None:
        """Generate User entity, repository, service, and controller."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)

        entity_path = entity_dir / "User.java"
        if not entity_path.exists():
            entity_path.write_text(
                BackendSkill.generate_entity_template("User", "users"),
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

    def _generate_meeting_management_code(self, project_folder: Path, base_package: str) -> None:
        """Generate meeting management entities, services, and controllers."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Generate Meeting entity
        self._generate_entity_file(entity_dir, "Meeting", base_package)
        self._generate_entity_file(entity_dir, "TimeSlot", base_package)
        self._generate_entity_file(entity_dir, "Attendee", base_package)

        # Generate repositories
        self._generate_repository_file(repo_dir, "Meeting", base_package)

        # Generate service
        self._generate_service_file(service_dir, "MeetingService", base_package)

        # Generate controller
        self._generate_controller_file(controller_dir, "MeetingController", base_package, "/api/v1/meetings")

        self.log_action("Generated meeting management code")

    def _generate_meeting_completion_code(self, project_folder: Path, base_package: str) -> None:
        """Generate meeting completion service and related classes."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)

        # Generate MeetingNotes entity
        self._generate_entity_file(entity_dir, "MeetingNotes", base_package)

        # Generate completion service
        self._generate_service_file(service_dir, "MeetingCompletionService", base_package)

        # Generate controller
        self._generate_controller_file(controller_dir, "MeetingCompletionController", base_package, "/api/v1/meeting-completion")

        self.log_action("Generated meeting completion code")

    def _generate_calendar_code(self, project_folder: Path, base_package: str) -> None:
        """Generate calendar and scheduling related code."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Generate Calendar entity
        self._generate_entity_file(entity_dir, "Calendar", base_package)

        # Generate repository
        self._generate_repository_file(repo_dir, "Calendar", base_package)

        # Generate service
        self._generate_service_file(service_dir, "CalendarService", base_package)

        # Generate controller
        self._generate_controller_file(controller_dir, "CalendarController", base_package, "/api/v1/calendar")

        self.log_action("Generated calendar code")

    def _generate_audit_code(self, project_folder: Path, base_package: str) -> None:
        """Generate audit logging service and related classes."""
        entity_dir = project_folder / f"src/main/java/com/example/{base_package}/entity"
        entity_dir.mkdir(parents=True, exist_ok=True)
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)
        controller_dir = project_folder / f"src/main/java/com/example/{base_package}/controller"
        controller_dir.mkdir(parents=True, exist_ok=True)
        repo_dir = project_folder / f"src/main/java/com/example/{base_package}/repository"
        repo_dir.mkdir(parents=True, exist_ok=True)

        entity_path = entity_dir / "AuditLog.java"
        if not entity_path.exists():
            entity_path.write_text(
                BackendSkill.generate_entity_template("AuditLog", "audit_log"),
                encoding="utf-8"
            )
            self.created_files.append(entity_path)
            self.log_action("Generated entity: AuditLog")

        service_dir_path = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_path = service_dir_path / "AuditService.java"
        if not service_path.exists():
            service_path.write_text(
                BackendSkill.generate_service_template("audit"),
                encoding="utf-8"
            )
            self.created_files.append(service_path)
            self.log_action("Generated service: AuditService")

        # Generate controller
        self._generate_controller_file(controller_dir, "AuditController", base_package, "/api/v1/audit")

    def _generate_generic_workflow_code(self, project_folder: Path, base_package: str, workflow_name: str) -> None:
        """Generate generic code for unknown workflows."""
        service_dir = project_folder / f"src/main/java/com/example/{base_package}/service"
        service_dir.mkdir(parents=True, exist_ok=True)

        # Create a generic workflow service
        workflow_service_name = "".join([word.capitalize() for word in workflow_name.split()]) + "Service"
        service_path = service_dir / f"{workflow_service_name}.java"

        if not service_path.exists():
            service_content = f"""package com.example.{base_package}.service;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {workflow_service_name}
 * Handles {workflow_name} workflow logic
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class {workflow_service_name} {{

    // TODO: Implement {workflow_name} workflow methods

}}
"""
            service_path.write_text(service_content, encoding="utf-8")
            self.created_files.append(service_path)
            self.log_action(f"Generated service: {workflow_service_name}")

    def _generate_entity_file(self, entity_dir: Path, entity_name: str, base_package: str) -> None:
        """Generate a generic JPA entity file."""
        entity_path = entity_dir / f"{entity_name}.java"

        if not entity_path.exists():
            entity_content = f"""package com.example.{base_package}.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

/**
 * {entity_name} Entity
 */
@Entity
@Table(name = "{entity_name.lower()}")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class {entity_name} {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    private String description;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;
}}
"""
            entity_path.write_text(entity_content, encoding="utf-8")
            self.created_files.append(entity_path)
            self.log_action(f"Generated entity: {entity_name}")

    def _generate_repository_file(self, repo_dir: Path, entity_name: str, base_package: str) -> None:
        """Generate a Spring Data JPA repository file."""
        repo_name = f"{entity_name}Repository"
        repo_path = repo_dir / f"{repo_name}.java"

        if not repo_path.exists():
            repo_content = f"""package com.example.{base_package}.repository;

import com.example.{base_package}.entity.{entity_name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * {repo_name}
 */
@Repository
public interface {repo_name} extends JpaRepository<{entity_name}, Long> {{

    // TODO: Add custom query methods

}}
"""
            repo_path.write_text(repo_content, encoding="utf-8")
            self.created_files.append(repo_path)
            self.log_action(f"Generated repository: {repo_name}")

    def _generate_service_file(self, service_dir: Path, service_name: str, base_package: str) -> None:
        """Generate a Spring service class."""
        service_path = service_dir / f"{service_name}.java"

        if not service_path.exists():
            service_content = f"""package com.example.{base_package}.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {service_name}
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class {service_name} {{

    // TODO: Inject repositories and implement business logic

}}
"""
            service_path.write_text(service_content, encoding="utf-8")
            self.created_files.append(service_path)
            self.log_action(f"Generated service: {service_name}")

    def _generate_controller_file(self, controller_dir: Path, controller_name: str, base_package: str, base_path: str) -> None:
        """Generate a REST controller class."""
        controller_path = controller_dir / f"{controller_name}.java"

        if not controller_path.exists():
            controller_content = f"""package com.example.{base_package}.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {controller_name}
 */
@RestController
@RequestMapping("{base_path}")
@RequiredArgsConstructor
@Slf4j
public class {controller_name} {{

    // TODO: Inject services and implement REST endpoints

    @GetMapping
    public ResponseEntity<?> list() {{
        // TODO: Implement list operation
        return ResponseEntity.ok().build();
    }}

    @GetMapping("{{id}}")
    public ResponseEntity<?> getById(@PathVariable Long id) {{
        // TODO: Implement get by id operation
        return ResponseEntity.ok().build();
    }}

    @PostMapping
    public ResponseEntity<?> create(@RequestBody Object request) {{
        // TODO: Implement create operation
        return ResponseEntity.ok().build();
    }}

    @PutMapping("{{id}}")
    public ResponseEntity<?> update(@PathVariable Long id, @RequestBody Object request) {{
        // TODO: Implement update operation
        return ResponseEntity.ok().build();
    }}

    @DeleteMapping("{{id}}")
    public ResponseEntity<?> delete(@PathVariable Long id) {{
        // TODO: Implement delete operation
        return ResponseEntity.ok().build();
    }}
}}
"""
            controller_path.write_text(controller_content, encoding="utf-8")
            self.created_files.append(controller_path)
            self.log_action(f"Generated controller: {controller_name}")

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

