-- ============================================================
-- Schema Creation Script for to_do_lä°st_app
-- ============================================================

-- Create Tablespace
CREATE TABLESPACE to_do_lä°st_app_ts
  DATAFILE '/opt/oracle/oradata/to_do_lä°st_app_01.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Create Schema/User
CREATE USER to_do_lä°st_app IDENTIFIED BY welcome123
  DEFAULT TABLESPACE to_do_lä°st_app_ts
  QUOTA UNLIMITED ON to_do_lä°st_app_ts;

-- Grant Privileges
GRANT CREATE SESSION TO to_do_lä°st_app;
GRANT CREATE TABLE TO to_do_lä°st_app;
GRANT CREATE SEQUENCE TO to_do_lä°st_app;
GRANT CREATE PROCEDURE TO to_do_lä°st_app;
GRANT CREATE TRIGGER TO to_do_lä°st_app;
GRANT UNLIMITED TABLESPACE TO to_do_lä°st_app;

-- ============================================================
-- Sequences
-- ============================================================

CREATE SEQUENCE to_do_lä°st_app_seq
  START WITH 1
  INCREMENT BY 1
  NOCYCLE
  NOCACHE;

-- ============================================================
-- Audit Tables
-- ============================================================

CREATE TABLE to_do_lä°st_app_audit (
  audit_id NUMBER PRIMARY KEY,
  table_name VARCHAR2(30),
  operation VARCHAR2(10),
  operation_time TIMESTAMP DEFAULT SYSTIMESTAMP,
  user_name VARCHAR2(30)
);

-- ============================================================
-- End of Schema Creation Script
-- ============================================================
