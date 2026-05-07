"""Frontend Agent - Creates frontend subtasks and generates React/Next.js code."""

from typing import Any, Dict, List
from pathlib import Path

from .base_agent import BaseAgent
from skills.frontend_skills import FrontendSkill


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

        # Sanitize filename by removing colons
        sanitized_id = subtask["id"].replace(":", "_")
        filepath = self.save_task_file(
            filename=sanitized_id,
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
        """Create frontend subtasks specific to the business process."""
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

        # Get specifications for this business process, or use defaults
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
        """Generate code specific to each business process."""
        # Extract business process from subtask title
        title = subtask.get("title", "")
        business_process = title.split(" - ")[0] if " - " in title else title

        if "User Management" in business_process:
            self._generate_user_management_components(project_folder)
        elif "Authentication" in business_process:
            self._generate_authentication_components(project_folder)
        elif "Core Business Logic" in business_process:
            self._generate_core_feature_components(project_folder)
        elif "API & Integration" in business_process:
            self._generate_api_integration_components(project_folder)
        elif "Audit & Monitoring" in business_process:
            self._generate_audit_components(project_folder)

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

