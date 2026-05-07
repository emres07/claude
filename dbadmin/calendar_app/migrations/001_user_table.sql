-- Create user table
-- Part of None
CREATE TABLE user (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR2(255) NOT NULL UNIQUE,
    name VARCHAR2(255) NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_user_id ON user(id);
CREATE INDEX idx_user_created_at ON user(created_at);

-- Create unique constraints if needed
COMMIT;