# Database Versioning & Migration System

## 📋 Overview

The database agent generates **versioned SQL migration scripts** that are:

- ✅ **Version-controlled** - All changes tracked in `migrations/` folder
- ✅ **NOT auto-executed** - Manual execution for safety and auditability
- ✅ **Semantic versioned** - v001, v002, v003... with clear naming
- ✅ **Safe rollback** - Each version can be rolled back independently
- ✅ **CI/CD ready** - Integration scripts provided for automation

## 🗂️ Folder Structure

```
dbadmin/[project_name]/
├── migrations/                    # All versioned migration scripts
│   ├── 001_schema_creation.sql    # VERSION 001: Create schema
│   ├── 002_create_tables.sql      # VERSION 002: Create tables
│   ├── 003_crud_procedures.sql    # VERSION 003: Create procedures
│   ├── .migration_status          # Version tracking (JSON)
│   ├── .executed_migrations       # Execution history (JSON)
│   └── README.md                  # Detailed migration guide
├── README.md                      # Project overview
└── (no setup.sh - manual execution only)
```

## 🔄 Versioning System

### Version Naming Convention

```
NNN_description.sql

NNN     = 3-digit version number (001, 002, 003, 004, etc.)
_       = Separator
description = What this migration does (lowercase, underscores)

Examples:
- 001_schema_creation.sql
- 002_create_tables.sql
- 003_crud_procedures.sql
- 004_add_indexes.sql
- 005_create_packages.sql
```

### Migration Status Tracking

Each project contains `.migration_status` (JSON):

```json
{
  "current_version": "003",
  "database": "oracle",
  "created_at": "2026-05-07",
  "migrations": [
    {
      "version": "001",
      "name": "schema_creation",
      "description": "Create schema, tablespace, and user",
      "status": "pending",      // pending, executed, failed
      "file": "001_schema_creation.sql",
      "executed": false,        // true after successful execution
      "executed_at": null,      // timestamp when executed
      "executed_by": null       // who executed it
    },
    {
      "version": "002",
      "name": "create_tables",
      "description": "Create user, transaction, and audit tables",
      "status": "pending",
      "file": "002_create_tables.sql",
      "executed": false
    }
    // ... more versions
  ]
}
```

## 📥 Manual Execution

### Prerequisites

```bash
# Check what you need
✓ Oracle Database 21c or 23c installed
✓ SQL*Plus client available
✓ DBA or schema creation privileges
✓ Network connectivity to Oracle database
```

### Execution Steps

#### Step 1: Review Migrations

```bash
cd dbadmin/[project_name]
ls -la migrations/

# Output:
# 001_schema_creation.sql
# 002_create_tables.sql
# 003_crud_procedures.sql
# .migration_status
# .executed_migrations
# README.md
```

#### Step 2: Execute v001 (Schema Creation)

```bash
sqlplus /nolog

# In SQL*Plus:
CONNECT / AS SYSDBA;
@migrations/001_schema_creation.sql

# Output:
# Tablespace MYAPP_TS created.
# User MYAPP created.
# Privileges granted.
```

**What it creates:**
- Tablespace `myapp_ts`
- User `myapp` with password `welcome123`
- Required system privileges
- Sequence `myapp_seq` for auto-increment

#### Step 3: Execute v002 (Create Tables)

```bash
sqlplus /nolog

# In SQL*Plus:
CONNECT myapp/welcome123@xe;
@migrations/002_create_tables.sql

# Output:
# Table USER created.
# Index IDX_USER_CREATED_AT created.
# Trigger USER_AUDIT_TRG created.
# Table TRANSACTION created.
# ...
```

**What it creates:**
- `user` table with indexes and triggers
- `transaction` table with audit capability
- `audit` table for change tracking
- All indexes for performance
- All triggers for automatic updates

#### Step 4: Execute v003 (CRUD Procedures)

```bash
sqlplus /nolog

# In SQL*Plus:
CONNECT myapp/welcome123@xe;
@migrations/003_crud_procedures.sql

# Output:
# Procedure SP_USER_INSERT created.
# Procedure SP_USER_GET created.
# ...
# Package PKG_USER_OPS created.
# Package Body PKG_USER_OPS created.
```

**What it creates:**
- CRUD stored procedures for each table
- PL/SQL packages wrapping procedures
- Error handling in all procedures
- Transaction safety mechanisms

### Step 5: Update Migration Status

After successful execution, manually update `.migration_status`:

```json
{
  "current_version": "003",
  "migrations": [
    {
      "version": "001",
      "status": "executed",
      "executed": true,
      "executed_at": "2026-05-07T10:30:00Z",
      "executed_by": "dba_user"
    },
    {
      "version": "002",
      "status": "executed",
      "executed": true,
      "executed_at": "2026-05-07T10:35:00Z",
      "executed_by": "dba_user"
    },
    {
      "version": "003",
      "status": "executed",
      "executed": true,
      "executed_at": "2026-05-07T10:40:00Z",
      "executed_by": "dba_user"
    }
  ]
}
```

## 🧪 Testing Migrations

### Verify Installation

```sql
-- Check tables created
SELECT table_name FROM user_tables;
-- Expected: USER, TRANSACTION, AUDIT

-- Check procedures created
SELECT object_name FROM user_procedures;
-- Expected: SP_USER_INSERT, SP_USER_GET, etc.

-- Check packages created
SELECT object_name FROM user_packages;
-- Expected: PKG_USER_OPS, PKG_TRANSACTION_OPS, etc.

-- Check indexes
SELECT index_name FROM user_indexes;
-- Expected: IDX_USER_CREATED_AT, etc.
```

### Test CRUD Operations

```sql
-- INSERT
DECLARE
  v_id NUMBER;
BEGIN
  pkg_user_ops.insert_record('john@example.com', 'securepass', v_id);
  DBMS_OUTPUT.PUT_LINE('User inserted with ID: ' || v_id);
END;
/

-- SELECT
DECLARE
  v_cursor SYS_REFCURSOR;
BEGIN
  pkg_user_ops.get_record(1, v_cursor);
  -- Process cursor results
END;
/

-- UPDATE
BEGIN
  pkg_user_ops.update_record(1, 'newemail@example.com', 'newpass');
  DBMS_OUTPUT.PUT_LINE('User updated successfully');
END;
/

-- DELETE
BEGIN
  pkg_user_ops.delete_record(1);
  DBMS_OUTPUT.PUT_LINE('User deleted successfully');
END;
/
```

### Check Audit Trail

```sql
-- View all audit records
SELECT * FROM audit ORDER BY operation_time DESC;

-- View inserts
SELECT * FROM audit WHERE operation = 'INSERT';

-- View updates
SELECT * FROM audit WHERE operation = 'UPDATE';

-- View deletes
SELECT * FROM audit WHERE operation = 'DELETE';
```

## 🔄 Rollback Procedures

### Rollback v003 (Drop Procedures)

```sql
-- Connect as schema owner
CONNECT myapp/welcome123@xe;

-- Drop packages (packages contain procedures)
DROP PACKAGE pkg_user_ops;
DROP PACKAGE pkg_transaction_ops;
DROP PACKAGE pkg_audit_ops;

-- Commit
COMMIT;

-- Update .migration_status to v002
```

### Rollback v002 (Drop Tables)

```sql
-- Connect as schema owner
CONNECT myapp/welcome123@xe;

-- Drop tables (order matters - foreign keys first)
DROP TABLE audit;
DROP TABLE transaction;
DROP TABLE user;

-- Commit
COMMIT;

-- Update .migration_status to v001
```

### Rollback v001 (Drop Schema)

```bash
# Connect as DBA
sqlplus / AS SYSDBA;

# In SQL*Plus:
DROP USER myapp CASCADE;
DROP TABLESPACE myapp_ts INCLUDING CONTENTS AND DATAFILES;
COMMIT;
```

## ➕ Adding New Migrations

### Step 1: Create New Migration File

```bash
cd migrations/
cat > 004_add_new_feature.sql << 'EOF'
-- ============================================================
-- VERSION 004: Add New Feature
-- Description: Add product catalog
-- ============================================================

CREATE TABLE product (
  id NUMBER PRIMARY KEY,
  name VARCHAR2(255) NOT NULL,
  price NUMBER(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_product_name ON product(name);

CREATE OR REPLACE PROCEDURE sp_product_insert (
  p_name IN VARCHAR2,
  p_price IN NUMBER,
  p_id OUT NUMBER
)
IS
BEGIN
  INSERT INTO product (id, name, price, created_at, updated_at)
  VALUES (myapp_seq.NEXTVAL, p_name, p_price, SYSTIMESTAMP, SYSTIMESTAMP)
  RETURNING id INTO p_id;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END sp_product_insert;
/

-- ============================================================
EOF
```

### Step 2: Update .migration_status

```json
{
  "current_version": "004",
  "migrations": [
    // ... previous migrations ...
    {
      "version": "004",
      "name": "add_new_feature",
      "description": "Add product catalog",
      "status": "pending",
      "file": "004_add_new_feature.sql",
      "executed": false
    }
  ]
}
```

### Step 3: Test the Migration

```bash
cd /path/to/database
sqlplus /nolog

# In SQL*Plus:
CONNECT myapp/welcome123@xe;
@migrations/004_add_new_feature.sql

# Verify
SELECT table_name FROM user_tables WHERE table_name = 'PRODUCT';
```

### Step 4: Update Status & Commit

```bash
# Update .migration_status - mark as executed
# Commit to Git
git add migrations/
git commit -m "Add migration v004: Product catalog feature"
git push origin main
```

## 🤖 CI/CD Integration

### Automated Migration Script

```bash
#!/bin/bash
# run_migrations.sh

set -e

SQLPLUS_PATH="/opt/oracle/client/bin/sqlplus"
MIGRATIONS_DIR="migrations"
MIGRATION_STATUS="$MIGRATIONS_DIR/.migration_status"
DB_USER="${DB_USER:-myapp}"
DB_PASS="${DB_PASS:-welcome123}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-1521}"
DB_SID="${DB_SID:-xe}"

echo "🔄 Starting database migrations..."

# Check which migrations are pending
CURRENT_VERSION=$(grep '"current_version"' "$MIGRATION_STATUS" | grep -oE '[0-9]+')
echo "Current version: v$CURRENT_VERSION"

# Execute each pending migration
for v in 001 002 003 004 005; do
  version_padded=$(printf "%03d" $v)
  
  if [ $v -gt $CURRENT_VERSION ]; then
    migration_file=$(find $MIGRATIONS_DIR -name "${version_padded}_*.sql" -type f)
    
    if [ -f "$migration_file" ]; then
      echo "📥 Executing $migration_file..."
      
      # Execute migration
      $SQLPLUS_PATH -s "$DB_USER/$DB_PASS@(DESCRIPTION=(ADDRESS=(HOST=$DB_HOST)(PORT=$DB_PORT)(PROTOCOL=tcp))(CONNECT_DATA=(SID=$DB_SID)))" << EOF
@$migration_file
EXIT;
EOF
      
      if [ $? -eq 0 ]; then
        echo "✅ v$version_padded executed successfully"
        # Update .migration_status
        sed -i "s/\"current_version\": \"[0-9]*\"/\"current_version\": \"$version_padded\"/" "$MIGRATION_STATUS"
      else
        echo "❌ v$version_padded execution failed"
        exit 1
      fi
    fi
  fi
done

echo "✅ All migrations completed"
```

### GitHub Actions Example

```yaml
name: Database Migrations

on:
  push:
    paths:
      - 'dbadmin/*/migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    
    services:
      oracle:
        image: oracle-database:21c
        env:
          ORACLE_PASSWORD: admin123
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Migrations
        run: |
          cd dbadmin/myapp
          chmod +x ../../run_migrations.sh
          DB_USER=myapp DB_PASS=welcome123 ../../run_migrations.sh
      
      - name: Verify Installation
        run: |
          sqlplus myapp/welcome123@localhost:1521/xe << EOF
          SELECT COUNT(*) FROM user_tables;
          SELECT COUNT(*) FROM user_procedures;
          EXIT;
          EOF
      
      - name: Commit Status
        run: |
          git config user.email "ci@example.com"
          git config user.name "CI Bot"
          git add dbadmin/*/migrations/.migration_status
          git commit -m "Update migration status [skip ci]"
          git push
```

## 📊 Migration History Example

```
Project: TO DO LIST APP
Created: 2026-05-07

Timeline:
├── 2026-05-07 10:30 - v001 (Schema Creation) ✅ EXECUTED
│   └─ User: dba_admin
│   └─ Tables: 1 (audit)
│   └─ Objects: 1 schema, 1 user, 1 sequence
│
├── 2026-05-07 10:35 - v002 (Create Tables) ✅ EXECUTED
│   └─ User: dba_admin
│   └─ Tables: 3 (user, transaction, audit)
│   └─ Objects: 3 triggers, 3 indexes
│
└── 2026-05-07 10:40 - v003 (CRUD Procedures) ✅ EXECUTED
    └─ User: dba_admin
    └─ Procedures: 9 (3 per table)
    └─ Packages: 3 (pkg_user_ops, pkg_transaction_ops, pkg_audit_ops)
```

## ✅ Best Practices

### DO
- ✅ Always review scripts before execution
- ✅ Test in development first
- ✅ Execute migrations in order (v001 → v002 → v003)
- ✅ Keep .migration_status updated
- ✅ Commit migration files to Git
- ✅ Write clear migration descriptions
- ✅ Include rollback instructions

### DON'T
- ❌ Skip versions
- ❌ Modify existing migration files
- ❌ Execute multiple versions simultaneously
- ❌ Delete migration files
- ❌ Forget to update .migration_status
- ❌ Commit without testing
- ❌ Execute without backup

## 📚 Documentation in Each Project

Each generated database project includes:

```
migrations/README.md              # Complete migration guide
migrations/.migration_status      # Version tracking
migrations/.executed_migrations   # Execution history
README.md                         # Project overview
```

## 🎯 Summary

The database versioning system ensures:

- **Safety**: Manual execution prevents accidental changes
- **Auditability**: Each change is tracked and versioned
- **Reversibility**: Each version can be rolled back
- **Version Control**: All scripts committed to Git
- **Documentation**: Clear instructions for each migration
- **CI/CD Ready**: Easy automation when needed
- **Team Coordination**: Clear status tracking for teams

---

**All database changes are versioned, documented, and safe! 🔐**
