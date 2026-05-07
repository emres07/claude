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
                title=f"Database Setup & Schema Creation - {task_title}",
                description="Create schema, tablespace, user, and initial setup",
                tables=["schema_setup", "tablespace", "user_creation"],
            ),
            self.create_database_subtask(
                task_id=task_id,
                title=f"Create Core Tables - {task_title}",
                description="Create user, task, and audit tables with constraints",
                tables=["user", "task", "audit"],
            ),
            self.create_database_subtask(
                task_id=task_id,
                title=f"Create Indexes & Triggers - {task_title}",
                description="Create indexes for performance and triggers for audit",
                indexes=["idx_user_email", "idx_task_user", "idx_audit_time"],
                performance_critical=True,
            ),
            self.create_database_subtask(
                task_id=task_id,
                title=f"Create Stored Procedures - {task_title}",
                description="Create CRUD procedures and packages for all tables",
                tables=["user", "task", "audit"],
            ),
            self.create_database_subtask(
                task_id=task_id,
                title=f"Setup Backup & Documentation - {task_title}",
                description="Document schema, create backup strategy, and version control",
                indexes=["backup_strategy", "documentation"],
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

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None,
                                  schema_name: str = None, subtask_indices: List[int] = None) -> None:
        """Generate versioned Oracle database scripts based on subtasks."""
        if schema_name is None:
            schema_name = project_name.lower().replace(' ', '_')

        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create migrations folder with versioning
        migrations_dir = project_folder / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        # Only generate code for subtasks passed in
        if subtasks:
            for i, subtask in enumerate(subtasks):
                # Use provided indices or default to enumerate indices
                idx = subtask_indices[i] if subtask_indices and i < len(subtask_indices) else i + 1
                self._generate_subtask_migration(migrations_dir, subtask, idx, schema_name)
        else:
            # If no subtasks, generate all (backward compatibility)
            self._generate_all_migrations(migrations_dir, schema_name)

        # Generate migration guide and status file only after code generation
        self._create_migration_guide(migrations_dir, project_name, schema_name)

        # ============= MAIN README =============
        project_folder = migrations_dir.parent
        readme_path = project_folder / "README.md"
        readme_content = f"""# {project_name} - Database Component

## Overview

Oracle database schema and stored procedures for **{project_name}**.

- **Database Type**: Oracle 21c/23c
- **Schema Name**: {schema_name}
- **Versioning**: Semantic versioning (v001, v002, v003...)
- **Status**: NOT auto-executed - manual execution required

## 📂 Structure

```
.
├── migrations/                 # Versioned SQL migration scripts
│   ├── 001_schema_creation.sql     # v001: Schema & user setup
│   ├── 002_create_tables.sql       # v002: Table definitions
│   ├── 003_crud_procedures.sql     # v003: Stored procedures
│   ├── .migration_status           # Version tracking (JSON)
│   ├── .executed_migrations        # Execution history (JSON)
│   └── README.md                   # Migration guide
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
```bash
# Oracle Database 21c/23c
# SQL*Plus client
# DBA or schema creation privileges
```

### Execute Migrations

```bash
# Step 1: Create schema (as DBA)
sqlplus / AS SYSDBA
@migrations/001_schema_creation.sql

# Step 2: Create tables (as schema user)
sqlplus {schema_name.lower()}/welcome123@xe
@migrations/002_create_tables.sql

# Step 3: Create procedures (as schema user)
@migrations/003_crud_procedures.sql
```

### Verify Installation

```sql
-- Check tables
SELECT table_name FROM user_tables;

-- Check procedures
SELECT object_name FROM user_procedures;

-- Check packages
SELECT object_name FROM user_packages;
```

## 📋 Database Schema

### Tables

#### 1. `user` Table
```sql
- id (NUMBER) - Primary Key
- email (VARCHAR2) - User email
- password (VARCHAR2) - Hashed password
- created_at (TIMESTAMP) - Creation time
- updated_at (TIMESTAMP) - Last update time
```

#### 2. `transaction` Table
```sql
- id (NUMBER) - Primary Key
- user_id (NUMBER) - Foreign Key
- amount (NUMBER) - Transaction amount
- status (VARCHAR2) - Transaction status
- created_at (TIMESTAMP) - Creation time
- updated_at (TIMESTAMP) - Last update time
```

#### 3. `audit` Table
```sql
- audit_id (NUMBER) - Audit ID
- table_name (VARCHAR2) - Modified table
- operation (VARCHAR2) - INSERT/UPDATE/DELETE
- operation_time (TIMESTAMP) - When it happened
- user_name (VARCHAR2) - Who did it
```

## 🔄 CRUD Operations

All operations through PL/SQL packages:

```sql
-- INSERT
EXEC pkg_user_ops.insert_record('user@email.com', 'password', p_id);

-- SELECT
EXEC pkg_user_ops.get_record(1, p_cursor);

-- UPDATE
EXEC pkg_user_ops.update_record(1, 'newemail@email.com', 'newpass');

-- DELETE
EXEC pkg_user_ops.delete_record(1);
```

## 📊 Features

✅ **Versioned Migrations** - All changes tracked with versions
✅ **CRUD Procedures** - Stored procedures for all operations
✅ **Audit Trail** - Automatic tracking of all changes
✅ **Indexes** - Performance optimized with indexes
✅ **Constraints** - Data integrity with constraints
✅ **Triggers** - Automatic timestamp updates
✅ **Error Handling** - Robust error handling in procedures

## 🔒 Security Features

- Parameterized queries (no SQL injection)
- Stored procedures for controlled access
- User privileges properly configured
- Audit trail for compliance
- Encryption-ready schema

## 📈 Performance

- Indexed frequently queried columns
- Optimized table structure
- Efficient CRUD procedures
- Prepared for scaling

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 001 | 2026-05-07 | Initial schema creation |
| 002 | 2026-05-07 | Create all tables |
| 003 | 2026-05-07 | Create CRUD procedures |

## 📚 Documentation

- **migrations/README.md** - Complete migration guide
- **migrations/.migration_status** - Version tracking
- **migrations/.executed_migrations** - Execution history

## 🆘 Support

For issues:
1. Check **migrations/README.md** for troubleshooting
2. Verify all migrations executed in order
3. Check Oracle logs
4. Review audit trail for errors

## 🎯 Next Steps

1. ✅ Review migration scripts
2. 📥 Execute migrations in order
3. 🧪 Test CRUD operations
4. 🐙 Commit to GitHub
5. 🔄 Create new migrations as needed

---

**Important**: Scripts are versioned and never auto-executed. Manual execution ensures safety! 🔐
"""
        readme_path.write_text(readme_content, encoding="utf-8")
        self.created_files.append(readme_path)

        # Generate subtask documentation only (code is already in main folder)
        if subtasks:
            self._generate_subtask_documentation(project_folder, subtasks)

        self.log_action(f"Database project structure created (versioned, not executed): {project_name}")

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
- `migrations/` - SQL migration scripts (versioned)
- `.migration_status` - Version tracking (JSON)
- `README.md` - Migration documentation

### Tables Generated
{chr(10).join([f"- {table}" for table in subtask.get('tables', [])])}

### Indexes Generated
{chr(10).join([f"- {idx}" for idx in subtask.get('indexes', [])])}

### Acceptance Criteria
- [x] Code generated automatically
- [ ] Migrations tested in development
- [ ] Migrations executed in order
- [ ] Backup strategy implemented
- [ ] Code reviewed

### Next Steps
1. Review generated scripts in main project folder
2. Test migrations in development environment
3. Execute migrations in order (001 → 002 → 003)
4. Verify all tables and procedures created
5. Test CRUD operations
6. Commit to version control

### Files to Review
- All SQL files follow Oracle best practices
- Migration scripts are versioned and safe (not auto-executed)
- Stored procedures include error handling
- Tables include proper constraints and indexes
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            self.log_action(f"Generated documentation for subtask {idx}: {subtask['title']}")

    def _generate_subtask_migration(self, migrations_dir: Path, subtask: Dict[str, Any],
                                     subtask_idx: int, schema_name: str) -> None:
        """Generate database migration scripts based on subtask."""
        tables = ["user", "transaction", "audit"]

        if subtask_idx == 1:
            # Subtask 1: Database Setup & Schema Creation
            schema_sql_path = migrations_dir / "001_schema_creation.sql"
            schema_sql_path.write_text(
                DatabaseSkill.generate_oracle_schema(schema_name),
                encoding="utf-8"
            )
            self.created_files.append(schema_sql_path)
            self.log_action(f"Generated v001: Schema creation for {schema_name}")

        elif subtask_idx == 2:
            # Subtask 2: Create Core Tables
            tables_sql_path = migrations_dir / "002_create_tables.sql"
            tables_content = "-- ============================================================\n"
            tables_content += "-- VERSION 002: Create Tables\n"
            tables_content += "-- ============================================================\n\n"

            for table in tables:
                tables_content += DatabaseSkill.generate_table_template(table) + "\n"

            tables_sql_path.write_text(tables_content, encoding="utf-8")
            self.created_files.append(tables_sql_path)
            self.log_action(f"Generated v002: Create all tables")

        elif subtask_idx == 3:
            # Subtask 3: Create Indexes & Triggers
            # This could be extended with actual index and trigger generation
            pass

        elif subtask_idx == 4:
            # Subtask 4: Create Stored Procedures
            crud_sql_path = migrations_dir / "003_crud_procedures.sql"
            crud_content = "-- ============================================================\n"
            crud_content += "-- VERSION 003: Create CRUD Stored Procedures\n"
            crud_content += "-- ============================================================\n\n"

            for table in tables:
                crud_content += DatabaseSkill.generate_crud_procedures(table) + "\n\n"

            crud_sql_path.write_text(crud_content, encoding="utf-8")
            self.created_files.append(crud_sql_path)
            self.log_action(f"Generated v003: CRUD procedures for all tables")

        elif subtask_idx == 5:
            # Subtask 5: Setup Backup & Documentation
            pass

    def _generate_all_migrations(self, migrations_dir: Path, schema_name: str) -> None:
        """Generate all migration scripts (backward compatibility)."""
        tables = ["user", "transaction", "audit"]

        # VERSION 001: Schema Creation
        schema_sql_path = migrations_dir / "001_schema_creation.sql"
        schema_sql_path.write_text(
            DatabaseSkill.generate_oracle_schema(schema_name),
            encoding="utf-8"
        )
        self.created_files.append(schema_sql_path)
        self.log_action(f"Generated v001: Schema creation for {schema_name}")

        # VERSION 002: Create Tables
        tables_sql_path = migrations_dir / "002_create_tables.sql"
        tables_content = "-- ============================================================\n"
        tables_content += "-- VERSION 002: Create Tables\n"
        tables_content += "-- ============================================================\n\n"

        for table in tables:
            tables_content += DatabaseSkill.generate_table_template(table) + "\n"

        tables_sql_path.write_text(tables_content, encoding="utf-8")
        self.created_files.append(tables_sql_path)
        self.log_action(f"Generated v002: Create all tables")

        # VERSION 003: CRUD Procedures
        crud_sql_path = migrations_dir / "003_crud_procedures.sql"
        crud_content = "-- ============================================================\n"
        crud_content += "-- VERSION 003: Create CRUD Stored Procedures\n"
        crud_content += "-- ============================================================\n\n"

        for table in tables:
            crud_content += DatabaseSkill.generate_crud_procedures(table) + "\n\n"

        crud_sql_path.write_text(crud_content, encoding="utf-8")
        self.created_files.append(crud_sql_path)
        self.log_action(f"Generated v003: CRUD procedures for all tables")

    def _create_migration_guide(self, migrations_dir: Path, project_name: str, schema_name: str) -> None:
        """Create migration status and guide files."""
        # ============= VERSION TRACKING FILE =============
        migration_status_path = migrations_dir / ".migration_status"
        migration_status = """{
  "current_version": "003",
  "database": "oracle",
  "created_at": "2026-05-07",
  "migrations": [
    {
      "version": "001",
      "name": "schema_creation",
      "description": "Create schema, tablespace, and user",
      "status": "pending",
      "file": "001_schema_creation.sql",
      "executed": false
    },
    {
      "version": "002",
      "name": "create_tables",
      "description": "Create user, transaction, and audit tables",
      "status": "pending",
      "file": "002_create_tables.sql",
      "executed": false
    },
    {
      "version": "003",
      "name": "crud_procedures",
      "description": "Create CRUD stored procedures and packages",
      "status": "pending",
      "file": "003_crud_procedures.sql",
      "executed": false
    }
  ],
  "notes": "Scripts are versioned but NOT auto-executed. Manual execution required."
}
"""
        migration_status_path.write_text(migration_status, encoding="utf-8")
        self.created_files.append(migration_status_path)
