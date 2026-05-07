-- Create completionrecord table
-- Part of None
CREATE TABLE completionrecord (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_completionrecord_id ON completionrecord(id);
CREATE INDEX idx_completionrecord_created_at ON completionrecord(created_at);

-- Create unique constraints if needed
COMMIT;