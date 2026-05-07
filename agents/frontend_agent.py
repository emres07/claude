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
                title=f"Setup Next.js Project - {task_title}",
                description="Initialize Next.js project with TypeScript, dependencies, and configuration",
                components=["project setup", "tsconfig", "eslint config"],
                responsive=True,
            ),
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"Create Base Components - {task_title}",
                description="Build reusable UI components (Button, Form, Card, Modal, Input)",
                components=["Button", "Form", "Card", "Modal", "Input", "Table"],
                responsive=True,
            ),
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"Build Feature Components - {task_title}",
                description="Create domain-specific components for main features",
                components=["UserCard", "TaskList", "TaskForm", "AuditLog", "FilterBar"],
                responsive=True,
            ),
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"Implement Pages & Routing - {task_title}",
                description="Create pages and setup Next.js routing",
                pages=["Dashboard", "Users", "Tasks", "Settings", "Profile"],
                responsive=True,
            ),
            self.create_frontend_subtask(
                task_id=task_id,
                title=f"API Integration & State Management - {task_title}",
                description="Connect frontend to backend APIs and setup state management",
                components=["API services", "React hooks", "Data fetching"],
                responsive=True,
            ),
        ]

        return subtasks

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None) -> None:
        """Generate complete frontend project structure with subtask-specific code."""
        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create subtasks folder for organization
        subtasks_folder = project_folder / "subtasks"
        subtasks_folder.mkdir(parents=True, exist_ok=True)

        # Create package.json
        package_json_path = project_folder / "package.json"
        package_json_path.write_text(
            FrontendSkill.generate_package_json(project_name),
            encoding="utf-8"
        )
        self.created_files.append(package_json_path)
        self.log_action(f"Generated package.json for {project_name}")

        # Create tsconfig.json
        tsconfig_path = project_folder / "tsconfig.json"
        tsconfig_path.write_text(
            FrontendSkill.generate_tsconfig(),
            encoding="utf-8"
        )
        self.created_files.append(tsconfig_path)
        self.log_action(f"Generated tsconfig.json")

        # Create .eslintrc.json
        eslint_path = project_folder / ".eslintrc.json"
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

        # Create API service
        services_dir = project_folder / "src/services"
        api_service_path = services_dir / "api.service.ts"
        api_service_path.write_text(
            FrontendSkill.generate_api_service("api"),
            encoding="utf-8"
        )
        self.created_files.append(api_service_path)
        self.log_action("Generated API service")

        # Create base components
        components_dir = project_folder / "src/components"
        base_components = ["button", "form", "card", "modal", "input"]

        for component in base_components:
            component_path = components_dir / f"{component.title()}.tsx"
            component_path.write_text(
                FrontendSkill.generate_component_template(component),
                encoding="utf-8"
            )
            self.created_files.append(component_path)
            self.log_action(f"Generated component: {component.title()}")

        # Create feature components
        feature_components = ["UserCard", "TaskList", "TaskForm", "AuditLog"]

        for component in feature_components:
            component_path = components_dir / f"{component}.tsx"
            component_path.write_text(
                FrontendSkill.generate_component_template(component.lower()),
                encoding="utf-8"
            )
            self.created_files.append(component_path)
            self.log_action(f"Generated component: {component}")

        # Create pages
        pages_dir = project_folder / "src/pages"
        pages = ["dashboard", "users", "tasks", "settings", "profile"]

        for page in pages:
            page_path = pages_dir / f"{page}.tsx"
            page_path.write_text(
                FrontendSkill.generate_page_template(page),
                encoding="utf-8"
            )
            self.created_files.append(page_path)
            self.log_action(f"Generated page: {page}")

        # Create setup script
        setup_script = project_folder / "setup.sh"
        setup_script.write_text(
            FrontendSkill.generate_setup_script(),
            encoding="utf-8"
        )
        self.created_files.append(setup_script)

        # Generate subtask documentation only (code is already in main folder)
        if subtasks:
            self._generate_subtask_documentation(project_folder, subtasks)

        self.log_action(f"Frontend project structure created: {project_name}")

    def _generate_subtask_documentation(
        self, project_folder: Path, subtasks: List[Dict[str, Any]]
    ) -> None:
        """Generate documentation for each subtask (code is in main folder)."""
        subtasks_folder = project_folder / "subtasks"
        subtasks_folder.mkdir(parents=True, exist_ok=True)

        for idx, subtask in enumerate(subtasks, 1):
            subtask_name = subtask["title"].lower().replace(" - ", "_").replace(" ", "_").replace("&", "")
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

