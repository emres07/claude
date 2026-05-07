"""
Main entry point for the multi-agent task management system.

This script orchestrates the agent team to create tasks and subtasks.
"""

import json
import argparse
from pathlib import Path

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

    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {}

    def create_sample_task(self) -> dict:
        """Create a sample task for demonstration."""
        task = self.task_creator.create_main_task(
            title="Implement User Authentication System",
            description="Add comprehensive user authentication with JWT tokens, password hashing, and session management.",
            priority="high",
            domains=["backend", "frontend", "database"],
            acceptance_criteria=[
                "Users can register with email",
                "Users can login securely",
                "JWT tokens are generated and validated",
                "Password reset functionality works",
                "Session management is secure",
            ],
        )
        return task

    def process_task(self, task: dict) -> None:
        """Process a task through the agent team."""
        print(f"\n{'='*60}")
        print(f"Processing Task: {task['title']}")
        print(f"{'='*60}\n")

        # Save main task
        task_file = self.task_creator.save_task(task)
        self.created_tasks["tasks"].append(task_file)
        print(f"✓ Main task saved: {task_file}\n")

        # Create backend subtasks
        print("Creating backend subtasks...")
        backend_subtasks = self.backend_agent.create_subtasks_from_task(
            task_id=task["id"],
            task_title=task["title"],
        )
        for subtask in backend_subtasks:
            subtask_file = self.backend_agent.save_subtask(subtask)
            self.created_tasks["backend"].append(subtask_file)
            print(f"  ✓ {subtask['title']}")

        # Create frontend subtasks
        print("\nCreating frontend subtasks...")
        frontend_subtasks = self.frontend_agent.create_subtasks_from_task(
            task_id=task["id"],
            task_title=task["title"],
        )
        for subtask in frontend_subtasks:
            subtask_file = self.frontend_agent.save_subtask(subtask)
            self.created_tasks["frontend"].append(subtask_file)
            print(f"  ✓ {subtask['title']}")

        # Create database subtasks
        print("\nCreating database subtasks...")
        database_subtasks = self.database_agent.create_subtasks_from_task(
            task_id=task["id"],
            task_title=task["title"],
        )
        for subtask in database_subtasks:
            subtask_file = self.database_agent.save_subtask(subtask)
            self.created_tasks["database"].append(subtask_file)
            print(f"  ✓ {subtask['title']}")

        # Clarify task
        print("\nClarifying task description...")
        clarified_task = self.database_agent.clarify_task_description(task)
        print(f"  ✓ Task clarified and validated")

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
        description="Multi-agent task management system",
    )
    parser.add_argument(
        "--config",
        default="agent_team_config.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--task-title",
        help="Title for the main task",
        default="Implement User Authentication System",
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

    # Create and process sample task
    task = orchestrator.create_sample_task()
    orchestrator.process_task(task)

    # Organize outputs
    orchestrator.organize_outputs()

    # GitHub publishing
    if args.publish or args.github_repo:
        orchestrator.publish_to_github(repo_url=args.github_repo)

    # Print summary
    orchestrator.print_summary()


if __name__ == "__main__":
    main()
