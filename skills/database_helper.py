"""Database Skill Helper - Provides Oracle database templates with Jinja2."""

from pathlib import Path
from .jinja_template_loader import JinjaTemplateLoader


class DatabaseSkill:
    """Helper for Oracle database code generation with dynamic templates."""

    TEMPLATES_FILE = Path(__file__).parent / "database_templates.md"

    @staticmethod
    def generate_oracle_schema(schema_name: str, password: str = "welcome123") -> str:
        """Generate Oracle schema creation SQL."""
        context = {
            "schema_name": schema_name,
            "password": password
        }
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "oracle_schema", context
        )
        return template

    @staticmethod
    def generate_table_template(
        table_name: str,
        columns: list = None,
        indexes: list = None
    ) -> str:
        """Generate a dynamic table template."""
        table_name = table_name.lower()
        context = {
            "table_name": table_name,
            "columns": columns or [],
            "indexes": indexes or []
        }
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "dynamic_table", context
        )
        return template

    @staticmethod
    def generate_crud_procedures(
        table_name: str,
        columns: list = None
    ) -> str:
        """Generate CRUD stored procedures."""
        table_name = table_name.lower()
        context = {
            "table_name": table_name,
            "columns": columns or []
        }
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "dynamic_crud_procedures", context
        )
        return template

    @staticmethod
    def generate_trigger(
        table_name: str
    ) -> str:
        """Generate audit trigger for table changes."""
        table_name = table_name.lower()
        context = {
            "table_name": table_name
        }
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "dynamic_trigger", context
        )
        return template

    @staticmethod
    def generate_audit_log_table() -> str:
        """Generate audit_log table creation script."""
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "audit_table", {}
        )
        return template

    @staticmethod
    def generate_migration_status(
        current_version: str = "001",
        created_at: str = "2026-05-08",
        migrations: list = None
    ) -> str:
        """Generate migration status JSON."""
        context = {
            "current_version": current_version,
            "created_at": created_at,
            "migrations": migrations or []
        }
        template = JinjaTemplateLoader.render_template(
            str(DatabaseSkill.TEMPLATES_FILE), "migration_status", context
        )
        return template

    # Backward compatibility methods
    @staticmethod
    def generate_flyway_init_schema() -> str:
        """Generate initial Flyway migration for schema setup."""
        return '''-- V001__init_schema.sql
-- Initial schema setup

CREATE TABLE users (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR2(255) NOT NULL UNIQUE,
    name VARCHAR2(100) NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    active NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_active ON users(active);

COMMIT;
'''

    @staticmethod
    def generate_meeting_migration() -> str:
        """Generate migration for meeting tables."""
        return '''-- V002__create_meeting_tables.sql
-- Meeting, Calendar, TimeSlot, and Attendee tables
-- Part of Meeting Management Workflow

CREATE TABLE meeting (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR2(255) NOT NULL,
    description CLOB,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR2(255),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE calendar (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE timeslot (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    available NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE attendee (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    email VARCHAR2(255),
    status VARCHAR2(50),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_meeting_start ON meeting(start_time);
CREATE INDEX idx_calendar_created ON calendar(created_at);
CREATE INDEX idx_timeslot_available ON timeslot(available);

COMMIT;
'''

    @staticmethod
    def generate_audit_migration() -> str:
        """Generate migration for audit tables."""
        return '''-- V003__create_audit_tables.sql
-- Audit logging tables for compliance tracking

CREATE TABLE audit_log (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    entity_type VARCHAR2(255) NOT NULL,
    entity_id NUMBER(19),
    operation VARCHAR2(50) NOT NULL,
    changes CLOB,
    user_id NUMBER(19),
    timestamp TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_user ON audit_log(user_id);

COMMIT;
'''

    @staticmethod
    def generate_session_migration() -> str:
        """Generate migration for session tables."""
        return '''-- V004__create_session_tables.sql
-- User session management tables

CREATE TABLE sessions (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    token VARCHAR2(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_session_token ON sessions(token);
CREATE INDEX idx_session_user ON sessions(user_id);

COMMIT;
'''

    @staticmethod
    def generate_stored_procedure_user_crud() -> str:
        """Generate CRUD stored procedures for users."""
        return '''-- User CRUD Procedures

CREATE OR REPLACE PACKAGE pkg_user_ops AS
    PROCEDURE insert_user(p_email VARCHAR2, p_name VARCHAR2, p_password VARCHAR2, p_id OUT NUMBER);
    PROCEDURE get_user(p_id NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_user(p_id NUMBER, p_email VARCHAR2, p_name VARCHAR2);
    PROCEDURE delete_user(p_id NUMBER);
END pkg_user_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_user_ops AS
    PROCEDURE insert_user(p_email VARCHAR2, p_name VARCHAR2, p_password VARCHAR2, p_id OUT NUMBER) IS
    BEGIN
        INSERT INTO users (email, name, password_hash) VALUES (p_email, p_name, p_password);
        SELECT id INTO p_id FROM users WHERE email = p_email AND ROWNUM = 1;
        COMMIT;
    END insert_user;

    PROCEDURE get_user(p_id NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR SELECT * FROM users WHERE id = p_id;
    END get_user;

    PROCEDURE update_user(p_id NUMBER, p_email VARCHAR2, p_name VARCHAR2) IS
    BEGIN
        UPDATE users SET email = p_email, name = p_name WHERE id = p_id;
        COMMIT;
    END update_user;

    PROCEDURE delete_user(p_id NUMBER) IS
    BEGIN
        DELETE FROM users WHERE id = p_id;
        COMMIT;
    END delete_user;
END pkg_user_ops;
/
'''

    @staticmethod
    def generate_stored_procedure_meeting_crud() -> str:
        """Generate CRUD stored procedures for meetings."""
        return '''-- Meeting CRUD Procedures

CREATE OR REPLACE PACKAGE pkg_meeting_ops AS
    PROCEDURE create_meeting(p_title VARCHAR2, p_description CLOB, p_id OUT NUMBER);
    PROCEDURE get_meeting(p_id NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_meeting(p_id NUMBER, p_title VARCHAR2, p_description CLOB);
    PROCEDURE delete_meeting(p_id NUMBER);
END pkg_meeting_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_meeting_ops AS
    PROCEDURE create_meeting(p_title VARCHAR2, p_description CLOB, p_id OUT NUMBER) IS
    BEGIN
        INSERT INTO meeting (title, description) VALUES (p_title, p_description);
        SELECT id INTO p_id FROM meeting WHERE title = p_title AND ROWNUM = 1;
        COMMIT;
    END create_meeting;

    PROCEDURE get_meeting(p_id NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR SELECT * FROM meeting WHERE id = p_id;
    END get_meeting;

    PROCEDURE update_meeting(p_id NUMBER, p_title VARCHAR2, p_description CLOB) IS
    BEGIN
        UPDATE meeting SET title = p_title, description = p_description WHERE id = p_id;
        COMMIT;
    END update_meeting;

    PROCEDURE delete_meeting(p_id NUMBER) IS
    BEGIN
        DELETE FROM meeting WHERE id = p_id;
        COMMIT;
    END delete_meeting;
END pkg_meeting_ops;
/
'''

    @staticmethod
    def generate_audit_trigger() -> str:
        """Generate audit trigger for change tracking."""
        return '''-- Audit Trigger for Meeting Table Changes

CREATE OR REPLACE TRIGGER trg_meeting_audit
AFTER INSERT OR UPDATE OR DELETE ON meeting
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id)
        VALUES ('MEETING', :NEW.id, 'INSERT', SYS_CONTEXT('USERENV', 'SESSION_USER'));
    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id)
        VALUES ('MEETING', :NEW.id, 'UPDATE', SYS_CONTEXT('USERENV', 'SESSION_USER'));
    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id)
        VALUES ('MEETING', :OLD.id, 'DELETE', SYS_CONTEXT('USERENV', 'SESSION_USER'));
    END IF;
    COMMIT;
END trg_meeting_audit;
/
'''
