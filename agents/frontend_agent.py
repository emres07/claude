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

        # Generate subtask-specific implementations
        if subtasks:
            self._generate_subtask_implementations(project_folder, subtasks)

        self.log_action(f"Frontend project structure created: {project_name}")

    def _generate_subtask_implementations(
        self, project_folder: Path, subtasks: List[Dict[str, Any]]
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

## Components/Pages
{chr(10).join([f"- {item}" for item in subtask.get('components', []) + subtask.get('pages', [])])}

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Responsive design working
- [ ] API integration complete
- [ ] Code reviewed

## Files Generated
Generated implementation files for this subtask.
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            # Subtask 1: Setup
            if idx == 1:
                self._generate_subtask_1_setup(subtask_folder)
            # Subtask 2: Base Components
            elif idx == 2:
                self._generate_subtask_2_base_components(subtask_folder)
            # Subtask 3: Feature Components
            elif idx == 3:
                self._generate_subtask_3_feature_components(subtask_folder)
            # Subtask 4: Pages
            elif idx == 4:
                self._generate_subtask_4_pages(subtask_folder)
            # Subtask 5: API Integration
            elif idx == 5:
                self._generate_subtask_5_api_integration(subtask_folder)

    def _generate_subtask_1_setup(self, subtask_folder: Path) -> None:
        """Generate Next.js setup files."""
        package_path = subtask_folder / "package.json"
        package_path.write_text(FrontendSkill.generate_package_json("setup"), encoding="utf-8")
        self.created_files.append(package_path)
        self.log_action("Generated subtask 1: Setup files")

    def _generate_subtask_2_base_components(self, subtask_folder: Path) -> None:
        """Generate base components."""
        components_dir = subtask_folder / "components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["button", "form", "card", "modal", "input"]:
            comp_path = components_dir / f"{component.title()}.tsx"
            comp_path.write_text(FrontendSkill.generate_component_template(component), encoding="utf-8")
            self.created_files.append(comp_path)

        self.log_action("Generated subtask 2: Base Components")

    def _generate_subtask_3_feature_components(self, subtask_folder: Path) -> None:
        """Generate feature components."""
        components_dir = subtask_folder / "components"
        components_dir.mkdir(parents=True, exist_ok=True)

        for component in ["user_card", "task_list", "task_form", "audit_log"]:
            comp_path = components_dir / f"{component.title()}.tsx"
            comp_path.write_text(FrontendSkill.generate_component_template(component), encoding="utf-8")
            self.created_files.append(comp_path)

        self.log_action("Generated subtask 3: Feature Components")

    def _generate_subtask_4_pages(self, subtask_folder: Path) -> None:
        """Generate pages."""
        pages_dir = subtask_folder / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)

        for page in ["dashboard", "users", "tasks", "settings", "profile"]:
            page_path = pages_dir / f"{page}.tsx"
            page_path.write_text(FrontendSkill.generate_page_template(page), encoding="utf-8")
            self.created_files.append(page_path)

        self.log_action("Generated subtask 4: Pages")

    def _generate_subtask_5_api_integration(self, subtask_folder: Path) -> None:
        """Generate API integration files."""
        services_dir = subtask_folder / "services"
        services_dir.mkdir(parents=True, exist_ok=True)

        api_path = services_dir / "api.service.ts"
        api_path.write_text(FrontendSkill.generate_api_service("api"), encoding="utf-8")
        self.created_files.append(api_path)

        self.log_action("Generated subtask 5: API Integration")

        self.log_action(f"Frontend project structure created: {project_name}")
