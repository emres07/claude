-- Create attendee table
-- Part of None
CREATE TABLE attendee (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_attendee_id ON attendee(id);
CREATE INDEX idx_attendee_created_at ON attendee(created_at);

-- Create unique constraints if needed
COMMIT;