-- V003_create_activity_logs_table.sql
-- Create activity logs table for user activity tracking
-- Tracks user sessions, logins, and interactions

CREATE TABLE activity_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    activity_type VARCHAR2(100) NOT NULL,
    description VARCHAR2(500),
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500),
    status VARCHAR2(50),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_activity_logs_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for activity queries
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at);
CREATE INDEX idx_activity_logs_activity_type ON activity_logs(activity_type);
CREATE INDEX idx_activity_logs_status ON activity_logs(status);

-- Create index for recent activity queries
CREATE INDEX idx_activity_logs_user_recent ON activity_logs(user_id, created_at DESC);

-- Create procedure to get user activity summary
CREATE OR REPLACE PROCEDURE sp_get_user_activity_summary(
    p_user_id NUMBER,
    p_days_back NUMBER DEFAULT 30
)
IS
BEGIN
    SELECT
        user_id,
        activity_type,
        COUNT(*) AS count,
        MIN(created_at) AS first_activity,
        MAX(created_at) AS last_activity
    FROM activity_logs
    WHERE user_id = p_user_id
      AND created_at >= SYSTIMESTAMP - p_days_back
    GROUP BY user_id, activity_type
    ORDER BY last_activity DESC;
END sp_get_user_activity_summary;
/

COMMIT;
