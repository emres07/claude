-- Create token table
-- Part of None
CREATE TABLE token (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_token_id ON token(id);
CREATE INDEX idx_token_created_at ON token(created_at);

-- Create unique constraints if needed
COMMIT;