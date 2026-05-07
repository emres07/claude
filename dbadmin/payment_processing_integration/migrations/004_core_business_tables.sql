-- Core Business Logic Tables
-- ============================================================
-- Table: RESOURCES
-- ============================================================

CREATE TABLE resources (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE resources ADD CONSTRAINT pk_resources PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_resources_created_at ON resources(created_at);
CREATE INDEX idx_resources_updated_at ON resources(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER resources_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON resources
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO resources_audit (audit_id, table_name, operation, user_name)
    VALUES (resources_seq.NEXTVAL, 'resources', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO resources_audit (audit_id, table_name, operation, user_name)
    VALUES (resources_seq.NEXTVAL, 'resources', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO resources_audit (audit_id, table_name, operation, user_name)
    VALUES (resources_seq.NEXTVAL, 'resources', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE resources IS 'Resources master table';
COMMENT ON COLUMN resources.id IS 'Primary Key';
COMMENT ON COLUMN resources.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN resources.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: WORKFLOWS
-- ============================================================

CREATE TABLE workflows (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE workflows ADD CONSTRAINT pk_workflows PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_workflows_created_at ON workflows(created_at);
CREATE INDEX idx_workflows_updated_at ON workflows(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER workflows_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON workflows
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO workflows_audit (audit_id, table_name, operation, user_name)
    VALUES (workflows_seq.NEXTVAL, 'workflows', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO workflows_audit (audit_id, table_name, operation, user_name)
    VALUES (workflows_seq.NEXTVAL, 'workflows', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO workflows_audit (audit_id, table_name, operation, user_name)
    VALUES (workflows_seq.NEXTVAL, 'workflows', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE workflows IS 'Workflows master table';
COMMENT ON COLUMN workflows.id IS 'Primary Key';
COMMENT ON COLUMN workflows.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN workflows.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: TRANSACTIONS
-- ============================================================

CREATE TABLE transactions (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE transactions ADD CONSTRAINT pk_transactions PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_updated_at ON transactions(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER transactions_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON transactions
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO transactions_audit (audit_id, table_name, operation, user_name)
    VALUES (transactions_seq.NEXTVAL, 'transactions', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO transactions_audit (audit_id, table_name, operation, user_name)
    VALUES (transactions_seq.NEXTVAL, 'transactions', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO transactions_audit (audit_id, table_name, operation, user_name)
    VALUES (transactions_seq.NEXTVAL, 'transactions', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE transactions IS 'Transactions master table';
COMMENT ON COLUMN transactions.id IS 'Primary Key';
COMMENT ON COLUMN transactions.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN transactions.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

