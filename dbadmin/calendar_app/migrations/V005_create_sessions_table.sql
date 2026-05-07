-- V004_create_sessions_table.sql
-- Create sessions table for session management and authentication
-- Tracks active sessions for security and audit purposes

CREATE TABLE sessions (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    token_hash VARCHAR2(255) NOT NULL UNIQUE,
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500),
    expires_at TIMESTAMP NOT NULL,
    revoked NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT chk_sessions_revoked CHECK (revoked IN (0, 1))
);

-- Create indexes for session lookups
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);

-- Create index for active sessions
CREATE INDEX idx_sessions_active ON sessions(user_id, expires_at, revoked);

-- Create procedure to cleanup expired sessions
CREATE OR REPLACE PROCEDURE sp_cleanup_expired_sessions
IS
    v_deleted_count NUMBER;
BEGIN
    DELETE FROM sessions
    WHERE expires_at < SYSTIMESTAMP OR revoked = 1;

    v_deleted_count := SQL%ROWCOUNT;
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Cleaned up ' || v_deleted_count || ' sessions');
END sp_cleanup_expired_sessions;
/

-- Create update trigger for updated_at
CREATE OR REPLACE TRIGGER trg_sessions_updated_at
BEFORE UPDATE ON sessions
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/

COMMIT;
