-- V001_create_users_table.sql
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
