-- Create permission table
-- Part of None
CREATE TABLE permission (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_permission_id ON permission(id);
CREATE INDEX idx_permission_created_at ON permission(created_at);

-- Create unique constraints if needed
COMMIT;