-- Create calendarview table
-- Part of None
CREATE TABLE calendarview (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_calendarview_id ON calendarview(id);
CREATE INDEX idx_calendarview_created_at ON calendarview(created_at);

-- Create unique constraints if needed
COMMIT;