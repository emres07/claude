"""
Main entry point for the multi-agent task management system.

This script orchestrates the agent team to create tasks and subtasks from projects.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

from agents import (
    TaskCreatorAgent,
    BackendAgent,
    FrontendAgent,
    DatabaseAgent,
)


class AgentTeamOrchestrator:
    """Orchestrates the multi-agent team."""

    def __init__(self, config_path: str = "agent_team_config.json"):
        """Initialize the orchestrator with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()

        self.task_creator = TaskCreatorAgent()
        self.backend_agent = BackendAgent()
        self.frontend_agent = FrontendAgent()
        self.database_agent = DatabaseAgent()

        self.created_tasks = {"tasks": [], "backend": [], "frontend": [], "database": []}
        self.projects: List[Dict[str, Any]] = []

    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {}

    def load_projects(self, projects_file: str = None) -> List[Dict[str, Any]]:
        """Load projects from JSON file."""
        if projects_file is None:
            projects_file = self.config.get("projects", {}).get("input_file", "projects.json")

        projects_path = Path(projects_file)
        if projects_path.exists():
            with open(projects_path) as f:
                self.projects = json.load(f)
                print(f"[OK] Loaded {len(self.projects)} projects from {projects_file}\n")
                return self.projects
        else:
            print(f"[WARN] No projects file found at {projects_file}")
            return []

    def add_project(self, name: str, description: str, priority: str = "medium",
                   domains: List[str] = None) -> Dict[str, Any]:
        """Add a project to the processing queue."""
        if domains is None:
            domains = ["backend", "frontend", "database"]

        project = {
            "name": name,
            "description": description,
            "priority": priority,
            "domains": domains,
        }
        self.projects.append(project)
        return project

    def process_project(self, project: Dict[str, Any]) -> None:
        """Process a single project by breaking it into business process tasks."""
        print(f"\n{'='*70}")
        print(f"Processing Project: {project['name']}")
        print(f"Priority: {project.get('priority', 'medium').upper()}")
        print(f"Description: {project['description']}")
        print(f"{'='*70}\n")

        # Task Creator Agent: Break project into business process tasks
        print("[*] Task Creator Agent is breaking project into business processes...")
        tasks = self.task_creator.create_tasks_from_project(
            project_name=project['name'],
            project_description=project['description'],
            priority=project.get('priority', 'medium'),
            domains=project.get('domains', ['backend', 'frontend', 'database']),
        )

        # Save all main tasks
        main_task_files = []
        for task in tasks:
            task_file = self.task_creator.save_task(task)
            main_task_files.append(task_file)
            self.created_tasks["tasks"].append(task_file)
            print(f"  [OK] Business process task created: {task['title']}")

        print()

        # Process each business process task with all domain agents
        for task in tasks:
            self._process_business_process_task(task, project)

    def _process_business_process_task(self, task: Dict[str, Any], project: Dict[str, Any]) -> None:
        """Process a business process task by having all domain agents create their subtasks."""
        project_name = project['name']
        domains = task.get("domains", ["backend", "frontend", "database"])

        print(f"\n{'='*70}")
        print(f"Business Process: {task['title']}")
        print(f"Domains: {', '.join([d.upper() for d in domains])}")
        print(f"{'='*70}\n")

        # Clarify task description
        print("[CHECK] Clarifying business process requirements...")
        clarified_task = self.database_agent.clarify_task_description(task)
        print(f"  [OK] Requirements clarified\n")

        # Backend Agent creates subtask for this business process
        if "backend" in domains:
            print("[TOOL] Backend Agent is creating implementation subtask...")
            try:
                backend_subtask_list = self.backend_agent.create_subtasks_from_task(
                    task_id=task["id"],
                    task_title=task["title"],
                )
                backend_subtask = backend_subtask_list[0] if backend_subtask_list else None
                if backend_subtask:
                    subtask_file = self.backend_agent.save_subtask(backend_subtask)
                    self.created_tasks["backend"].append(subtask_file)
                    print(f"  [OK] {backend_subtask['title']}")

                    # Generate backend code for this business process
                    self.backend_agent.generate_project_structure(project_name, [backend_subtask])
                    print(f"  [OK] Backend code generated\n")
            except Exception as e:
                print(f"  [ERROR] Backend error: {str(e)}\n")

        # Frontend Agent creates subtask for this business process
        if "frontend" in domains:
            print("[ART] Frontend Agent is creating implementation subtask...")
            try:
                frontend_subtask_list = self.frontend_agent.create_subtasks_from_task(
                    task_id=task["id"],
                    task_title=task["title"],
                )
                frontend_subtask = frontend_subtask_list[0] if frontend_subtask_list else None
                if frontend_subtask:
                    subtask_file = self.frontend_agent.save_subtask(frontend_subtask)
                    self.created_tasks["frontend"].append(subtask_file)
                    print(f"  [OK] {frontend_subtask['title']}")

                    # Generate frontend code for this business process
                    self.frontend_agent.generate_project_structure(project_name, [frontend_subtask])
                    print(f"  [OK] Frontend code generated\n")
            except Exception as e:
                print(f"  [ERROR] Frontend error: {str(e)}\n")

        # Database Agent creates subtask for this business process
        if "database" in domains:
            print("[DB] Database Agent is creating implementation subtask...")
            try:
                database_subtask_list = self.database_agent.create_subtasks_from_task(
                    task_id=task["id"],
                    task_title=task["title"],
                )
                database_subtask = database_subtask_list[0] if database_subtask_list else None
                if database_subtask:
                    subtask_file = self.database_agent.save_subtask(database_subtask)
                    self.created_tasks["database"].append(subtask_file)
                    print(f"  [OK] {database_subtask['title']}")

                    # Generate database code for this business process
                    self.database_agent.generate_project_structure(project_name, [database_subtask])
                    print(f"  [OK] Database code generated\n")
            except Exception as e:
                print(f"  [ERROR] Database error: {str(e)}\n")

    def process_all_projects(self) -> None:
        """Process all projects through the agent team."""
        if not self.projects:
            print("[WARN] No projects to process!")
            return

        print(f"\n{'='*70}")
        print(f"[>>] STARTING AGENT TEAM PROCESSING FOR {len(self.projects)} PROJECT(S)")
        print(f"{'='*70}\n")

        for project in self.projects:
            try:
                self.process_project(project)
            except Exception as e:
                print(f"[ERROR] Error processing project '{project.get('name', 'Unknown')}': {str(e)}")
                import traceback
                traceback.print_exc()
                continue

        print(f"\n{'='*70}")
        print(f"[YES] ALL PROJECTS PROCESSED SUCCESSFULLY")
        print(f"{'='*70}\n")

    def organize_outputs(self) -> None:
        """Organize all outputs and create summary."""
        print(f"\n{'='*60}")
        print("Organizing all outputs...")
        print(f"{'='*60}\n")

        # Aggregate files from all agents
        all_agents_files = (
            self.task_creator.get_created_files() +
            self.backend_agent.get_created_files() +
            self.frontend_agent.get_created_files() +
            self.database_agent.get_created_files()
        )

        summary_file = self.database_agent.organize_and_save_summary(
            all_tasks=self.created_tasks,
            output_folder=".",
        )
        print(f"[OK] Project summary created: {summary_file}")

    def publish_to_github(self, repo_url: str = None) -> None:
        """Prepare for GitHub publishing."""
        print(f"\n{'='*60}")
        print("GitHub Publishing")
        print(f"{'='*60}\n")

        # Aggregate files from all agents for commit
        all_files = (
            self.task_creator.get_created_files() +
            self.backend_agent.get_created_files() +
            self.frontend_agent.get_created_files() +
            self.database_agent.get_created_files()
        )

        commit_data = self.database_agent.prepare_github_commit()
        commit_data["files"] = all_files

        print(f"Commit Message: {commit_data['commit_message']}")
        print(f"Files to commit: {len(commit_data['files'])}")
        print(f"Timestamp: {commit_data['timestamp']}")

        if repo_url:
            print(f"\nTo push to GitHub:")
            print(f"  1. git init")
            print(f"  2. git add .")
            print(f"  3. git commit -m '{commit_data['commit_message']}'")
            print(f"  4. git remote add origin {repo_url}")
            print(f"  5. git push -u origin main")
        else:
            print("\nNote: Provide GitHub repo URL with --github-repo to see push commands")

    def print_summary(self) -> None:
        """Print execution summary."""
        print(f"\n{'='*60}")
        print("EXECUTION SUMMARY")
        print(f"{'='*60}\n")

        print(f"Tasks created: {len(self.created_tasks['tasks'])}")
        print(f"Backend subtasks: {len(self.created_tasks['backend'])}")
        print(f"Frontend subtasks: {len(self.created_tasks['frontend'])}")
        print(f"Database subtasks: {len(self.created_tasks['database'])}")

        print(f"\n[DIR] Output folders:")
        print(f"  • tasks/")
        print(f"  • subtasks/backend/")
        print(f"  • subtasks/frontend/")
        print(f"  • subtasks/database/")


def get_interactive_project_input() -> Dict[str, Any]:
    """Get project input interactively from user."""
    print("\n" + "="*70)
    print("[>>] AGENT TEAM PROJECT INPUT")
    print("="*70 + "\n")

    # Get project name
    name = input("📝 Project name: ").strip()
    if not name:
        print("[ERROR] Project name cannot be empty!")
        return None

    # Get description
    description = input("📝 Project description: ").strip()
    if not description:
        description = name

    # Get priority
    print("\n⭐ Select priority:")
    print("  1. Low")
    print("  2. Medium (default)")
    print("  3. High")
    priority_input = input("Choose (1-3) [default: 2]: ").strip()
    priority_map = {"1": "low", "2": "medium", "3": "high"}
    priority = priority_map.get(priority_input, "medium")

    # Get domains
    print("\n[TOOL] Select domains (comma-separated or all):")
    print("  backend   - Java, Spring Boot, Hibernate, Maven")
    print("  frontend  - React, Next.js, Vite, TypeScript, Axios")
    print("  database  - Oracle, PL/SQL, Schema, CRUD")
    print("  all       - Include all domains (default)")
    domains_input = input("Choose [default: all]: ").strip().lower()

    if not domains_input or domains_input == "all":
        domains = ["backend", "frontend", "database"]
    else:
        domains = [d.strip() for d in domains_input.split(",") if d.strip()]
        valid_domains = {"backend", "frontend", "database"}
        domains = [d for d in domains if d in valid_domains]
        if not domains:
            domains = ["backend", "frontend", "database"]

    project = {
        "name": name,
        "description": description,
        "priority": priority,
        "domains": domains,
    }

    print("\n[YES] Project configured:")
    print(f"   Name: {name}")
    print(f"   Description: {description}")
    print(f"   Priority: {priority.upper()}")
    print(f"   Domains: {', '.join(domains)}\n")

    return project


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Multi-agent task management system - Generate full-stack code from project ideas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive              - Interactive project input
  python main.py --sample                   - Run sample projects
  python main.py --projects projects.json   - Load from file
  python main.py --add-project "Project Name" --description "Details"

Each agent generates production-ready code in their folder:
  - Backend Agent → backend/  (Java, Spring Boot, Hibernate, Maven)
  - Frontend Agent → frontend/ (React, Next.js, Vite, TypeScript, Axios)
  - Database Agent → dbadmin/ (Oracle, PL/SQL, CRUD procedures)
        """,
    )
    parser.add_argument(
        "--config",
        default="agent_team_config.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode - enter project details",
    )
    parser.add_argument(
        "--projects",
        help="Path to projects JSON file",
    )
    parser.add_argument(
        "--add-project",
        help="Add a project by name",
    )
    parser.add_argument(
        "--description",
        help="Description for the project",
    )
    parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Priority for the project",
    )
    parser.add_argument(
        "--domains",
        default="backend,frontend,database",
        help="Comma-separated domains",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run with sample projects",
    )
    parser.add_argument(
        "--github-repo",
        help="GitHub repository URL",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Prepare for GitHub publishing",
    )

    args = parser.parse_args()

    # Initialize orchestrator
    orchestrator = AgentTeamOrchestrator(config_path=args.config)

    # Load projects based on input
    if args.interactive:
        project = get_interactive_project_input()
        if project:
            orchestrator.add_project(**project)
    elif args.projects:
        orchestrator.load_projects(args.projects)
    elif args.add_project:
        domains = [d.strip() for d in args.domains.split(",")]
        orchestrator.add_project(
            name=args.add_project,
            description=args.description or args.add_project,
            priority=args.priority,
            domains=domains,
        )
    elif args.sample:
        orchestrator.projects = [
            {
                "name": "User Authentication System",
                "description": "Implement comprehensive user authentication with JWT tokens, password hashing, and session management.",
                "priority": "high",
                "domains": ["backend", "frontend", "database"],
            },
            {
                "name": "Payment Processing Integration",
                "description": "Add Stripe payment integration with webhook support and transaction tracking.",
                "priority": "high",
                "domains": ["backend", "frontend", "database"],
            },
        ]
        print("[OK] Using sample projects\n")
    else:
        orchestrator.load_projects()

    # Process all projects
    if orchestrator.projects:
        print(f"\n[>>] Agents will generate code in:")
        print(f"   [DIR] backend/   - Spring Boot Java code")
        print(f"   [DIR] frontend/  - React/Next.js TypeScript code")
        print(f"   [DIR] dbadmin/   - Oracle/PL-SQL scripts\n")

        try:
            orchestrator.process_all_projects()
            orchestrator.organize_outputs()

            if args.publish or args.github_repo:
                orchestrator.publish_to_github(repo_url=args.github_repo)

            orchestrator.print_summary()
        except Exception as e:
            print(f"\n[ERROR] Error during project processing: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("[ERROR] No projects to process!")
        print("\n🎯 Usage examples:")
        print("  python main.py --interactive           # Enter project interactively")
        print("  python main.py --sample                # Run with sample projects")
        print("  python main.py --projects projects.json  # Load from file")
        print("  python main.py --add-project 'My App' --description 'Details'")


if __name__ == "__main__":
    main()
