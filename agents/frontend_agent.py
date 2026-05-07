"""Frontend Agent - Creates frontend subtasks and generates React/Next.js code."""

from typing import Any, Dict, List
from pathlib import Path

from .base_agent import BaseAgent
from skills.code_generator import DynamicCodeGenerator
from skills.detailed_subtask_generation import DetailedSubtaskGenerator
from skills.frontend_helper import FrontendSkill
from skills.frontend_implementation_skill import FrontendImplementationSkill
from skills.specification_parser import SpecificationParser


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
                "react_nextjs",
                "vite",
                "typescript",
                "axios",
                "responsive_design",
                "design_patterns",
            ],
        )
        self.code_folder = Path("frontend")
        self.code_folder.mkdir(parents=True, exist_ok=True)

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
        """Save frontend subtask to file with detailed specifications."""
        content = self.generate_metadata(
            subtask["title"],
            subtask["description"],
        )

        content += f"## Domain\nFrontend\n\n"
        content += f"## Parent Task\n{subtask['parent_task_id']}\n\n"

        # Generate detailed specifications
        details = DetailedSubtaskGenerator.generate_frontend_subtask_details(
            subtask["title"],
            subtask["description"],
            subtask.get("components", []),
            subtask.get("pages", [])
        )

        # Technical Requirements
        if details.get("technical_requirements"):
            content += "## Technical Requirements\n"
            for req in details["technical_requirements"]:
                content += f"- {req}\n"
            content += "\n"

        # Pages to Create
        if subtask["pages"]:
            content += "## Pages to Create\n"
            for page in subtask["pages"]:
                content += f"- {page}\n"
            content += "\n"

        # Component Structure
        if details.get("component_structure"):
            content += "## Component Structure\n"
            for comp in details["component_structure"]:
                content += f"- {comp}\n"
            content += "\n"

        # State Management
        if details.get("state_management"):
            content += "## State Management Strategy\n"
            state = details["state_management"]
            if isinstance(state, dict):
                for key, value in state.items():
                    if isinstance(value, list):
                        content += f"### {key.replace('_', ' ').title()}\n"
                        for item in value:
                            content += f"- {item}\n"
                    else:
                        content += f"**{key.replace('_', ' ').title()}**: {value}\n"
            content += "\n"

        # UI/UX Requirements
        if details.get("ui_ux_requirements"):
            content += "## UI/UX Requirements\n"
            for req in details["ui_ux_requirements"]:
                content += f"- {req}\n"
            content += "\n"

        # API Integration
        if details.get("api_integration"):
            content += "## API Integration Points\n"
            api = details["api_integration"]
            if isinstance(api, dict):
                for key, value in api.items():
                    if isinstance(value, list):
                        content += f"### {key.replace('_', ' ').title()}\n"
                        for item in value:
                            content += f"- {item}\n"
                    else:
                        content += f"**{key.replace('_', ' ').title()}**: `{value}`\n"
            content += "\n"

        # Performance Considerations
        if details.get("performance"):
            content += "## Performance Considerations\n"
            for perf in details["performance"]:
                content += f"- {perf}\n"
            content += "\n"

        # Testing Strategy
        if details.get("testing_strategy"):
            content += "## Testing Strategy\n"
            for test in details["testing_strategy"]:
                content += f"- {test}\n"
            content += "\n"

        # Dependencies
        if details.get("dependencies"):
            content += "## Dependencies\n"
            deps = details["dependencies"]
            if isinstance(deps, dict):
                for category, items in deps.items():
                    if items:
                        content += f"### {category.capitalize()}\n"
                        for dep in items:
                            content += f"- {dep}\n"
            content += "\n"

        # Responsive Design
        if subtask["responsive"]:
            content += "## Responsive Design\nRequired: Yes - Mobile, Tablet, Desktop\n\n"

        # Acceptance Criteria
        content += "## Acceptance Criteria\n"
        if subtask["acceptance_criteria"]:
            for criterion in subtask["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] All pages and components implemented\n"
            content += "- [ ] Responsive design working on all breakpoints\n"
            content += "- [ ] State management properly configured\n"
            content += "- [ ] API integration implemented and tested\n"
            content += "- [ ] Error handling and loading states\n"
            content += "- [ ] TypeScript types properly defined\n"
            content += "- [ ] Unit tests written (>80% coverage)\n"
            content += "- [ ] E2E tests passing\n"
            content += "- [ ] Accessibility (WCAG 2.1 AA) validated\n"
            content += "- [ ] Performance optimized\n"
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
            f"Created detailed frontend subtask for {subtask['parent_task_id']}: {subtask['title']}"
        )
        return str(filepath)

    def create_subtasks_from_task(
        self,
        task_id: str,
        task_title: str,
        task: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """Create frontend subtasks specific to the business process or workflow."""
        # Check if this is a workflow-based task
        workflow = None
        if task and "workflow" in task:
            workflow = task["workflow"]

        # Map business processes to frontend technical specifications
        business_process = task_title.split(" - ")[0]  # Extract business process name

        subtask_specs = {
            "User Management": {
                "title": "User Management UI Components",
                "description": "Create user registration form, user profile page, user list component with search/filter, and user edit form with validation",
                "components": ["RegistrationForm", "UserProfile", "UserList", "UserEditForm"],
                "pages": ["Users", "UserProfile"],
                "responsive": True,
            },
            "Authentication & Authorization": {
                "title": "Authentication Pages & Components",
                "description": "Build login form, logout button, password reset form, role-based UI elements, and protected route components with proper redirects",
                "components": ["LoginForm", "LogoutButton", "PasswordResetForm", "ProtectedRoute"],
                "pages": ["Login", "Logout", "PasswordReset"],
                "responsive": True,
            },
            "Core Business Logic": {
                "title": "Core Feature Components & Pages",
                "description": "Create main feature components, dashboard page with business metrics, workflow components, and data display components",
                "components": ["Dashboard", "DataTable", "FormComponents", "StatusIndicator"],
                "pages": ["Dashboard", "Resources"],
                "responsive": True,
            },
            "API & Integration": {
                "title": "API Integration & Data Management",
                "description": "Create API service client with error handling, state management hooks, data fetching components, and real-time update listeners",
                "components": ["ApiService", "DataFetcher", "ErrorBoundary", "LoadingSpinner"],
                "pages": ["Loading", "Error"],
                "responsive": True,
            },
            "Audit & Monitoring": {
                "title": "Audit & Monitoring Dashboard",
                "description": "Build audit log viewer, activity timeline, analytics dashboard with charts, and report generation components",
                "components": ["AuditLog", "Timeline", "Analytics", "ChartComponent"],
                "pages": ["Audit", "Reports", "Analytics"],
                "responsive": True,
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
            description = f"Implement frontend for {workflow_name} workflow.\n\n"
            description += f"Workflow Steps:\n"
            for i, step in enumerate(workflow_steps, 1):
                description += f"{i}. {step}\n"
            description += f"\nFeatures to implement: {', '.join(workflow_features)}\n"
            description += f"Data entities to work with: {', '.join(workflow_data_entities)}"

            # Generate component names from workflow features
            components = [feature.replace('_', ' ').title() for feature in workflow_features]

            # Generate page names from workflow name
            pages = [workflow_name.replace(' ', '')]

            spec = {
                "title": f"Frontend Implementation for {workflow_name}",
                "description": description,
                "components": components,
                "pages": pages,
                "responsive": True,
            }
        else:
            # Fall back to business process specifications
            spec = subtask_specs.get(business_process, {
                "title": f"Frontend Implementation for {business_process}",
                "description": f"Implement frontend components and pages for {business_process}",
                "components": [business_process.replace(" ", "")],
                "pages": [business_process.replace(" ", "")],
                "responsive": True,
            })

        subtask = self.create_frontend_subtask(
            task_id=task_id,
            title=f"{spec['title']} - {task_title}",
            description=spec["description"],
            components=spec.get("components", []),
            pages=spec.get("pages", []),
            responsive=spec.get("responsive", True),
        )

        # Store business process/workflow name for code generation
        subtask["business_process"] = business_process
        if workflow:
            subtask["workflow"] = workflow

        return [subtask]

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None) -> None:
        """Generate Next.js project structure based on business process subtasks."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Setup base project structure on first business process
        if subtasks:
            self._setup_base_project(project_folder, project_name)

            for subtask in subtasks:
                self._generate_subtask_code(project_folder, subtask, project_name)

            # Generate subtask documentation
            self._generate_subtask_documentation(project_folder, subtasks)

        self.log_action(f"Frontend project structure created: {project_name}")

    def _setup_base_project(self, project_folder: Path, project_name: str) -> None:
        """Setup base Next.js project structure."""
        # Create package.json if it doesn't exist
        package_json_path = project_folder / "package.json"
        if not package_json_path.exists():
            package_json_path.write_text(
                FrontendSkill.generate_package_json(project_name),
                encoding="utf-8"
            )
            self.created_files.append(package_json_path)
            self.log_action(f"Generated package.json for {project_name}")

        # Create tsconfig.json if it doesn't exist
        tsconfig_path = project_folder / "tsconfig.json"
        if not tsconfig_path.exists():
            tsconfig_path.write_text(
                FrontendSkill.generate_tsconfig(),
                encoding="utf-8"
            )
            self.created_files.append(tsconfig_path)
            self.log_action(f"Generated tsconfig.json")

        # Create .eslintrc.json if it doesn't exist
        eslint_path = project_folder / ".eslintrc.json"
        if not eslint_path.exists():
            eslint_path.write_text(
                FrontendSkill.generate_eslint_config(),
                encoding="utf-8"
            )
            self.created_files.append(eslint_path)

        # Create directories
        dirs = [
            "src/components",
            "src/pages",
            "src/services",
            "src/hooks",
            "src/types",
            "src/utils",
            "src/styles",
            "public",
        ]
        for dir_name in dirs:
            (project_folder / dir_name).mkdir(parents=True, exist_ok=True)

    def _generate_subtask_code(self, project_folder: Path, subtask: Dict[str, Any],
                               project_name: str) -> None:
        """Generate code specific to each business process based on subtask specifications."""
        business_process = subtask.get("business_process", "")

        # Try to find the subtask markdown file to parse specifications
        subtask_file_path = self._find_subtask_readme(business_process, subtask.get("title", ""))

        if subtask_file_path:
            # Parse the subtask file to extract field/column information
            spec = SpecificationParser.parse_subtask_file(subtask_file_path)

            # Extract data entities from the specification
            data_entities = spec.get("data_entities", [])

            if data_entities:
                # Generate frontend code for each data entity
                for entity_name in data_entities:
                    self._generate_entity_components_from_spec(
                        project_folder, entity_name, spec
                    )
                return

        # Fall back to business process-based generation
        self._generate_code_by_business_process(project_folder, business_process)

    def _find_subtask_readme(self, business_process: str, subtask_title: str) -> str:
        """Find subtask MD file for the given business process."""
        # Look for subtask MD files in subtasks/frontend/
        subtasks_base = Path("subtasks/frontend")
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

    def _generate_entity_components_from_spec(self, project_folder: Path,
                                             entity_name: str, spec: Dict[str, Any]) -> None:
        """Generate form, list, and page components for a data entity from specification."""
        components_dir = project_folder / "src/components"
        pages_dir = project_folder / "src/pages"
        hooks_dir = project_folder / "src/hooks"

        components_dir.mkdir(parents=True, exist_ok=True)
        pages_dir.mkdir(parents=True, exist_ok=True)
        hooks_dir.mkdir(parents=True, exist_ok=True)

        # Extract form fields for this entity
        form_fields = SpecificationParser.infer_form_fields(entity_name, spec.get("workflow_features", []))
        display_fields = SpecificationParser.infer_list_display_fields(entity_name)

        # Generate Add Form Component
        form_component_name = f"Add{entity_name}"
        form_code = FrontendImplementationSkill.generate_add_form_component(
            component_name=form_component_name,
            fields=form_fields,
            api_endpoint=f"/api/v1/{entity_name.lower()}s",
            form_title=f"Add New {entity_name}",
            submit_button_text=f"Create {entity_name}"
        )

        form_path = components_dir / f"{form_component_name}.tsx"
        form_path.write_text(form_code, encoding="utf-8")
        self.created_files.append(form_path)
        self.log_action(f"Generated component: {form_component_name}")

        # Generate List Component
        list_component_name = f"{entity_name}List"
        list_code = FrontendImplementationSkill.generate_list_component(
            component_name=list_component_name,
            api_endpoint=f"/api/v1/{entity_name.lower()}s",
            endpoint_singular=entity_name.lower(),
            display_fields=display_fields
        )

        list_path = components_dir / f"{list_component_name}.tsx"
        list_path.write_text(list_code, encoding="utf-8")
        self.created_files.append(list_path)
        self.log_action(f"Generated component: {list_component_name}")

        # Generate CRUD Page
        page_name = entity_name.lower()
        crud_page_code = FrontendImplementationSkill.generate_crud_page(
            page_name=page_name,
            form_component=form_component_name,
            list_component=list_component_name
        )

        page_path = pages_dir / f"{page_name}.tsx"
        page_path.write_text(crud_page_code, encoding="utf-8")
        self.created_files.append(page_path)
        self.log_action(f"Generated page: {page_name}")

        # Generate useAPI hook (only once per project)
        hook_path = hooks_dir / "useAPI.ts"
        if not hook_path.exists():
            hook_code = FrontendImplementationSkill.generate_use_api_hook()
            hook_path.write_text(hook_code, encoding="utf-8")
            self.created_files.append(hook_path)
            self.log_action(f"Generated hook: useAPI")

    def _generate_code_from_spec(self, project_folder: Path, spec: Dict[str, Any]) -> None:
        """Generate frontend code based on parsed specification."""
        components_dir = project_folder / "src/components"
        pages_dir = project_folder / "src/pages"
        services_dir = project_folder / "src/services"

        components_dir.mkdir(parents=True, exist_ok=True)
        pages_dir.mkdir(parents=True, exist_ok=True)
        services_dir.mkdir(parents=True, exist_ok=True)

        description = spec.get("description", "").lower()

        # Generate LoginForm for authentication
        if "login" in description or "auth" in description:
            login_code = DynamicCodeGenerator.generate_react_component(spec, "LoginForm")
            login_path = components_dir / "LoginForm.tsx"
            login_path.write_text(login_code, encoding="utf-8")
            self.log_action("Generated: LoginForm.tsx")

        # Generate UserList for user management
        if "user" in description and "list" in description:
            userlist_code = DynamicCodeGenerator.generate_react_component(spec, "UserList")
            userlist_path = components_dir / "UserList.tsx"
            userlist_path.write_text(userlist_code, encoding="utf-8")
            self.log_action("Generated: UserList.tsx")

        # Generate Dashboard page
        if "dashboard" in description:
            dashboard_code = DynamicCodeGenerator.generate_react_component(spec, "Dashboard")
            dashboard_path = pages_dir / "dashboard.tsx"
            dashboard_path.write_text(dashboard_code, encoding="utf-8")
            self.log_action("Generated: dashboard.tsx")

        # Generate generic component/page for other cases
        if not description:
            generic_code = DynamicCodeGenerator.generate_react_component(spec, "Component")
            component_path = components_dir / "Component.tsx"
            component_path.write_text(generic_code, encoding="utf-8")
            self.log_action("Generated: Component.tsx")

    def _generate_code_by_business_process(self, project_folder: Path, business_process: str) -> None:
        """Generate code based on business process/workflow type."""
        bp_lower = business_process.lower()

        # Map workflow names to component generation methods
        if "user" in bp_lower and "management" in bp_lower:
            self._generate_user_management_components(project_folder)
        elif "auth" in bp_lower or "authentication" in bp_lower:
            self._generate_authentication_components(project_folder)
        elif "meeting" in bp_lower and "management" in bp_lower:
            self._generate_meeting_management_components(project_folder)
        elif "meeting" in bp_lower and "completion" in bp_lower:
            self._generate_meeting_completion_components(project_folder)
        elif "calendar" in bp_lower or "scheduling" in bp_lower:
            self._generate_calendar_components(project_folder)
        elif "audit" in bp_lower or "monitoring" in bp_lower:
            self._generate_audit_components(project_folder)
        elif "core" in bp_lower or "business" in bp_lower:
            self._generate_core_feature_components(project_folder)
        elif "api" in bp_lower or "integration" in bp_lower:
            self._generate_api_integration_components(project_folder)
        else:
            # Generic component generation for unknown workflows
            self._generate_generic_workflow_components(project_folder, business_process)

    def _generate_user_management_components(self, project_folder: Path) -> None:
        """Generate user management components and pages."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["RegistrationForm", "UserProfile", "UserList"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for page in ["users", "profile"]:
            page_path = pages_dir / f"{page}.tsx"
            if not page_path.exists():
                page_path.write_text(
                    FrontendSkill.generate_page_template(page),
                    encoding="utf-8"
                )
                self.created_files.append(page_path)
                self.log_action(f"Generated page: {page}")

    def _generate_authentication_components(self, project_folder: Path) -> None:
        """Generate authentication components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["LoginForm", "LogoutButton", "ProtectedRoute"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

    def _generate_core_feature_components(self, project_folder: Path) -> None:
        """Generate core feature components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["Dashboard", "DataTable", "FormComponents"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

    def _generate_api_integration_components(self, project_folder: Path) -> None:
        """Generate API integration components."""
        services_dir = project_folder / "src/services"
        services_dir.mkdir(parents=True, exist_ok=True)

        api_service_path = services_dir / "api.service.ts"
        if not api_service_path.exists():
            api_service_path.write_text(
                FrontendSkill.generate_api_service("api"),
                encoding="utf-8"
            )
            self.created_files.append(api_service_path)
            self.log_action("Generated API service")

        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)
        for component in ["ErrorBoundary", "LoadingSpinner"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

    def _generate_audit_components(self, project_folder: Path) -> None:
        """Generate audit and monitoring components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["AuditLog", "Timeline", "Analytics"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for page in ["audit", "reports"]:
            page_path = pages_dir / f"{page}.tsx"
            if not page_path.exists():
                page_path.write_text(
                    FrontendSkill.generate_page_template(page),
                    encoding="utf-8"
                )
                self.created_files.append(page_path)
                self.log_action(f"Generated page: {page}")

    def _generate_meeting_management_components(self, project_folder: Path) -> None:
        """Generate meeting management workflow components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["AddMeeting", "EditMeeting", "DeleteMeeting", "MeetingList"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for page in ["meetings", "meeting_details"]:
            page_path = pages_dir / f"{page}.tsx"
            if not page_path.exists():
                page_path.write_text(
                    FrontendSkill.generate_page_template(page),
                    encoding="utf-8"
                )
                self.created_files.append(page_path)
                self.log_action(f"Generated page: {page}")

    def _generate_meeting_completion_components(self, project_folder: Path) -> None:
        """Generate meeting completion workflow components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["MeetingNotes", "CompletionForm", "AttendanceTracker"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for page in ["meeting_completion", "completion_reports"]:
            page_path = pages_dir / f"{page}.tsx"
            if not page_path.exists():
                page_path.write_text(
                    FrontendSkill.generate_page_template(page),
                    encoding="utf-8"
                )
                self.created_files.append(page_path)
                self.log_action(f"Generated page: {page}")

    def _generate_calendar_components(self, project_folder: Path) -> None:
        """Generate calendar/scheduling workflow components."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["CalendarView", "TimeSlotSelector", "SchedulingForm", "AvailabilityChecker"]:
            component_path = components_dir / f"{component}.tsx"
            if not component_path.exists():
                component_path.write_text(
                    FrontendSkill.generate_component_template(component.lower()),
                    encoding="utf-8"
                )
                self.created_files.append(component_path)
                self.log_action(f"Generated component: {component}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for page in ["calendar", "scheduling"]:
            page_path = pages_dir / f"{page}.tsx"
            if not page_path.exists():
                page_path.write_text(
                    FrontendSkill.generate_page_template(page),
                    encoding="utf-8"
                )
                self.created_files.append(page_path)
                self.log_action(f"Generated page: {page}")

    def _generate_generic_workflow_components(self, project_folder: Path, business_process: str) -> None:
        """Generate generic components for unknown workflows."""
        components_dir = project_folder / "src/components"
        components_dir.mkdir(parents=True, exist_ok=True)

        # Create a generic component based on the business process name
        safe_name = business_process.replace(" ", "").replace("-", "").replace("_", "")
        component_path = components_dir / f"{safe_name}.tsx"
        if not component_path.exists():
            component_path.write_text(
                FrontendSkill.generate_component_template(safe_name.lower()),
                encoding="utf-8"
            )
            self.created_files.append(component_path)
            self.log_action(f"Generated component: {safe_name}")

        pages_dir = project_folder / "src/pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        page_name = safe_name.lower()
        page_path = pages_dir / f"{page_name}.tsx"
        if not page_path.exists():
            page_path.write_text(
                FrontendSkill.generate_page_template(page_name),
                encoding="utf-8"
            )
            self.created_files.append(page_path)
            self.log_action(f"Generated page: {page_name}")

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
- `src/components/` - React components
- `src/pages/` - Next.js pages
- `src/services/` - API services
- `package.json` - Dependencies
- `tsconfig.json` - TypeScript configuration

### Components Generated
{chr(10).join([f"- {comp}" for comp in subtask.get('components', [])])}

### Pages Generated
{chr(10).join([f"- {page}" for page in subtask.get('pages', [])])}

### Responsive Design
{"Yes" if subtask.get('responsive') else "No"}

### Acceptance Criteria
- [x] Code generated automatically
- [ ] Components tested
- [ ] Responsive design verified
- [ ] API integration working
- [ ] Code reviewed

### Next Steps
1. Review generated components and pages in main project folder
2. Customize styling and layout
3. Test responsiveness on different screens
4. Integrate with backend APIs
5. Run: `npm run dev`

### Files to Review
- All TypeScript/React files follow best practices
- Components are reusable and well-typed
- Pages use Next.js routing conventions
- API service handles error cases
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            self.log_action(f"Generated documentation for subtask {idx}: {subtask['title']}")

