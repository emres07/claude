-- User Management Tables
-- ============================================================
-- Table: USERS
-- ============================================================

CREATE TABLE users (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE users ADD CONSTRAINT pk_users PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_updated_at ON users(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER users_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO users_audit (audit_id, table_name, operation, user_name)
    VALUES (users_seq.NEXTVAL, 'users', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO users_audit (audit_id, table_name, operation, user_name)
    VALUES (users_seq.NEXTVAL, 'users', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO users_audit (audit_id, table_name, operation, user_name)
    VALUES (users_seq.NEXTVAL, 'users', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE users IS 'Users master table';
COMMENT ON COLUMN users.id IS 'Primary Key';
COMMENT ON COLUMN users.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN users.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: USERPROFILES
-- ============================================================

CREATE TABLE userprofiles (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE userprofiles ADD CONSTRAINT pk_userprofiles PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_userprofiles_created_at ON userprofiles(created_at);
CREATE INDEX idx_userprofiles_updated_at ON userprofiles(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER userprofiles_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON userprofiles
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO userprofiles_audit (audit_id, table_name, operation, user_name)
    VALUES (userprofiles_seq.NEXTVAL, 'userprofiles', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO userprofiles_audit (audit_id, table_name, operation, user_name)
    VALUES (userprofiles_seq.NEXTVAL, 'userprofiles', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO userprofiles_audit (audit_id, table_name, operation, user_name)
    VALUES (userprofiles_seq.NEXTVAL, 'userprofiles', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE userprofiles IS 'Userprofiles master table';
COMMENT ON COLUMN userprofiles.id IS 'Primary Key';
COMMENT ON COLUMN userprofiles.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN userprofiles.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

