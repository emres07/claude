-- ============================================================
-- Schema Creation Script for user_authentication_system
-- ============================================================

-- Create Tablespace
CREATE TABLESPACE user_authentication_system_ts
  DATAFILE '/opt/oracle/oradata/user_authentication_system_01.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Create Schema/User
CREATE USER user_authentication_system IDENTIFIED BY welcome123
  DEFAULT TABLESPACE user_authentication_system_ts
  QUOTA UNLIMITED ON user_authentication_system_ts;

-- Grant Privileges
GRANT CREATE SESSION TO user_authentication_system;
GRANT CREATE TABLE TO user_authentication_system;
GRANT CREATE SEQUENCE TO user_authentication_system;
GRANT CREATE PROCEDURE TO user_authentication_system;
GRANT CREATE TRIGGER TO user_authentication_system;
GRANT UNLIMITED TABLESPACE TO user_authentication_system;

-- ============================================================
-- Sequences
-- ============================================================

CREATE SEQUENCE user_authentication_system_seq
  START WITH 1
  INCREMENT BY 1
  NOCYCLE
  NOCACHE;

-- ============================================================
-- Audit Tables
-- ============================================================

CREATE TABLE user_authentication_system_audit (
  audit_id NUMBER PRIMARY KEY,
  table_name VARCHAR2(30),
  operation VARCHAR2(10),
  operation_time TIMESTAMP DEFAULT SYSTIMESTAMP,
  user_name VARCHAR2(30)
);

-- ============================================================
-- End of Schema Creation Script
-- ============================================================
