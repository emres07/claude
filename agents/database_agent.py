"""Database Agent - Creates database subtasks and generates Oracle/PL-SQL code."""

from typing import Any, Dict, List
import json
from pathlib import Path

from .base_agent import BaseAgent
from skills.database_skills import DatabaseSkill


class DatabaseAgent(BaseAgent):
    """Agent responsible for database development subtasks and file organization."""

    def __init__(self):
        """Initialize Database Agent."""
        super().__init__(
            agent_id="database_agent",
            name="Database Agent",
            role="database_developer",
            output_folder="subtasks/database",
            skills=[
                "oracle",
                "plsql",
                "schema_design",
                "crud_operations",
                "task_clarification",
                "file_organization",
                "github_integration",
            ],
        )
        self.code_folder = Path("dbadmin")
        self.code_folder.mkdir(parents=True, exist_ok=True)

    def create_database_subtask(
        self,
        task_id: str,
        title: str,
        description: str,
        tables: List[str] = None,
        indexes: List[str] = None,
        performance_critical: bool = False,
    ) -> Dict[str, Any]:
        """Create a database-specific subtask."""
        subtask = self.create_task(
            title=title,
            description=description,
            task_type="database_subtask",
        )

        subtask["parent_task_id"] = task_id
        subtask["domain"] = "database"
        subtask["tables"] = tables or []
        subtask["indexes"] = indexes or []
        subtask["performance_critical"] = performance_critical
        subtask["acceptance_criteria"] = []

        return subtask

    def save_subtask(self, subtask: Dict[str, Any]) -> str:
        """Save database subtask to file."""
        content = self.generate_metadata(
            subtask["title"],
            subtask["description"],
        )

        content += f"## Domain\nDatabase\n\n"
        content += f"## Parent Task\n{subtask['parent_task_id']}\n\n"

        if subtask["tables"]:
            content += "## Tables\n"
            for table in subtask["tables"]:
                content += f"- {table}\n"
            content += "\n"

        if subtask["indexes"]:
            content += "## Indexes\n"
            for index in subtask["indexes"]:
                content += f"- {index}\n"
            content += "\n"

        if subtask["performance_critical"]:
            content += "## Performance Considerations\nThis is performance-critical work\n\n"

        content += "## Acceptance Criteria\n"
        if subtask["acceptance_criteria"]:
            for criterion in subtask["acceptance_criteria"]:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] Schema designed and validated\n"
            content += "- [ ] Migration scripts created\n"
            content += "- [ ] Indexes optimized\n"
            content += "- [ ] Backup strategy documented\n"
        content += "\n"

        content += f"## Status\n{subtask['status']}\n"

        filepath = self.save_task_file(
            filename=subtask["id"],
            content=content,
            task_id=None,
        )

        self.log_action(
            f"Created database subtask for {subtask['parent_task_id']}: {subtask['title']}"
        )
        return str(filepath)

    def create_subtasks_from_task(
        self,
        task_id: str,
        task_title: str,
    ) -> List[Dict[str, Any]]:
        """Create multiple database subtasks from a main task."""
        subtasks = [
            self.create_database_subtask(
                task_id=task_id,
                title=f"Database Schema - {task_title}",
                description="Design database schema and create migration",
                tables=["main_table", "related_table"],
            ),
            self.create_database_subtask(
                task_id=task_id,
                title=f"Query Optimization - {task_title}",
                description="Optimize queries and create indexes",
                indexes=["idx_primary", "idx_secondary"],
                performance_critical=True,
            ),
        ]

        return subtasks

    def clarify_task_description(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Clarify and enhance task description."""
        self.log_action(f"Clarifying task description for: {task['title']}")

        # Add clarification metadata
        task["clarified"] = True
        task["clarification_timestamp"] = (
            self.__class__.__module__
        )

        if not task.get("acceptance_criteria"):
            task["acceptance_criteria"] = [
                "Requirements clearly understood",
                "Scope defined",
                "Success criteria established",
            ]

        return task

    def organize_and_save_summary(
        self,
        all_tasks: Dict[str, List[str]],
        output_folder: str = ".",
    ) -> str:
        """Organize all tasks/subtasks and create summary file."""
        summary = "# Project Task Organization Summary\n\n"
        summary += "## Overview\n"
        summary += "This file contains an organized view of all tasks and subtasks created by the agent team.\n\n"

        summary += "## Tasks\n"
        if all_tasks.get("tasks"):
            for task in all_tasks["tasks"]:
                summary += f"- {task}\n"
        summary += "\n"

        summary += "## Backend Subtasks\n"
        if all_tasks.get("backend"):
            for subtask in all_tasks["backend"]:
                summary += f"- {subtask}\n"
        summary += "\n"

        summary += "## Frontend Subtasks\n"
        if all_tasks.get("frontend"):
            for subtask in all_tasks["frontend"]:
                summary += f"- {subtask}\n"
        summary += "\n"

        summary += "## Database Subtasks\n"
        if all_tasks.get("database"):
            for subtask in all_tasks["database"]:
                summary += f"- {subtask}\n"
        summary += "\n"

        filepath = self.save_task_file(
            filename="project_summary",
            content=summary,
            task_id=None,
        )

        self.log_action(f"Created project summary: {filepath}")
        return str(filepath)

    def prepare_github_commit(self, message: str = None) -> Dict[str, Any]:
        """Prepare data for GitHub commit."""
        if message is None:
            message = "Auto-generated tasks and subtasks from agent team"

        return {
            "commit_message": message,
            "files": self.get_created_files(),
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "agent_id": self.agent_id,
        }

    def generate_project_structure(self, project_name: str, schema_name: str = None) -> None:
        """Generate complete Oracle database project structure."""
        if schema_name is None:
            schema_name = project_name.lower().replace(' ', '_')

        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create schema creation script
        schema_sql_path = project_folder / "001_schema_creation.sql"
        schema_sql_path.write_text(
            DatabaseSkill.generate_oracle_schema(schema_name),
            encoding="utf-8"
        )
        self.created_files.append(schema_sql_path)
        self.log_action(f"Generated schema creation script for {schema_name}")

        # Create tables
        tables_dir = project_folder / "tables"
        tables_dir.mkdir(parents=True, exist_ok=True)

        tables = ["user", "transaction", "audit"]
        for table in tables:
            table_sql_path = tables_dir / f"02_{table}_table.sql"
            table_sql_path.write_text(
                DatabaseSkill.generate_table_template(table),
                encoding="utf-8"
            )
            self.created_files.append(table_sql_path)

        # Create CRUD procedures
        procedures_dir = project_folder / "procedures"
        procedures_dir.mkdir(parents=True, exist_ok=True)

        for table in tables:
            crud_path = procedures_dir / f"03_{table}_crud.sql"
            crud_path.write_text(
                DatabaseSkill.generate_crud_procedures(table),
                encoding="utf-8"
            )
            self.created_files.append(crud_path)

        # Create migration script
        migration_path = project_folder / "migrations" / "001_initial.sql"
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_text(
            DatabaseSkill.generate_migration_script("001"),
            encoding="utf-8"
        )
        self.created_files.append(migration_path)

        # Create packages
        packages_dir = project_folder / "packages"
        packages_dir.mkdir(parents=True, exist_ok=True)

        # Create setup script
        setup_script = project_folder / "setup.sh"
        setup_script.write_text(
            DatabaseSkill.generate_oracle_setup_script(),
            encoding="utf-8"
        )
        self.created_files.append(setup_script)

        # Create README
        readme_path = project_folder / "README.md"
        readme_content = f"""# {project_name} - Database Schema

## Schema Information

- **Schema Name**: {schema_name}
- **Database**: Oracle 21c/23c
- **Connection String**: jdbc:oracle:thin:@localhost:1521:xe

## Directory Structure

- `001_schema_creation.sql` - Initial schema and user setup
- `tables/` - Table definitions
- `procedures/` - CRUD stored procedures
- `packages/` - PL/SQL packages
- `migrations/` - Migration scripts
- `setup.sh` - Automated setup script

## CRUD Operations

All tables include:
- INSERT procedure
- SELECT procedure (single & all)
- UPDATE procedure
- DELETE procedure
- Audit triggers
- Indexes for performance

## Setup

```bash
# Run setup script
./setup.sh

# Connect to SQL*Plus
sqlplus /nolog

# In SQL*Plus:
@001_schema_creation.sql
@tables/02_user_table.sql
@tables/02_transaction_table.sql
@tables/02_audit_table.sql
@procedures/03_user_crud.sql
@procedures/03_transaction_crud.sql
@procedures/03_audit_crud.sql
```

## Tables Created

1. **user** - User master table
2. **transaction** - Transaction records
3. **audit** - Audit trail

Each table includes:
- Primary key
- Timestamps (created_at, updated_at)
- Audit triggers
- Indexes

## Best Practices

- Use parameters for security
- All procedures with error handling
- Automatic audit trail
- Transaction safety
- Proper indexing
"""
        readme_path.write_text(readme_content, encoding="utf-8")
        self.created_files.append(readme_path)

        self.log_action(f"Database project structure created: {project_name}")
