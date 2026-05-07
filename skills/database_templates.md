# Database Code Templates - Jinja2 Format

## Oracle Schema Creation Template

<!-- oracle_schema -->
```sql
-- Create schema user for {{ schema_name }}
CREATE USER {{ schema_name }} IDENTIFIED BY {{ password | default('welcome123') }};
GRANT CONNECT, RESOURCE, CREATE VIEW TO {{ schema_name }};
ALTER USER {{ schema_name }} QUOTA UNLIMITED ON USERS;

COMMIT;
```
<!-- /oracle_schema -->

## Dynamic Table Template

<!-- dynamic_table -->
```sql
-- Create {{ table_name }} table
CREATE TABLE {{ table_name }} (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    {% if columns -%}
    {% for col in columns -%}
    {{ col.name }} {{ col.type }}{% if col.nullable %} {% else %} NOT NULL{% endif %},
    {% endfor %}
    {% else -%}
    name VARCHAR2(255),
    description CLOB,
    {% endif -%}
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

{% if indexes -%}
{% for idx in indexes -%}
CREATE INDEX idx_{{ table_name }}_{{ idx }} ON {{ table_name }}({{ idx }});
{% endfor %}
{% else -%}
CREATE INDEX idx_{{ table_name }}_created ON {{ table_name }}(created_at);
{% endif -%}
```
<!-- /dynamic_table -->

## Dynamic CRUD Procedures Template

<!-- dynamic_crud_procedures -->
```sql
-- CRUD Procedures for {{ table_name }}

CREATE OR REPLACE PACKAGE pkg_{{ table_name }}_ops AS
    PROCEDURE insert_record(
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }},
        {% endfor %}
        {% endif -%}
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }}{% if not loop.last %},{% endif %}
        {% endfor %}
        {% endif -%}
    );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_{{ table_name }}_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_{{ table_name }}_ops AS
    PROCEDURE insert_record(
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }},
        {% endfor %}
        {% endif -%}
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO {{ table_name }} (
            {% if columns -%}
            {% for col in columns -%}
            {{ col.name }}{% if not loop.last %}, {% endif %}
            {% endfor %}
            {% endif -%}
        ) VALUES (
            {% if columns -%}
            {% for col in columns -%}
            p_{{ col.name }}{% if not loop.last %}, {% endif %}
            {% endfor %}
            {% endif -%}
        );
        SELECT id INTO p_id FROM {{ table_name }} WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM {{ table_name }} WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }}{% if not loop.last %},{% endif %}
        {% endfor %}
        {% endif -%}
    ) IS
    BEGIN
        UPDATE {{ table_name }} SET
            {% if columns -%}
            {% for col in columns -%}
            {{ col.name }} = p_{{ col.name }}{% if not loop.last %},{% endif %}
            {% endfor %}
            {% endif -%}
        WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM {{ table_name }} WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_{{ table_name }}_ops;
/
```
<!-- /dynamic_crud_procedures -->

## Dynamic Trigger Template

<!-- dynamic_trigger -->
```sql
-- Audit trigger for {{ table_name }} changes
CREATE OR REPLACE TRIGGER trg_{{ table_name }}_audit
AFTER INSERT OR UPDATE OR DELETE ON {{ table_name }}
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id, timestamp)
        VALUES ('{{ table_name | upper }}', :NEW.id, 'INSERT', SYS_CONTEXT('USERENV', 'SESSION_USER'), SYSTIMESTAMP);
    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id, timestamp)
        VALUES ('{{ table_name | upper }}', :NEW.id, 'UPDATE', SYS_CONTEXT('USERENV', 'SESSION_USER'), SYSTIMESTAMP);
    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, user_id, timestamp)
        VALUES ('{{ table_name | upper }}', :OLD.id, 'DELETE', SYS_CONTEXT('USERENV', 'SESSION_USER'), SYSTIMESTAMP);
    END IF;
    COMMIT;
END trg_{{ table_name }}_audit;
/
```
<!-- /dynamic_trigger -->

## Audit Log Table Template

<!-- audit_table -->
```sql
-- Create audit_log table for compliance and tracking
CREATE TABLE audit_log (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    entity_type VARCHAR2(255) NOT NULL,
    entity_id NUMBER(19),
    operation VARCHAR2(50) NOT NULL,
    changes CLOB,
    user_id VARCHAR2(255),
    timestamp TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_user ON audit_log(user_id);

COMMIT;
```
<!-- /audit_table -->

## Migration Status Template

<!-- migration_status -->
```json
{
  "current_version": "{{ current_version | default('001') }}",
  "database": "oracle",
  "created_at": "{{ created_at | default('2026-05-08') }}",
  "migrations": [
    {% for migration in migrations -%}
    {
      "version": "{{ migration.version }}",
      "name": "{{ migration.name }}",
      "description": "{{ migration.description }}",
      "status": "{{ migration.status | default('pending') }}",
      "file": "{{ migration.file }}",
      "executed": {{ migration.executed | lower | default('false') }}
    }{{ "," if not loop.last }}
    {% endfor %}
  ],
  "notes": "Scripts are versioned but NOT auto-executed. Manual execution required."
}
```
<!-- /migration_status -->
