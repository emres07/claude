-- Create calendar table
-- Part of None
CREATE TABLE calendar (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_calendar_id ON calendar(id);
CREATE INDEX idx_calendar_created_at ON calendar(created_at);

-- Create unique constraints if needed
COMMIT;