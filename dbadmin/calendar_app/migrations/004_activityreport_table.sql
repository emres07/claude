-- Create activityreport table
-- Part of None
CREATE TABLE activityreport (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_activityreport_id ON activityreport(id);
CREATE INDEX idx_activityreport_created_at ON activityreport(created_at);

-- Create unique constraints if needed
COMMIT;