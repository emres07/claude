-- ============================================================
-- Schema Creation Script for calendar_app
-- ============================================================

-- Create Tablespace
CREATE TABLESPACE calendar_app_ts
  DATAFILE '/opt/oracle/oradata/calendar_app_01.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Create Schema/User
CREATE USER calendar_app IDENTIFIED BY welcome123
  DEFAULT TABLESPACE calendar_app_ts
  QUOTA UNLIMITED ON calendar_app_ts;

-- Grant Privileges
GRANT CREATE SESSION TO calendar_app;
GRANT CREATE TABLE TO calendar_app;
GRANT CREATE SEQUENCE TO calendar_app;
GRANT CREATE PROCEDURE TO calendar_app;
GRANT CREATE TRIGGER TO calendar_app;
GRANT UNLIMITED TABLESPACE TO calendar_app;

-- ============================================================
-- Sequences
-- ============================================================

CREATE SEQUENCE calendar_app_seq
  START WITH 1
  INCREMENT BY 1
  NOCYCLE
  NOCACHE;

-- ============================================================
-- Audit Tables
-- ============================================================

CREATE TABLE calendar_app_audit (
  audit_id NUMBER PRIMARY KEY,
  table_name VARCHAR2(30),
  operation VARCHAR2(10),
  operation_time TIMESTAMP DEFAULT SYSTIMESTAMP,
  user_name VARCHAR2(30)
);

-- ============================================================
-- End of Schema Creation Script
-- ============================================================
