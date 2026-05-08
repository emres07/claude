-- Create meetingnotes table
-- Part of None
CREATE TABLE meetingnotes (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    content CLOB NOT NULL,
    summary CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_meetingnotes_id ON meetingnotes(id);
CREATE INDEX idx_meetingnotes_created_at ON meetingnotes(created_at);

-- Create unique constraints if needed
COMMIT;