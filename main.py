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
                print(f"✓ Loaded {len(self.projects)} projects from {projects_file}\n")
                return self.projects
        else:
            print(f"⚠ No projects file found at {projects_file}")
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
        """Process a single project through all agents."""
        print(f"\n{'='*60}")
        print(f"Processing Project: {project['name']}")
        print(f"Priority: {project.get('priority', 'medium').upper()}")
        print(f"{'='*60}\n")

        # Task Creator Agent: Create main task from project
        print("📋 Task Creator Agent is working...")
        task = self.task_creator.create_main_task(
            title=project['name'],
            description=project['description'],
            priority=project.get('priority', 'medium'),
            domains=project.get('domains', ['backend', 'frontend', 'database']),
            acceptance_criteria=[],
        )

        task_file = self.task_creator.save_task(task)
        self.created_tasks["tasks"].append(task_file)
        print(f"  ✓ Main task created: {project['name']}\n")

        # Clarify task description (Database Agent responsibility)
        print("🔍 Database Agent is clarifying requirements...")
        clarified_task = self.database_agent.clarify_task_description(task)
        print(f"  ✓ Task requirements clarified\n")

        # Backend Agent: Create backend subtasks
        if "backend" in project.get('domains', []):
            print("🔧 Backend Agent is creating subtasks...")
            backend_subtasks = self.backend_agent.create_subtasks_from_task(
                task_id=task["id"],
                task_title=task["title"],
            )
            for subtask in backend_subtasks:
                subtask_file = self.backend_agent.save_subtask(subtask)
                self.created_tasks["backend"].append(subtask_file)
                print(f"  ✓ {subtask['title']}")
            print()

        # Frontend Agent: Create frontend subtasks
        if "frontend" in project.get('domains', []):
            print("🎨 Frontend Agent is creating subtasks...")
            frontend_subtasks = self.frontend_agent.create_subtasks_from_task(
                task_id=task["id"],
                task_title=task["title"],
            )
            for subtask in frontend_subtasks:
                subtask_file = self.frontend_agent.save_subtask(subtask)
                self.created_tasks["frontend"].append(subtask_file)
                print(f"  ✓ {subtask['title']}")
            print()

        # Database Agent: Create database subtasks
        if "database" in project.get('domains', []):
            print("💾 Database Agent is creating subtasks...")
            database_subtasks = self.database_agent.create_subtasks_from_task(
                task_id=task["id"],
                task_title=task["title"],
            )
            for subtask in database_subtasks:
                subtask_file = self.database_agent.save_subtask(subtask)
                self.created_tasks["database"].append(subtask_file)
                print(f"  ✓ {subtask['title']}")
            print()

        print(f"✅ Project '{project['name']}' processing complete!\n")

    def process_all_projects(self) -> None:
        """Process all projects through the agent team."""
        if not self.projects:
            print("⚠ No projects to process!")
            return

        print(f"\n{'='*70}")
        print(f"🚀 STARTING AGENT TEAM PROCESSING FOR {len(self.projects)} PROJECT(S)")
        print(f"{'='*70}\n")

        for project in self.projects:
            self.process_project(project)

        print(f"\n{'='*70}")
        print(f"✅ ALL PROJECTS PROCESSED SUCCESSFULLY")
        print(f"{'='*70}\n")

    def organize_outputs(self) -> None:
        """Organize all outputs and create summary."""
        print(f"\n{'='*60}")
        print("Organizing all outputs...")
        print(f"{'='*60}\n")

        summary_file = self.database_agent.organize_and_save_summary(
            all_tasks=self.created_tasks,
            output_folder=".",
        )
        print(f"✓ Project summary created: {summary_file}")

    def publish_to_github(self, repo_url: str = None) -> None:
        """Prepare for GitHub publishing."""
        print(f"\n{'='*60}")
        print("GitHub Publishing")
        print(f"{'='*60}\n")

        commit_data = self.database_agent.prepare_github_commit()

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

        print(f"\n📁 Output folders:")
        print(f"  • tasks/")
        print(f"  • subtasks/backend/")
        print(f"  • subtasks/frontend/")
        print(f"  • subtasks/database/")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Multi-agent task management system - Process projects with specialized agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --projects projects.json
  python main.py --add-project "Project Name" --description "Project description"
  python main.py --projects projects.json --publish --github-repo https://github.com/user/repo.git
        """,
    )
    parser.add_argument(
        "--config",
        default="agent_team_config.json",
        help="Path to configuration file (default: agent_team_config.json)",
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
        help="Description for the project (used with --add-project)",
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
        help="Comma-separated domains (backend,frontend,database)",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run with sample projects",
    )
    parser.add_argument(
        "--github-repo",
        help="GitHub repository URL for publishing",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Prepare for GitHub publishing",
    )

    args = parser.parse_args()

    # Initialize orchestrator
    orchestrator = AgentTeamOrchestrator(config_path=args.config)

    # Load projects
    if args.projects:
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
        print("✓ Using sample projects\n")
    else:
        orchestrator.load_projects()

    # Process all projects
    if orchestrator.projects:
        orchestrator.process_all_projects()
        orchestrator.organize_outputs()

        if args.publish or args.github_repo:
            orchestrator.publish_to_github(repo_url=args.github_repo)

        orchestrator.print_summary()
    else:
        print("❌ No projects to process!")
        print("\nUsage examples:")
        print("  python main.py --sample")
        print("  python main.py --projects projects.json")
        print("  python main.py --add-project 'My Project' --description 'Project details'")


if __name__ == "__main__":
    main()
