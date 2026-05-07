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

    def generate_project_structure(self, project_name: str, subtasks: List[Dict[str, Any]] = None, schema_name: str = None) -> None:
        """Generate versioned Oracle database scripts (no execution, version control only)."""
        if schema_name is None:
            schema_name = project_name.lower().replace(' ', '_')

        project_folder = self.code_folder / project_name.lower().replace(' ', '_')
        project_folder.mkdir(parents=True, exist_ok=True)

        # Create migrations folder with versioning
        migrations_dir = project_folder / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        # ============= VERSION 001: Schema Creation =============
        schema_sql_path = migrations_dir / "001_schema_creation.sql"
        schema_sql_path.write_text(
            DatabaseSkill.generate_oracle_schema(schema_name),
            encoding="utf-8"
        )
        self.created_files.append(schema_sql_path)
        self.log_action(f"Generated v001: Schema creation for {schema_name}")

        # ============= VERSION 002: Create Tables =============
        tables = ["user", "transaction", "audit"]

        # Create combined tables script for version 002
        tables_dir = migrations_dir
        tables_sql_path = tables_dir / "002_create_tables.sql"
        tables_content = "-- ============================================================\n"
        tables_content += "-- VERSION 002: Create Tables\n"
        tables_content += "-- ============================================================\n\n"

        for table in tables:
            tables_content += DatabaseSkill.generate_table_template(table) + "\n"

        tables_sql_path.write_text(tables_content, encoding="utf-8")
        self.created_files.append(tables_sql_path)
        self.log_action(f"Generated v002: Create all tables")

        # ============= VERSION 003: CRUD Procedures =============
        crud_sql_path = tables_dir / "003_crud_procedures.sql"
        crud_content = "-- ============================================================\n"
        crud_content += "-- VERSION 003: Create CRUD Stored Procedures\n"
        crud_content += "-- ============================================================\n\n"

        for table in tables:
            crud_content += DatabaseSkill.generate_crud_procedures(table) + "\n\n"

        crud_sql_path.write_text(crud_content, encoding="utf-8")
        self.created_files.append(crud_sql_path)
        self.log_action(f"Generated v003: CRUD procedures for all tables")

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

        # ============= MIGRATION GUIDE =============
        migration_guide_path = migrations_dir / "README.md"
        migration_guide = f"""# {project_name} - Database Migrations

## Overview

All database changes are versioned and organized in this `migrations/` folder.
**Scripts are NOT automatically executed** - manual execution is required for safety.

## Current Version: v003

### Migration History

| Version | Name | Description | Status | File |
|---------|------|-------------|--------|------|
| 001 | Schema Creation | Create schema, tablespace, user | Pending | `001_schema_creation.sql` |
| 002 | Create Tables | Create user, transaction, audit tables | Pending | `002_create_tables.sql` |
| 003 | CRUD Procedures | Create stored procedures & packages | Pending | `003_crud_procedures.sql` |

## How to Execute Migrations

### Prerequisites
- Oracle Database 21c or 23c installed
- SQL*Plus access
- Sufficient privileges (DBA or schema creation)

### Manual Execution Steps

#### Step 1: Execute v001 (Schema Creation)
```bash
sqlplus /nolog
SQL> CONNECT / AS SYSDBA
SQL> @migrations/001_schema_creation.sql
```

This creates:
- Tablespace `{schema_name.lower()}_ts`
- User `{schema_name.lower()}` with password `welcome123`
- Required privileges
- Sequence for auto-increment

#### Step 2: Execute v002 (Create Tables)
```bash
sqlplus /nolog
SQL> CONNECT {schema_name.lower()}/welcome123@xe
SQL> @migrations/002_create_tables.sql
```

This creates:
- `user` table with columns and indexes
- `transaction` table for transaction records
- `audit` table for audit trail
- Audit triggers for automatic logging

#### Step 3: Execute v003 (CRUD Procedures)
```bash
sqlplus /nolog
SQL> CONNECT {schema_name.lower()}/welcome123@xe
SQL> @migrations/003_crud_procedures.sql
```

This creates:
- Stored procedures: `sp_user_insert`, `sp_user_get`, `sp_user_update`, `sp_user_delete`
- Stored procedures for `transaction` and `audit` tables
- PL/SQL packages: `pkg_user_ops`, `pkg_transaction_ops`, `pkg_audit_ops`

## Supported Operations

### User Management
```sql
-- Insert user
EXEC pkg_user_ops.insert_record('user@email.com', 'password', p_id);

-- Get user by ID
EXEC pkg_user_ops.get_record(1, p_cursor);

-- Update user
EXEC pkg_user_ops.update_record(1, 'new@email.com', 'new password');

-- Delete user
EXEC pkg_user_ops.delete_record(1);
```

### Transaction Management
```sql
-- Similar operations for transactions
EXEC pkg_transaction_ops.insert_record(...);
EXEC pkg_transaction_ops.get_record(...);
EXEC pkg_transaction_ops.update_record(...);
EXEC pkg_transaction_ops.delete_record(...);
```

### Audit Trail
```sql
-- Query audit table
SELECT * FROM audit ORDER BY operation_time DESC;
```

## Version Control Best Practices

1. **Never modify existing migrations** - Create new versions instead
2. **Always increment version numbers** - 001, 002, 003, etc.
3. **Document changes** - Add description to each migration
4. **Test before execution** - Run in test environment first
5. **Keep .migration_status updated** - Track executed migrations
6. **Commit to Git** - Version control all SQL files

## Adding New Migrations

To add a new migration:

1. Create file: `migrations/00X_description.sql`
2. Increment version in `.migration_status`
3. Add migration record with status "pending"
4. Test the script
5. Execute manually when ready
6. Update `.migration_status` to "executed"
7. Commit changes to Git

## Rollback Procedures

### Rollback v003 (Drop Procedures)
```sql
DROP PACKAGE pkg_user_ops;
DROP PACKAGE pkg_transaction_ops;
DROP PACKAGE pkg_audit_ops;
DROP PROCEDURE sp_user_insert;
DROP PROCEDURE sp_user_get;
-- ... drop all procedures
```

### Rollback v002 (Drop Tables)
```sql
DROP TABLE audit;
DROP TABLE transaction;
DROP TABLE user;
```

### Rollback v001 (Drop Schema)
```sql
DROP USER {schema_name.lower()} CASCADE;
DROP TABLESPACE {schema_name.lower()}_ts INCLUDING CONTENTS AND DATAFILES;
```

## Troubleshooting

### Error: Table already exists
**Cause**: Migration already executed
**Solution**: Check `.migration_status` - mark as executed and skip

### Error: Insufficient privileges
**Cause**: Connected user doesn't have DBA rights
**Solution**: Connect as SYSDBA or schema owner

### Error: Tablespace not found
**Cause**: v001 not executed yet
**Solution**: Execute migrations in order (001 → 002 → 003)

### Error: Procedure not found
**Cause**: v003 not executed
**Solution**: Execute v003 migration script

## File Structure

```
migrations/
├── 001_schema_creation.sql    # Version 001: Schema setup
├── 002_create_tables.sql      # Version 002: Table definitions
├── 003_crud_procedures.sql    # Version 003: Stored procedures
├── .migration_status          # Version tracking (JSON)
├── .executed_migrations       # (Created after execution)
└── README.md                  # This file
```

## Integration with CI/CD

To automate migrations in CI/CD:

```bash
#!/bin/bash
# run_migrations.sh

SQLPLUS_PATH="/opt/oracle/client/bin/sqlplus"
MIGRATIONS_DIR="migrations"
MIGRATION_STATUS="$MIGRATIONS_DIR/.migration_status"

# Check current version
CURRENT_VERSION=$(grep '"current_version"' "$MIGRATION_STATUS" | grep -oE '[0-9]+')

# Execute pending migrations
for v in 001 002 003; do
  if [ $v -gt $CURRENT_VERSION ]; then
    echo "Executing migration v$v..."
    $SQLPLUS_PATH user/password@xe @$MIGRATIONS_DIR/${v}_*.sql
    if [ $? -eq 0 ]; then
      echo "v$v executed successfully"
    else
      echo "v$v execution failed"
      exit 1
    fi
  fi
done
```

## Next Steps

1. ✅ Review migration scripts in this folder
2. 📝 Execute migrations in order (001 → 002 → 003)
3. 🧪 Test CRUD operations
4. 📊 Monitor audit trail
5. 🔄 Create new migrations as needed
6. 🐙 Commit to version control

---

**Important**: Scripts are versioned for safety and auditability. Always test in non-production first! 🔒
"""
        migration_guide_path.write_text(migration_guide, encoding="utf-8")
        self.created_files.append(migration_guide_path)

        # ============= EXECUTION LOG (EMPTY) =============
        execution_log_path = migrations_dir / ".executed_migrations"
        execution_log = """{
  "last_execution": null,
  "executed_migrations": [],
  "notes": "This file is updated when migrations are manually executed"
}
"""
        execution_log_path.write_text(execution_log, encoding="utf-8")
        self.created_files.append(execution_log_path)

        # ============= MAIN README =============
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

        # Generate subtask-specific implementations
        if subtasks:
            self._generate_subtask_implementations(project_folder, subtasks, schema_name)

        self.log_action(f"Database project structure created (versioned, not executed): {project_name}")

    def _generate_subtask_implementations(
        self, project_folder: Path, subtasks: List[Dict[str, Any]], schema_name: str
    ) -> None:
        """Generate specific code for each subtask."""
        subtasks_folder = project_folder / "subtasks"
        subtasks_folder.mkdir(parents=True, exist_ok=True)

        for idx, subtask in enumerate(subtasks, 1):
            subtask_name = subtask["title"].lower().replace(" - ", "_").replace(" ", "_")
            subtask_folder = subtasks_folder / f"{idx:02d}_{subtask_name}"
            subtask_folder.mkdir(parents=True, exist_ok=True)

            # Create README for subtask
            readme_content = f"""# {subtask['title']}

## Description
{subtask['description']}

## Tables
{chr(10).join([f"- {table}" for table in subtask.get('tables', [])])}

## Indexes
{chr(10).join([f"- {idx}" for idx in subtask.get('indexes', [])])}

## Acceptance Criteria
- [ ] Schema designed and validated
- [ ] Migration scripts tested
- [ ] Permissions configured
- [ ] Documentation complete

## Files Generated
Generated SQL scripts for this subtask.
"""
            readme_path = subtask_folder / "README.md"
            readme_path.write_text(readme_content, encoding="utf-8")
            self.created_files.append(readme_path)

            # Subtask 1: Setup
            if idx == 1:
                self._generate_db_subtask_1_setup(subtask_folder, schema_name)
            # Subtask 2: Create Tables
            elif idx == 2:
                self._generate_db_subtask_2_tables(subtask_folder, schema_name)
            # Subtask 3: Indexes & Triggers
            elif idx == 3:
                self._generate_db_subtask_3_indexes_triggers(subtask_folder, schema_name)
            # Subtask 4: Procedures
            elif idx == 4:
                self._generate_db_subtask_4_procedures(subtask_folder, schema_name)
            # Subtask 5: Backup
            elif idx == 5:
                self._generate_db_subtask_5_backup(subtask_folder, schema_name)

    def _generate_db_subtask_1_setup(self, subtask_folder: Path, schema_name: str) -> None:
        """Generate setup script."""
        setup_path = subtask_folder / "001_setup.sql"
        setup_path.write_text(
            DatabaseSkill.generate_oracle_schema(schema_name),
            encoding="utf-8"
        )
        self.created_files.append(setup_path)
        self.log_action("Generated DB subtask 1: Setup")

    def _generate_db_subtask_2_tables(self, subtask_folder: Path, schema_name: str) -> None:
        """Generate table creation scripts."""
        tables_path = subtask_folder / "002_tables.sql"
        content = "-- ============================================================\n"
        content += "-- TABLE CREATION SCRIPTS\n"
        content += "-- ============================================================\n\n"

        for table in ["user", "task", "audit"]:
            content += DatabaseSkill.generate_table_template(table) + "\n\n"

        tables_path.write_text(content, encoding="utf-8")
        self.created_files.append(tables_path)
        self.log_action("Generated DB subtask 2: Tables")

    def _generate_db_subtask_3_indexes_triggers(self, subtask_folder: Path, schema_name: str) -> None:
        """Generate indexes and triggers."""
        indexes_path = subtask_folder / "003_indexes_triggers.sql"
        indexes_path.write_text(
            "-- ============================================================\n"
            "-- INDEXES AND TRIGGERS\n"
            "-- ============================================================\n\n"
            "-- Indexes for performance\n"
            "CREATE INDEX idx_user_email ON user(email);\n"
            "CREATE INDEX idx_task_user ON task(user_id);\n"
            "CREATE INDEX idx_audit_time ON audit(operation_time);\n",
            encoding="utf-8"
        )
        self.created_files.append(indexes_path)
        self.log_action("Generated DB subtask 3: Indexes & Triggers")

    def _generate_db_subtask_4_procedures(self, subtask_folder: Path, schema_name: str) -> None:
        """Generate stored procedures."""
        procedures_path = subtask_folder / "004_procedures.sql"
        content = "-- ============================================================\n"
        content += "-- CRUD STORED PROCEDURES\n"
        content += "-- ============================================================\n\n"

        for table in ["user", "task", "audit"]:
            content += DatabaseSkill.generate_crud_procedures(table) + "\n\n"

        procedures_path.write_text(content, encoding="utf-8")
        self.created_files.append(procedures_path)
        self.log_action("Generated DB subtask 4: Procedures")

    def _generate_db_subtask_5_backup(self, subtask_folder: Path, schema_name: str) -> None:
        """Generate backup documentation."""
        backup_path = subtask_folder / "BACKUP_STRATEGY.md"
        backup_path.write_text(
            f"""# Backup Strategy for {schema_name}

## Backup Plan

### Daily Backups
```bash
expdp {schema_name}/welcome123@xe directory=backup_dir dumpfile={schema_name}_daily.dmp logfile={schema_name}_daily.log
```

### Weekly Full Backups
```bash
expdp {schema_name}/welcome123@xe full=Y directory=backup_dir dumpfile={schema_name}_full_weekly.dmp
```

### Archive Logs
Enable archivelog mode for point-in-time recovery.

## Restore Procedure

```sql
-- Restore from backup
impdp {schema_name}/welcome123@xe directory=backup_dir dumpfile={schema_name}_daily.dmp logfile=restore.log
```

## Verification
- Test restore procedure monthly
- Document recovery time objectives (RTO)
- Document recovery point objectives (RPO)
""",
            encoding="utf-8"
        )
        self.created_files.append(backup_path)
        self.log_action("Generated DB subtask 5: Backup Strategy")
