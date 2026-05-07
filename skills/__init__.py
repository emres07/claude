"""
Skills system for agents.

Each skill represents a specialized capability that an agent can use
to perform their domain-specific work.
"""

from .task_clarification import TaskClarificationSkill
from .backend_skills import BackendSkill
from .frontend_skills import FrontendSkill
from .database_skills import DatabaseSkill

__all__ = [
    "TaskClarificationSkill",
    "BackendSkill",
    "FrontendSkill",
    "DatabaseSkill",
]
