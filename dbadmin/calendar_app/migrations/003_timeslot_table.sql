-- Create timeslot table
-- Part of None
CREATE TABLE timeslot (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_timeslot_id ON timeslot(id);
CREATE INDEX idx_timeslot_created_at ON timeslot(created_at);

-- Create unique constraints if needed
COMMIT;