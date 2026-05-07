-- API Integration Tables
-- ============================================================
-- Table: APILOGS
-- ============================================================

CREATE TABLE apilogs (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE apilogs ADD CONSTRAINT pk_apilogs PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_apilogs_created_at ON apilogs(created_at);
CREATE INDEX idx_apilogs_updated_at ON apilogs(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER apilogs_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON apilogs
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO apilogs_audit (audit_id, table_name, operation, user_name)
    VALUES (apilogs_seq.NEXTVAL, 'apilogs', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO apilogs_audit (audit_id, table_name, operation, user_name)
    VALUES (apilogs_seq.NEXTVAL, 'apilogs', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO apilogs_audit (audit_id, table_name, operation, user_name)
    VALUES (apilogs_seq.NEXTVAL, 'apilogs', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE apilogs IS 'Apilogs master table';
COMMENT ON COLUMN apilogs.id IS 'Primary Key';
COMMENT ON COLUMN apilogs.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN apilogs.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: WEBHOOKS
-- ============================================================

CREATE TABLE webhooks (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE webhooks ADD CONSTRAINT pk_webhooks PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_webhooks_created_at ON webhooks(created_at);
CREATE INDEX idx_webhooks_updated_at ON webhooks(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER webhooks_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON webhooks
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO webhooks_audit (audit_id, table_name, operation, user_name)
    VALUES (webhooks_seq.NEXTVAL, 'webhooks', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO webhooks_audit (audit_id, table_name, operation, user_name)
    VALUES (webhooks_seq.NEXTVAL, 'webhooks', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO webhooks_audit (audit_id, table_name, operation, user_name)
    VALUES (webhooks_seq.NEXTVAL, 'webhooks', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE webhooks IS 'Webhooks master table';
COMMENT ON COLUMN webhooks.id IS 'Primary Key';
COMMENT ON COLUMN webhooks.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN webhooks.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: INTEGRATIONS
-- ============================================================

CREATE TABLE integrations (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE integrations ADD CONSTRAINT pk_integrations PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_integrations_created_at ON integrations(created_at);
CREATE INDEX idx_integrations_updated_at ON integrations(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER integrations_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON integrations
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO integrations_audit (audit_id, table_name, operation, user_name)
    VALUES (integrations_seq.NEXTVAL, 'integrations', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO integrations_audit (audit_id, table_name, operation, user_name)
    VALUES (integrations_seq.NEXTVAL, 'integrations', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO integrations_audit (audit_id, table_name, operation, user_name)
    VALUES (integrations_seq.NEXTVAL, 'integrations', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE integrations IS 'Integrations master table';
COMMENT ON COLUMN integrations.id IS 'Primary Key';
COMMENT ON COLUMN integrations.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN integrations.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

