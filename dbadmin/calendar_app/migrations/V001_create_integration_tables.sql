-- V005_create_integration_tables.sql
-- Create tables for API integration tracking
-- Monitors third-party API connections and synchronization

CREATE TABLE integrations (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id NUMBER(19) NOT NULL,
    provider_name VARCHAR2(100) NOT NULL,
    provider_key VARCHAR2(255),
    provider_secret VARCHAR2(255),
    access_token VARCHAR2(500),
    refresh_token VARCHAR2(500),
    expires_at TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1,
    last_sync_at TIMESTAMP,
    sync_status VARCHAR2(50),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_integrations_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT chk_integrations_active CHECK (is_active IN (0, 1))
);

-- Create indexes for integration queries
CREATE INDEX idx_integrations_user_id ON integrations(user_id);
CREATE INDEX idx_integrations_provider ON integrations(user_id, provider_name);
CREATE INDEX idx_integrations_active ON integrations(is_active);
CREATE INDEX idx_integrations_last_sync ON integrations(last_sync_at);

-- Create table for API call tracking
CREATE TABLE api_call_logs (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    integration_id NUMBER(19) NOT NULL,
    endpoint VARCHAR2(500),
    method VARCHAR2(10),
    status_code NUMBER(3),
    response_time_ms NUMBER(10),
    error_message VARCHAR2(500),
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_api_call_logs_integration FOREIGN KEY (integration_id) REFERENCES integrations(id)
);

-- Create indexes for API call tracking
CREATE INDEX idx_api_call_logs_integration ON api_call_logs(integration_id);
CREATE INDEX idx_api_call_logs_created_at ON api_call_logs(created_at);
CREATE INDEX idx_api_call_logs_status ON api_call_logs(status_code);

COMMIT;
