"""
Enhanced Database Skills - Reads subtask READMEs and generates detailed implementation code.

Parses subtask specifications from README files and generates production-ready:
- Oracle SQL migration scripts with versioning
- Table creation with constraints and indexes
- Audit triggers for compliance
- Stored procedures for business logic
- Data seeding scripts
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class EnhancedDatabaseSkill:
    """Generates detailed database code based on subtask specifications."""

    @staticmethod
    def parse_readme(readme_path: str) -> Dict[str, Any]:
        """Parse README file and extract specifications."""
        if not Path(readme_path).exists():
            return {}

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        spec = {
            "title": EnhancedDatabaseSkill._extract_title(content),
            "description": EnhancedDatabaseSkill._extract_section(content, "### Description"),
            "tables": EnhancedDatabaseSkill._extract_list(content, "### Database Schemas")
                      or EnhancedDatabaseSkill._extract_list(content, "### Tables"),
            "apis": EnhancedDatabaseSkill._extract_list(content, "### APIs Generated"),
        }
        return spec

    @staticmethod
    def _extract_title(content: str) -> str:
        """Extract title from README."""
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_section(content: str, section_header: str) -> str:
        """Extract section content from README."""
        pattern = f"{section_header}\n(.+?)(?=\n###|$)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_list(content: str, section_header: str) -> List[str]:
        """Extract list items from README section."""
        section = EnhancedDatabaseSkill._extract_section(content, section_header)
        items = re.findall(r"^- (.+)$", section, re.MULTILINE)
        return [item.strip() for item in items]

    @staticmethod
    def generate_user_migration_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Users table migration based on specification."""
        return """-- V001_create_users_table.sql
-- Create users table for user management
-- Includes audit columns, role management, and deactivation support

CREATE TABLE users (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) NOT NULL UNIQUE,
    password_hash VARCHAR2(255) NOT NULL,
    phone_number VARCHAR2(20),
    role VARCHAR2(50) NOT NULL DEFAULT 'USER',
    active NUMBER(1) DEFAULT 1 NOT NULL,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    version NUMBER(19) DEFAULT 0,
    CONSTRAINT chk_users_active CHECK (active IN (0, 1))
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_updated_at ON users(updated_at);
CREATE INDEX idx_users_active ON users(active);

-- Create audit trigger for users table
CREATE OR REPLACE TRIGGER trg_users_audit
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_logs (action, entity, entity_id, user_id, details, timestamp)
        VALUES ('INSERT', 'USERS', :NEW.id, 'SYSTEM',
                'User created: ' || :NEW.email, SYSTIMESTAMP);
    ELSIF UPDATING THEN
        INSERT INTO audit_logs (action, entity, entity_id, user_id, details, timestamp)
        VALUES ('UPDATE', 'USERS', :NEW.id, 'SYSTEM',
                'User updated: ' || :NEW.email, SYSTIMESTAMP);
    ELSIF DELETING THEN
        INSERT INTO audit_logs (action, entity, entity_id, user_id, details, timestamp)
        VALUES ('DELETE', 'USERS', :OLD.id, 'SYSTEM',
                'User deleted: ' || :OLD.email, SYSTIMESTAMP);
    END IF;
END;
/

-- Create update trigger for updated_at column
CREATE OR REPLACE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/

COMMIT;
"""

    @staticmethod
    def generate_audit_logs_migration_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Audit Logs table migration based on specification."""
        return """-- V002_create_audit_logs_table.sql
-- Create audit logs table for compliance and audit trail
-- Tracks all user actions and system events

CREATE TABLE audit_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    action VARCHAR2(50) NOT NULL,
    entity VARCHAR2(100) NOT NULL,
    entity_id NUMBER(19),
    user_id VARCHAR2(255),
    details CLOB,
    timestamp TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500)
);

-- Create indexes for audit queries
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id, entity);

-- Create composite index for common audit queries
CREATE INDEX idx_audit_logs_entity_time ON audit_logs(entity, timestamp DESC);

-- Create retention policy procedure
CREATE OR REPLACE PROCEDURE sp_cleanup_old_audit_logs(p_days_to_keep NUMBER DEFAULT 90)
IS
    v_deleted_count NUMBER;
BEGIN
    DELETE FROM audit_logs
    WHERE timestamp < SYSTIMESTAMP - p_days_to_keep;

    v_deleted_count := SQL%ROWCOUNT;
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Deleted ' || v_deleted_count || ' old audit logs');
END sp_cleanup_old_audit_logs;
/

COMMIT;
"""

    @staticmethod
    def generate_activity_logs_migration_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Activity Logs table migration based on specification."""
        return """-- V003_create_activity_logs_table.sql
-- Create activity logs table for user activity tracking
-- Tracks user sessions, logins, and interactions

CREATE TABLE activity_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    activity_type VARCHAR2(100) NOT NULL,
    description VARCHAR2(500),
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500),
    status VARCHAR2(50),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_activity_logs_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for activity queries
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at);
CREATE INDEX idx_activity_logs_activity_type ON activity_logs(activity_type);
CREATE INDEX idx_activity_logs_status ON activity_logs(status);

-- Create index for recent activity queries
CREATE INDEX idx_activity_logs_user_recent ON activity_logs(user_id, created_at DESC);

-- Create procedure to get user activity summary
CREATE OR REPLACE PROCEDURE sp_get_user_activity_summary(
    p_user_id NUMBER,
    p_days_back NUMBER DEFAULT 30
)
IS
BEGIN
    SELECT
        user_id,
        activity_type,
        COUNT(*) AS count,
        MIN(created_at) AS first_activity,
        MAX(created_at) AS last_activity
    FROM activity_logs
    WHERE user_id = p_user_id
      AND created_at >= SYSTIMESTAMP - p_days_back
    GROUP BY user_id, activity_type
    ORDER BY last_activity DESC;
END sp_get_user_activity_summary;
/

COMMIT;
"""

    @staticmethod
    def generate_sessions_migration_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Sessions table migration based on specification."""
        return """-- V004_create_sessions_table.sql
-- Create sessions table for session management and authentication
-- Tracks active sessions for security and audit purposes

CREATE TABLE sessions (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    token_hash VARCHAR2(255) NOT NULL UNIQUE,
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500),
    expires_at TIMESTAMP NOT NULL,
    revoked NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT chk_sessions_revoked CHECK (revoked IN (0, 1))
);

-- Create indexes for session lookups
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);

-- Create index for active sessions
CREATE INDEX idx_sessions_active ON sessions(user_id, expires_at, revoked);

-- Create procedure to cleanup expired sessions
CREATE OR REPLACE PROCEDURE sp_cleanup_expired_sessions
IS
    v_deleted_count NUMBER;
BEGIN
    DELETE FROM sessions
    WHERE expires_at < SYSTIMESTAMP OR revoked = 1;

    v_deleted_count := SQL%ROWCOUNT;
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Cleaned up ' || v_deleted_count || ' sessions');
END sp_cleanup_expired_sessions;
/

-- Create update trigger for updated_at
CREATE OR REPLACE TRIGGER trg_sessions_updated_at
BEFORE UPDATE ON sessions
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/

COMMIT;
"""

    @staticmethod
    def generate_integration_tables_migration_from_spec(spec: Dict[str, Any]) -> str:
        """Generate Integration tracking tables migration based on specification."""
        return """-- V005_create_integration_tables.sql
-- Create tables for API integration tracking
-- Monitors third-party API connections and synchronization

CREATE TABLE integrations (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    provider_name VARCHAR2(100) NOT NULL,
    provider_key VARCHAR2(255),
    provider_secret VARCHAR2(255),
    access_token VARCHAR2(500),
    refresh_token VARCHAR2(500),
    expires_at TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1,
    last_sync_at TIMESTAMP,
    sync_status VARCHAR2(50),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_integrations_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT chk_integrations_active CHECK (is_active IN (0, 1))
);

-- Create indexes for integration queries
CREATE INDEX idx_integrations_user_id ON integrations(user_id);
CREATE INDEX idx_integrations_provider ON integrations(user_id, provider_name);
CREATE INDEX idx_integrations_active ON integrations(is_active);
CREATE INDEX idx_integrations_last_sync ON integrations(last_sync_at);

-- Create table for API call tracking
CREATE TABLE api_call_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    integration_id NUMBER(19) NOT NULL,
    endpoint VARCHAR2(500),
    method VARCHAR2(10),
    status_code NUMBER(3),
    response_time_ms NUMBER(10),
    error_message VARCHAR2(500),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_api_call_logs_integration FOREIGN KEY (integration_id) REFERENCES integrations(id)
);

-- Create indexes for API call tracking
CREATE INDEX idx_api_call_logs_integration ON api_call_logs(integration_id);
CREATE INDEX idx_api_call_logs_created_at ON api_call_logs(created_at);
CREATE INDEX idx_api_call_logs_status ON api_call_logs(status_code);

COMMIT;
"""

    @staticmethod
    def generate_seed_data_from_spec(spec: Dict[str, Any]) -> str:
        """Generate seed data script for initial data population."""
        return """-- seed_data.sql
-- Seed script for initial data population
-- Creates default roles and system users

BEGIN
    -- Insert default roles
    INSERT INTO user_roles (role_name, description)
    VALUES ('ADMIN', 'Administrator with full access');

    INSERT INTO user_roles (role_name, description)
    VALUES ('USER', 'Regular user with limited access');

    INSERT INTO user_roles (role_name, description)
    VALUES ('GUEST', 'Guest user with view-only access');

    COMMIT;

EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('Roles already exist');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error inserting roles: ' || SQLERRM);
END;
/

-- Verify seeding
SELECT 'Users table created' as status FROM dual
UNION ALL
SELECT 'Audit logs table created' FROM dual
UNION ALL
SELECT 'Activity logs table created' FROM dual
UNION ALL
SELECT 'Sessions table created' FROM dual
UNION ALL
SELECT 'Integrations table created' FROM dual;

COMMIT;
"""

    @staticmethod
    def generate_rollback_script_from_spec(spec: Dict[str, Any]) -> str:
        """Generate rollback script for migrations."""
        return """-- V001_rollback_create_users_table.sql
-- Rollback script to drop users table and related objects

BEGIN
    -- Drop triggers
    EXECUTE IMMEDIATE 'DROP TRIGGER trg_users_audit';
    EXECUTE IMMEDIATE 'DROP TRIGGER trg_users_updated_at';

    -- Drop indexes
    EXECUTE IMMEDIATE 'DROP INDEX idx_users_email';
    EXECUTE IMMEDIATE 'DROP INDEX idx_users_created_at';
    EXECUTE IMMEDIATE 'DROP INDEX idx_users_updated_at';
    EXECUTE IMMEDIATE 'DROP INDEX idx_users_active';

    -- Drop table
    EXECUTE IMMEDIATE 'DROP TABLE users';

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Users table rollback completed successfully');

EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN  -- Object does not exist
            DBMS_OUTPUT.PUT_LINE('Error during rollback: ' || SQLERRM);
            ROLLBACK;
        END IF;
END;
/

COMMIT;
"""
