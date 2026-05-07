"""Base agent class for the multi-agent system."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class BaseAgent:
    """Base class for all agents in the team."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        output_folder: str,
        skills: Optional[List[str]] = None,
    ):
        """Initialize agent with configuration."""
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.output_folder = Path(output_folder)
        self.skills = skills or []
        self.created_files: List[Path] = []

        # Ensure output folder exists
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def save_task_file(
        self,
        filename: str,
        content: str,
        task_id: Optional[str] = None,
    ) -> Path:
        """Save task or subtask to file."""
        if task_id:
            filepath = self.output_folder / f"{task_id}_{filename}.md"
        else:
            filepath = self.output_folder / f"{filename}.md"

        filepath.write_text(content, encoding="utf-8")
        self.created_files.append(filepath)
        return filepath

    def generate_metadata(self, title: str, description: str = "") -> str:
        """Generate metadata header for task files."""
        return (
            f"# {title}\n\n"
            f"**Created by**: {self.name}\n"
            f"**Agent Role**: {self.role}\n"
            f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Agent ID**: {self.agent_id}\n\n"
            f"## Description\n{description}\n\n"
        )

    def create_task(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        task_type: str = "task",
    ) -> Dict[str, Any]:
        """Create a task structure."""
        task = {
            "id": self._generate_task_id(title),
            "title": title,
            "description": description,
            "priority": priority,
            "type": task_type,
            "status": "pending",
            "created_by": self.agent_id,
            "created_at": datetime.now().isoformat(),
            "skills_required": self.skills,
        }
        return task

    def _generate_task_id(self, title: str) -> str:
        """Generate task ID from title."""
        return (
            title.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "")
        )

    def get_created_files(self) -> List[Path]:
        """Get list of files created by this agent."""
        return self.created_files

    def log_action(self, action: str) -> None:
        """Log agent action."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.name}: {action}")
