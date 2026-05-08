-- Create auditlog table
-- Part of None
CREATE TABLE auditlog (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    entity_type VARCHAR2(255) NOT NULL,
    entity_id NUMBER(19),
    operation VARCHAR2(50) NOT NULL,
    changes CLOB,
    user_id VARCHAR2(255),
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_auditlog_id ON auditlog(id);
CREATE INDEX idx_auditlog_created_at ON auditlog(created_at);

-- Create unique constraints if needed
COMMIT;