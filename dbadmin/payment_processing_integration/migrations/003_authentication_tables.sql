-- Authentication & Authorization Tables
-- ============================================================
-- Table: SESSIONS
-- ============================================================

CREATE TABLE sessions (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE sessions ADD CONSTRAINT pk_sessions PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
CREATE INDEX idx_sessions_updated_at ON sessions(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER sessions_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON sessions
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO sessions_audit (audit_id, table_name, operation, user_name)
    VALUES (sessions_seq.NEXTVAL, 'sessions', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO sessions_audit (audit_id, table_name, operation, user_name)
    VALUES (sessions_seq.NEXTVAL, 'sessions', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO sessions_audit (audit_id, table_name, operation, user_name)
    VALUES (sessions_seq.NEXTVAL, 'sessions', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE sessions IS 'Sessions master table';
COMMENT ON COLUMN sessions.id IS 'Primary Key';
COMMENT ON COLUMN sessions.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN sessions.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: ROLES
-- ============================================================

CREATE TABLE roles (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE roles ADD CONSTRAINT pk_roles PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_roles_created_at ON roles(created_at);
CREATE INDEX idx_roles_updated_at ON roles(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER roles_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON roles
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO roles_audit (audit_id, table_name, operation, user_name)
    VALUES (roles_seq.NEXTVAL, 'roles', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO roles_audit (audit_id, table_name, operation, user_name)
    VALUES (roles_seq.NEXTVAL, 'roles', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO roles_audit (audit_id, table_name, operation, user_name)
    VALUES (roles_seq.NEXTVAL, 'roles', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE roles IS 'Roles master table';
COMMENT ON COLUMN roles.id IS 'Primary Key';
COMMENT ON COLUMN roles.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN roles.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: USERROLES
-- ============================================================

CREATE TABLE userroles (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE userroles ADD CONSTRAINT pk_userroles PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_userroles_created_at ON userroles(created_at);
CREATE INDEX idx_userroles_updated_at ON userroles(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER userroles_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON userroles
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO userroles_audit (audit_id, table_name, operation, user_name)
    VALUES (userroles_seq.NEXTVAL, 'userroles', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO userroles_audit (audit_id, table_name, operation, user_name)
    VALUES (userroles_seq.NEXTVAL, 'userroles', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO userroles_audit (audit_id, table_name, operation, user_name)
    VALUES (userroles_seq.NEXTVAL, 'userroles', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE userroles IS 'Userroles master table';
COMMENT ON COLUMN userroles.id IS 'Primary Key';
COMMENT ON COLUMN userroles.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN userroles.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

