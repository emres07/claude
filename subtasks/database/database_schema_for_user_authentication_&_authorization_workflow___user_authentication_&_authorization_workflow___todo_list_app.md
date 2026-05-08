# Database Schema for User Authentication & Authorization Workflow - User Authentication & Authorization Workflow - TODO LIST APP

**Created by**: Database Agent
**Agent Role**: database_developer
**Date**: 2026-05-08 08:40:53
**Agent ID**: database_agent

## Description
Implement database schema for User Authentication & Authorization Workflow workflow.

Workflow Steps:
1. User navigates to login page
2. User enters credentials
3. System validates credentials against database
4. System generates JWT token if valid
5. User is granted access based on role
6. System restricts access to appropriate features

Data entities to persist: User, Role, Permission, Token

## Domain
Database

## Parent Task
user_authentication_&_authorization_workflow___todo_list_app

## Schema Design
**Database Type**: Oracle 21c/23c
### Naming Conventions
- Tables: lowercase with underscores (users, user_profiles)
- Columns: lowercase with underscores
- Constraints: prefix with constraint type (pk_*, uk_*, fk_*)
- Indexes: prefix with idx_ or idx_unique_
**Character Set**: AL32UTF8
### Entities
- users (core user data)
- user_profiles (extended profile)

## Tables to Create
- user
- role
- permission
- token

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

## Indexing Strategy
- Create primary keys (automatic indexes)
- Index on email (frequent lookups during login)
- Index on created_at (sorting and range queries)
- Index on active (filtering active/inactive users)

## Integrity Constraints
- Primary key constraints for unique identification
- Not null constraints for required fields
- Unique constraints for unique identifiers (email)

## Data Model Relationships
- No foreign key relationships (flat structure for this module)

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
- idx_user_id
- idx_role_id
- idx_permission_id
- idx_token_id

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
