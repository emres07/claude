-- ============================================================
-- Schema Creation Script for payment_processing_integration
-- ============================================================

-- Create Tablespace
CREATE TABLESPACE payment_processing_integration_ts
  DATAFILE '/opt/oracle/oradata/payment_processing_integration_01.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Create Schema/User
CREATE USER payment_processing_integration IDENTIFIED BY welcome123
  DEFAULT TABLESPACE payment_processing_integration_ts
  QUOTA UNLIMITED ON payment_processing_integration_ts;

-- Grant Privileges
GRANT CREATE SESSION TO payment_processing_integration;
GRANT CREATE TABLE TO payment_processing_integration;
GRANT CREATE SEQUENCE TO payment_processing_integration;
GRANT CREATE PROCEDURE TO payment_processing_integration;
GRANT CREATE TRIGGER TO payment_processing_integration;
GRANT UNLIMITED TABLESPACE TO payment_processing_integration;

-- ============================================================
-- Sequences
-- ============================================================

CREATE SEQUENCE payment_processing_integration_seq
  START WITH 1
  INCREMENT BY 1
  NOCYCLE
  NOCACHE;

-- ============================================================
-- Audit Tables
-- ============================================================

CREATE TABLE payment_processing_integration_audit (
  audit_id NUMBER PRIMARY KEY,
  table_name VARCHAR2(30),
  operation VARCHAR2(10),
  operation_time TIMESTAMP DEFAULT SYSTIMESTAMP,
  user_name VARCHAR2(30)
);

-- ============================================================
-- End of Schema Creation Script
-- ============================================================
