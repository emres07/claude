# Database Schema for Audit & Activity Tracking Workflow - Audit & Activity Tracking Workflow - TODO LIST APP

**Created by**: Database Agent
**Agent Role**: database_developer
**Date**: 2026-05-08 08:40:54
**Agent ID**: database_agent

## Description
Implement database schema for Audit & Activity Tracking Workflow workflow.

Workflow Steps:
1. User performs action (create, update, delete)
2. System logs action to audit log
3. System captures timestamp, user, entity, and changes
4. Admin can view audit logs
5. Admin can generate activity reports
6. System maintains historical record for compliance

Data entities to persist: AuditLog, User, Meeting, ActivityReport

## Domain
Database

## Parent Task
audit_&_activity_tracking_workflow___todo_list_app

## Schema Design
**Database Type**: Oracle 21c/23c
### Naming Conventions
- Tables: lowercase with underscores (users, user_profiles)
- Columns: lowercase with underscores
- Constraints: prefix with constraint type (pk_*, uk_*, fk_*)
- Indexes: prefix with idx_ or idx_unique_
**Character Set**: AL32UTF8
### Entities
- audit_logs (activity tracking)

## Tables to Create
- auditlog
- user
- meeting
- activityreport

## Table Specifications
### users
**Columns:**
- id (NUMBER(19), PRIMARY KEY)
- email (VARCHAR2(255), UNIQUE, NOT NULL)
- name (VARCHAR2(100), NOT NULL)
- password_hash (VARCHAR2(255), NOT NULL)
- active (NUMBER(1), DEFAULT 1)
- created_at (TIMESTAMP, DEFAULT SYSTIMESTAMP)
- updated_at (TIMESTAMP, DEFAULT SYSTIMESTAMP)
**Constraints:**
- PRIMARY KEY on id
- UNIQUE constraint on email
- CHECK constraint for active (0 or 1)

### audit_logs
**Columns:**
- id (NUMBER(19), PRIMARY KEY)
- action (VARCHAR2(50), NOT NULL)
- entity (VARCHAR2(100), NOT NULL)
- entity_id (NUMBER(19))
- user_id (VARCHAR2(255))
- details (CLOB)
- timestamp (TIMESTAMP, DEFAULT SYSTIMESTAMP)
**Constraints:**
- PRIMARY KEY on id

## Indexing Strategy
- Create primary keys (automatic indexes)
- Index on email (frequent lookups during login)
- Index on created_at (sorting and range queries)
- Index on active (filtering active/inactive users)
- Index on timestamp (audit log queries)
- Index on user_id (user activity tracking)
- Index on entity and entity_id (cross-entity queries)

## Integrity Constraints
- Primary key constraints for unique identification
- Not null constraints for required fields
- Unique constraints for unique identifiers (email)
- Foreign key to users table (optional, for data integrity)
- Check constraint for valid action types

## Data Model Relationships
- audit_logs -> users (many-to-one, user_id references users.id)

## Migration Strategy
**Tool**: Flyway versioned migrations
**Naming**: V{version:03d}_{description}.sql
**Execution**: Automatic on application startup
**Rollback**: Create V{version:03d}__undo_{description}.sql for rollbacks

## Stored Procedures/Functions
- PROCEDURE sp_create_user(p_email, p_name, ...)
- FUNCTION fn_get_user_by_email(p_email) RETURN user%ROWTYPE
- PROCEDURE sp_update_user(p_id, ...)
- PROCEDURE sp_delete_user(p_id)
- PROCEDURE sp_log_audit(p_action, p_entity, ...)
- FUNCTION fn_get_audit_logs(p_user_id, p_date_from)

## Performance Considerations
- Partitioning strategy for large tables (optional)
- Archive old audit logs to separate partition
- Analyze table statistics regularly with DBMS_STATS
- Monitor full table scans vs index usage

## Backup & Recovery Strategy
- Daily incremental backups
- Weekly full database backups
- Point-in-time recovery enabled
- Backup verification and restoration testing

## Indexes
- idx_auditlog_id
- idx_user_id
- idx_meeting_id
- idx_activityreport_id

## Acceptance Criteria
- [ ] Schema designed and documented
- [ ] Migration scripts created and tested
- [ ] All tables created with proper constraints
- [ ] Indexes designed and optimized
- [ ] Data integrity rules enforced
- [ ] Stored procedures/functions created
- [ ] Relationships defined
- [ ] Backup strategy implemented
- [ ] Performance tested and validated
- [ ] Documentation complete
- [ ] Code reviewed and approved

## Status
pending
