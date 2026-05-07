-- Create notification table
-- Part of None
CREATE TABLE notification (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_notification_id ON notification(id);
CREATE INDEX idx_notification_created_at ON notification(created_at);

-- Create unique constraints if needed
COMMIT;