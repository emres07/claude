-- Audit & Monitoring Tables
-- ============================================================
-- Table: AUDITLOGS
-- ============================================================

CREATE TABLE auditlogs (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE auditlogs ADD CONSTRAINT pk_auditlogs PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_auditlogs_created_at ON auditlogs(created_at);
CREATE INDEX idx_auditlogs_updated_at ON auditlogs(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER auditlogs_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON auditlogs
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO auditlogs_audit (audit_id, table_name, operation, user_name)
    VALUES (auditlogs_seq.NEXTVAL, 'auditlogs', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO auditlogs_audit (audit_id, table_name, operation, user_name)
    VALUES (auditlogs_seq.NEXTVAL, 'auditlogs', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO auditlogs_audit (audit_id, table_name, operation, user_name)
    VALUES (auditlogs_seq.NEXTVAL, 'auditlogs', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE auditlogs IS 'Auditlogs master table';
COMMENT ON COLUMN auditlogs.id IS 'Primary Key';
COMMENT ON COLUMN auditlogs.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN auditlogs.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: ACTIVITYLOGS
-- ============================================================

CREATE TABLE activitylogs (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE activitylogs ADD CONSTRAINT pk_activitylogs PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_activitylogs_created_at ON activitylogs(created_at);
CREATE INDEX idx_activitylogs_updated_at ON activitylogs(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER activitylogs_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON activitylogs
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO activitylogs_audit (audit_id, table_name, operation, user_name)
    VALUES (activitylogs_seq.NEXTVAL, 'activitylogs', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO activitylogs_audit (audit_id, table_name, operation, user_name)
    VALUES (activitylogs_seq.NEXTVAL, 'activitylogs', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO activitylogs_audit (audit_id, table_name, operation, user_name)
    VALUES (activitylogs_seq.NEXTVAL, 'activitylogs', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE activitylogs IS 'Activitylogs master table';
COMMENT ON COLUMN activitylogs.id IS 'Primary Key';
COMMENT ON COLUMN activitylogs.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN activitylogs.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

-- ============================================================
-- Table: SYSTEMEVENTS
-- ============================================================

CREATE TABLE systemevents (
  id NUMBER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
  name VARCHAR2(100) NOT NULL,
  description VARCHAR2(500) NULL,
  status VARCHAR2(20) NOT NULL DEFAULT 'ACTIVE'
);

-- Create Primary Key
ALTER TABLE systemevents ADD CONSTRAINT pk_systemevents PRIMARY KEY (id);

-- Create Indexes
CREATE INDEX idx_systemevents_created_at ON systemevents(created_at);
CREATE INDEX idx_systemevents_updated_at ON systemevents(updated_at);

-- Create Audit Trigger
CREATE OR REPLACE TRIGGER systemevents_audit_trg
BEFORE INSERT OR UPDATE OR DELETE ON systemevents
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO systemevents_audit (audit_id, table_name, operation, user_name)
    VALUES (systemevents_seq.NEXTVAL, 'systemevents', 'INSERT', USER);
  ELSIF UPDATING THEN
    INSERT INTO systemevents_audit (audit_id, table_name, operation, user_name)
    VALUES (systemevents_seq.NEXTVAL, 'systemevents', 'UPDATE', USER);
  ELSIF DELETING THEN
    INSERT INTO systemevents_audit (audit_id, table_name, operation, user_name)
    VALUES (systemevents_seq.NEXTVAL, 'systemevents', 'DELETE', USER);
  END IF;
END;
/

-- ============================================================
-- Comments for Documentation
-- ============================================================

COMMENT ON TABLE systemevents IS 'Systemevents master table';
COMMENT ON COLUMN systemevents.id IS 'Primary Key';
COMMENT ON COLUMN systemevents.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN systemevents.updated_at IS 'Last update timestamp';

-- ============================================================
-- End of Table Creation Script
-- ============================================================

