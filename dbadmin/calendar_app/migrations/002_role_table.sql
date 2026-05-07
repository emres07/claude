-- Create role table
-- Part of None
CREATE TABLE role (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_role_id ON role(id);
CREATE INDEX idx_role_created_at ON role(created_at);

-- Create unique constraints if needed
COMMIT;