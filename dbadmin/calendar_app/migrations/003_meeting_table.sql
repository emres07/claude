-- Create meeting table
-- Part of None
CREATE TABLE meeting (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR2(255) NOT NULL,
    description CLOB,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR2(255),
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_meeting_id ON meeting(id);
CREATE INDEX idx_meeting_created_at ON meeting(created_at);

-- Create unique constraints if needed
COMMIT;