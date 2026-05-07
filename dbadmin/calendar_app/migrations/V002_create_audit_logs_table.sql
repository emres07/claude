-- V002_create_audit_logs_table.sql
-- Create audit logs table for compliance and audit trail
-- Tracks all user actions and system events

CREATE TABLE audit_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    action VARCHAR2(50) NOT NULL,
    entity VARCHAR2(100) NOT NULL,
    entity_id NUMBER(19),
    user_id VARCHAR2(255),
    details CLOB,
    timestamp TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500)
);

-- Create indexes for audit queries
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id, entity);

-- Create composite index for common audit queries
CREATE INDEX idx_audit_logs_entity_time ON audit_logs(entity, timestamp DESC);

-- Create retention policy procedure
CREATE OR REPLACE PROCEDURE sp_cleanup_old_audit_logs(p_days_to_keep NUMBER DEFAULT 90)
IS
    v_deleted_count NUMBER;
BEGIN
    DELETE FROM audit_logs
    WHERE timestamp < SYSTIMESTAMP - p_days_to_keep;

    v_deleted_count := SQL%ROWCOUNT;
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Deleted ' || v_deleted_count || ' old audit logs');
END sp_cleanup_old_audit_logs;
/

COMMIT;
