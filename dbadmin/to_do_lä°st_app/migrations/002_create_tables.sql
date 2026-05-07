-- ============================================================
-- VERSION 002: Create Tables
-- ============================================================

-- ============================================================
-- Table: USER
-- ============================================================

CREATE TABLE user (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE user ADD CONSTRAINT pk_user PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_user_created_at ON user(created_at);
CREATE INDEX idx_user_updated_at ON user(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER user_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON user
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO user_audit (audit_id, table_name, operation, user_name)
    VALUES (user_seq.NEXTVAL, 'user', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO user_audit (audit_id, table_name, operation, user_name)
    VALUES (user_seq.NEXTVAL, 'user', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO user_audit (audit_id, table_name, operation, user_name)
    VALUES (user_seq.NEXTVAL, 'user', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE user IS 'User master table';
COMMENT ON COLUMN user.id IS 'Primary Key';
COMMENT ON COLUMN user.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN user.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: TRANSACTION
-- ============================================================

CREATE TABLE transaction (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE transaction ADD CONSTRAINT pk_transaction PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_transaction_created_at ON transaction(created_at);
CREATE INDEX idx_transaction_updated_at ON transaction(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER transaction_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON transaction
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO transaction_audit (audit_id, table_name, operation, user_name)
    VALUES (transaction_seq.NEXTVAL, 'transaction', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO transaction_audit (audit_id, table_name, operation, user_name)
    VALUES (transaction_seq.NEXTVAL, 'transaction', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO transaction_audit (audit_id, table_name, operation, user_name)
    VALUES (transaction_seq.NEXTVAL, 'transaction', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE transaction IS 'Transaction master table';
COMMENT ON COLUMN transaction.id IS 'Primary Key';
COMMENT ON COLUMN transaction.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN transaction.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: AUDIT
-- ============================================================

CREATE TABLE audit (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE audit ADD CONSTRAINT pk_audit PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_audit_created_at ON audit(created_at);
CREATE INDEX idx_audit_updated_at ON audit(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER audit_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON audit
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO audit_audit (audit_id, table_name, operation, user_name)
    VALUES (audit_seq.NEXTVAL, 'audit', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO audit_audit (audit_id, table_name, operation, user_name)
    VALUES (audit_seq.NEXTVAL, 'audit', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO audit_audit (audit_id, table_name, operation, user_name)
    VALUES (audit_seq.NEXTVAL, 'audit', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE audit IS 'Audit master table';
COMMENT ON COLUMN audit.id IS 'Primary Key';
COMMENT ON COLUMN audit.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN audit.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

