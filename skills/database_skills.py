"""Database Skills - Oracle, PL/SQL, Schema Design, CRUD Operations."""


class DatabaseSkill:
    """Skills for database development with Oracle, PL/SQL, schema design."""

    name = "database"
    description = "Database with Oracle, PL/SQL, Schema Design & CRUD Operations"

    DATABASES = {
        "oracle": "Oracle Database 21c/23c",
        "plsql": "PL/SQL for stored procedures",
    }

    TOOLS = ["SQL Developer", "Liquibase", "Flyway", "Oracle SQL*Plus"]

    @staticmethod
    def generate_oracle_schema(schema_name: str) -> str:
        """Generate Oracle schema creation script."""
        return f"""-- ============================================================
-- Schema Creation Script for {schema_name}
-- ============================================================

-- Create Tablespace
CREATE TABLESPACE {schema_name.lower()}_ts
  DATAFILE '/opt/oracle/oradata/{schema_name.lower()}_01.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Create Schema/User
CREATE USER {schema_name.lower()} IDENTIFIED BY welcome123
  DEFAULT TABLESPACE {schema_name.lower()}_ts
  QUOTA UNLIMITED ON {schema_name.lower()}_ts;

-- Grant Privileges
GRANT CREATE SESSION TO {schema_name.lower()};
GRANT CREATE TABLE TO {schema_name.lower()};
GRANT CREATE SEQUENCE TO {schema_name.lower()};
GRANT CREATE PROCEDURE TO {schema_name.lower()};
GRANT CREATE TRIGGER TO {schema_name.lower()};
GRANT UNLIMITED TABLESPACE TO {schema_name.lower()};

-- ============================================================
-- Sequences
-- ============================================================

CREATE SEQUENCE {schema_name.lower()}_seq
  START WITH 1
  INCREMENT BY 1
  NOCYCLE
  NOCACHE;

-- ============================================================
-- Audit Tables
-- ============================================================

CREATE TABLE {schema_name.lower()}_audit (
  audit_id NUMBER PRIMARY KEY,
  table_name VARCHAR2(30),
  operation VARCHAR2(10),
  operation_time TIMESTAMP DEFAULT SYSTIMESTAMP,
  user_name VARCHAR2(30)
);

-- ============================================================
-- End of Schema Creation Script
-- ============================================================
"""

    @staticmethod
    def generate_table_template(table_name: str, columns: list = None) -> str:
        """Generate Oracle table creation script."""
        if columns is None:
            columns = [
                {"name": "name", "type": "VARCHAR2(100)", "null": "NOT NULL"},
                {"name": "description", "type": "VARCHAR2(500)", "null": "NULL"},
                {"name": "status", "type": "VARCHAR2(20)", "null": "NOT NULL", "default": "'ACTIVE'"},
            ]

        pascal_case = ''.join(word.title() for word in table_name.split('_'))
        cols_sql = """  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
"""

        for col in columns:
            col_def = f"  {col['name']} {col['type']} {col.get('null', 'NULL')}"
            if 'default' in col:
                col_def += f" DEFAULT {col['default']}"
            cols_sql += col_def + ",\n"

        cols_sql = cols_sql.rstrip(",\n")

        return f"""-- ============================================================
-- Table: {table_name.upper()}
-- ============================================================

CREATE TABLE {table_name} (
{cols_sql}
);

-- Create Primary Key
ALTER TABLE {table_name} ADD CONSTRAINT pk_{table_name} PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at);
CREATE INDEX idx_{table_name}_updated_at ON {table_name}(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER {table_name}_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON {table_name}
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO {table_name}_audit (audit_id, table_name, operation, user_name)
    VALUES ({table_name}_seq.NEXTVAL, '{table_name}', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO {table_name}_audit (audit_id, table_name, operation, user_name)
    VALUES ({table_name}_seq.NEXTVAL, '{table_name}', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO {table_name}_audit (audit_id, table_name, operation, user_name)
    VALUES ({table_name}_seq.NEXTVAL, '{table_name}', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE {table_name} IS '{pascal_case} master table';
COMMENT ON COLUMN {table_name}.id IS 'Primary Key';
COMMENT ON COLUMN {table_name}.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN {table_name}.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================
"""

    @staticmethod
    def generate_crud_procedures(table_name: str) -> str:
        """Generate PL/SQL CRUD stored procedures."""
        pascal_case = ''.join(word.title() for word in table_name.split('_'))

        return f"""-- ============================================================
-- CRUD Stored Procedures for {table_name.upper()}
-- ============================================================

-- CREATE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_{table_name}_insert (
  p_name IN VARCHAR2,
  p_description IN VARCHAR2,
  p_status IN VARCHAR2 DEFAULT 'ACTIVE',
  p_id OUT NUMBER
)
IS
BEGIN
  INSERT INTO {table_name} (id, name, description, status, created_at, updated_at)
  VALUES ({table_name}_seq.NEXTVAL, p_name, p_description, p_status, SYSTIMESTAMP, SYSTIMESTAMP)
  RETURNING id INTO p_id;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('Record inserted successfully with ID: ' || p_id);
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error inserting record: ' || SQLERRM);
    RAISE;
END sp_{table_name}_insert;
/

-- READ PROCEDURE (Single Record)
CREATE OR REPLACE PROCEDURE sp_{table_name}_get (
  p_id IN NUMBER,
  p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
  OPEN p_cursor FOR
    SELECT id, name, description, status, created_at, updated_at
    FROM {table_name}
    WHERE id = p_id;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Record not found with ID: ' || p_id);
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error reading record: ' || SQLERRM);
    RAISE;
END sp_{table_name}_get;
/

-- READ PROCEDURE (All Records)
CREATE OR REPLACE PROCEDURE sp_{table_name}_get_all (
  p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
  OPEN p_cursor FOR
    SELECT id, name, description, status, created_at, updated_at
    FROM {table_name}
    ORDER BY created_at DESC;
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error retrieving records: ' || SQLERRM);
    RAISE;
END sp_{table_name}_get_all;
/

-- UPDATE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_{table_name}_update (
  p_id IN NUMBER,
  p_name IN VARCHAR2 DEFAULT NULL,
  p_description IN VARCHAR2 DEFAULT NULL,
  p_status IN VARCHAR2 DEFAULT NULL
)
IS
  v_rows_updated NUMBER;
BEGIN
  UPDATE {table_name}
  SET
    name = COALESCE(p_name, name),
    description = COALESCE(p_description, description),
    status = COALESCE(p_status, status),
    updated_at = SYSTIMESTAMP
  WHERE id = p_id;

  v_rows_updated := SQL%ROWCOUNT;

  IF v_rows_updated > 0 THEN
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Record updated successfully');
  ELSE
    DBMS_OUTPUT.PUT_LINE('No records found to update with ID: ' || p_id);
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error updating record: ' || SQLERRM);
    RAISE;
END sp_{table_name}_update;
/

-- DELETE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_{table_name}_delete (
  p_id IN NUMBER
)
IS
  v_rows_deleted NUMBER;
BEGIN
  DELETE FROM {table_name}
  WHERE id = p_id;

  v_rows_deleted := SQL%ROWCOUNT;

  IF v_rows_deleted > 0 THEN
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Record deleted successfully');
  ELSE
    DBMS_OUTPUT.PUT_LINE('No records found to delete with ID: ' || p_id);
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error deleting record: ' || SQLERRM);
    RAISE;
END sp_{table_name}_delete;
/

-- ============================================================
-- Package for {table_name.upper()} Operations
-- ============================================================

CREATE OR REPLACE PACKAGE pkg_{table_name}_ops IS
  PROCEDURE insert_record(
    p_name IN VARCHAR2,
    p_description IN VARCHAR2,
    p_id OUT NUMBER
  );

  PROCEDURE get_record(
    p_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
  );

  PROCEDURE get_all_records(
    p_cursor OUT SYS_REFCURSOR
  );

  PROCEDURE update_record(
    p_id IN NUMBER,
    p_name IN VARCHAR2,
    p_description IN VARCHAR2
  );

  PROCEDURE delete_record(
    p_id IN NUMBER
  );
END pkg_{table_name}_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_{table_name}_ops IS

  PROCEDURE insert_record(
    p_name IN VARCHAR2,
    p_description IN VARCHAR2,
    p_id OUT NUMBER
  ) IS
  BEGIN
    sp_{table_name}_insert(p_name, p_description, 'ACTIVE', p_id);
  END insert_record;

  PROCEDURE get_record(
    p_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
  ) IS
  BEGIN
    sp_{table_name}_get(p_id, p_cursor);
  END get_record;

  PROCEDURE get_all_records(
    p_cursor OUT SYS_REFCURSOR
  ) IS
  BEGIN
    sp_{table_name}_get_all(p_cursor);
  END get_all_records;

  PROCEDURE update_record(
    p_id IN NUMBER,
    p_name IN VARCHAR2,
    p_description IN VARCHAR2
  ) IS
  BEGIN
    sp_{table_name}_update(p_id, p_name, p_description, NULL);
  END update_record;

  PROCEDURE delete_record(
    p_id IN NUMBER
  ) IS
  BEGIN
    sp_{table_name}_delete(p_id);
  END delete_record;

END pkg_{table_name}_ops;
/

-- ============================================================
-- End of CRUD Procedures
-- ============================================================
"""

    @staticmethod
    def get_oracle_best_practices() -> dict:
        """Get Oracle and PL/SQL best practices."""
        return {
            "naming_conventions": [
                "Tables: SINGULAR_LOWERCASE (e.g., user_account)",
                "Columns: LOWERCASE_WITH_UNDERSCORE",
                "Procedures: sp_TABLE_OPERATION",
                "Packages: pkg_FUNCTIONALITY",
                "Indexes: idx_TABLE_COLUMN",
                "Constraints: constraint_TYPE_TABLE",
            ],
            "performance": [
                "Use indexes on frequently queried columns",
                "Partition large tables",
                "Use materialized views for complex queries",
                "Implement table compression",
                "Use cursor caching",
                "Avoid N+1 queries",
            ],
            "security": [
                "Use parameterized queries",
                "Implement row-level security",
                "Encrypt sensitive data",
                "Audit database changes",
                "Use virtual private database (VPD)",
            ],
            "maintenance": [
                "Regular backups (daily)",
                "Monitor table fragmentation",
                "Analyze tables regularly",
                "Keep statistics updated",
                "Archive old data",
            ],
        }

    @staticmethod
    def generate_migration_script(version: str = "001") -> str:
        """Generate database migration script."""
        return f"""-- ============================================================
-- Database Migration Script v{version}
-- Description: Initial schema setup
-- Author: Database Admin
-- Date: $(date '+%Y-%m-%d')
-- ============================================================

-- Enable SQL*Loader if needed
-- @$ORACLE_HOME/rdbms/admin/sqlldr

-- Begin Transaction
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN
  -- Start Migration
  DBMS_OUTPUT.PUT_LINE('Starting migration v{version}...');

  -- Add your DDL statements here

  -- End Migration
  DBMS_OUTPUT.PUT_LINE('Migration v{version} completed successfully');
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error in migration: ' || SQLERRM);
    ROLLBACK;
    RAISE;
END;
/

-- ============================================================
-- Verify Migration
-- ============================================================

SELECT COUNT(*) AS tables_count FROM user_tables;
SELECT COUNT(*) AS procedures_count FROM user_procedures;
SELECT COUNT(*) AS sequences_count FROM user_sequences;

-- ============================================================
-- End of Migration Script
-- ============================================================
"""

    @staticmethod
    def generate_oracle_setup_script() -> str:
        """Generate Oracle setup shell script."""
        return """#!/bin/bash

echo "🗄️  Oracle Database Setup Script"
echo "=============================="

# Check Oracle installation
if ! command -v sqlplus &> /dev/null; then
    echo "❌ Oracle SQL*Plus not found"
    exit 1
fi

echo "✓ Oracle SQL*Plus found"

# Set Oracle environment
export ORACLE_HOME=${ORACLE_HOME:-/opt/oracle/product/23c/dbhome_1}
export PATH=$ORACLE_HOME/bin:$PATH

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p migrations
mkdir -p procedures
mkdir -p tables
mkdir -p packages

echo "✓ Directories created"

# Create SQL scripts
echo ""
echo "📝 Creating SQL scripts..."

cat > migrations/001_init.sql << 'EOF'
-- Initial database setup
CREATE TABLESPACE app_ts DATAFILE 'app_01.dbf' SIZE 100M AUTOEXTEND ON;
CREATE USER appuser IDENTIFIED BY apppass DEFAULT TABLESPACE app_ts;
GRANT DBA TO appuser;
EOF

echo "✓ SQL scripts created"

# Initialize git
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial database setup"
fi

echo ""
echo "✅ Database setup complete!"
echo ""
echo "Next steps:"
echo "  sqlplus /nolog       - Login to SQL*Plus"
echo "  @migrations/001_init - Run migration"
"""
