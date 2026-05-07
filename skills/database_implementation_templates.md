# Database Implementation Templates - Jinja2 Format

## Table with Full Definition

<!-- table_full_definition -->
```sql
-- Create {{ table_name }} table
-- Part of {{ workflow_name | default('application') }}
CREATE TABLE {{ table_name }} (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    {% if columns -%}
    {% for col in columns -%}
    {{ col.name }} {{ col.oracle_type }}{% if col.constraints %} {{ col.constraints }}{% endif %},
    {% endfor %}
    {% else -%}
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    status VARCHAR2(50),
    {% endif -%}
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Create indexes for performance
{% if indexes -%}
{% for idx in indexes -%}
CREATE INDEX idx_{{ table_name }}_{{ idx.field }} ON {{ table_name }}({{ idx.field }});
{% endfor %}
{% else -%}
CREATE INDEX idx_{{ table_name }}_created_at ON {{ table_name }}(created_at);
CREATE INDEX idx_{{ table_name }}_updated_at ON {{ table_name }}(updated_at);
{% endif -%}

-- Create unique constraints if needed
{% if unique_constraints -%}
{% for constraint in unique_constraints -%}
ALTER TABLE {{ table_name }} ADD CONSTRAINT uk_{{ table_name }}_{{ constraint }} UNIQUE ({{ constraint }});
{% endfor %}
{% endif -%}

COMMIT;
```
<!-- /table_full_definition -->

## Complete CRUD Package

<!-- crud_package_complete -->
```sql
-- Complete CRUD Package for {{ table_name }}
CREATE OR REPLACE PACKAGE pkg_{{ table_name }}_ops AS
    -- Insert operation
    PROCEDURE insert_record(
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }},
        {% endfor %}
        {% endif -%}
        p_id OUT NUMBER
    );

    -- Select operation
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);

    -- Select all operation
    PROCEDURE get_all_records(p_cursor OUT SYS_REFCURSOR);

    -- Update operation
    PROCEDURE update_record(
        p_id IN NUMBER,
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }},
        {% endfor %}
        {% endif -%}
        p_success OUT NUMBER
    );

    -- Delete operation
    PROCEDURE delete_record(p_id IN NUMBER, p_success OUT NUMBER);

    {% if custom_procedures -%}
    {% for proc in custom_procedures -%}
    -- {{ proc.description }}
    PROCEDURE {{ proc.name }}(
        {% for param in proc.params -%}
        p_{{ param.name }} IN {{ param.type }},
        {% endfor -%}
        p_cursor OUT SYS_REFCURSOR
    );

    {% endfor %}
    {% endif -%}
END pkg_{{ table_name }}_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_{{ table_name }}_ops AS

    -- Insert record
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
            {{ col.name }}{{ "," if not loop.last }}
            {% endfor %}
            {% endif -%}
        ) VALUES (
            {% if columns -%}
            {% for col in columns -%}
            p_{{ col.name }}{{ "," if not loop.last }}
            {% endfor %}
            {% endif -%}
        )
        RETURNING id INTO p_id;
        
        COMMIT;
        log_action('INSERT', p_id);
    EXCEPTION
        WHEN OTHERS THEN
            log_action('INSERT_ERROR', NULL);
            ROLLBACK;
            RAISE;
    END insert_record;

    -- Get record by id
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM {{ table_name }}
            WHERE id = p_id;
    EXCEPTION
        WHEN OTHERS THEN
            log_action('GET_ERROR', p_id);
            RAISE;
    END get_record;

    -- Get all records
    PROCEDURE get_all_records(p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM {{ table_name }}
            ORDER BY created_at DESC;
    EXCEPTION
        WHEN OTHERS THEN
            log_action('GET_ALL_ERROR', NULL);
            RAISE;
    END get_all_records;

    -- Update record
    PROCEDURE update_record(
        p_id IN NUMBER,
        {% if columns -%}
        {% for col in columns -%}
        p_{{ col.name }} IN {{ col.oracle_type }},
        {% endfor %}
        {% endif -%}
        p_success OUT NUMBER
    ) IS
        v_rows_updated NUMBER;
    BEGIN
        UPDATE {{ table_name }} SET
            {% if columns -%}
            {% for col in columns -%}
            {{ col.name }} = p_{{ col.name }}{{ "," if not loop.last }}
            {% endfor %}
            {% endif -%}
            updated_at = SYSTIMESTAMP
        WHERE id = p_id;

        v_rows_updated := SQL%ROWCOUNT;
        
        IF v_rows_updated = 0 THEN
            p_success := 0;
            log_action('UPDATE_NOT_FOUND', p_id);
        ELSE
            p_success := 1;
            log_action('UPDATE', p_id);
            COMMIT;
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            p_success := -1;
            log_action('UPDATE_ERROR', p_id);
            ROLLBACK;
            RAISE;
    END update_record;

    -- Delete record
    PROCEDURE delete_record(p_id IN NUMBER, p_success OUT NUMBER) IS
        v_rows_deleted NUMBER;
    BEGIN
        DELETE FROM {{ table_name }} WHERE id = p_id;
        v_rows_deleted := SQL%ROWCOUNT;

        IF v_rows_deleted = 0 THEN
            p_success := 0;
            log_action('DELETE_NOT_FOUND', p_id);
        ELSE
            p_success := 1;
            log_action('DELETE', p_id);
            COMMIT;
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            p_success := -1;
            log_action('DELETE_ERROR', p_id);
            ROLLBACK;
            RAISE;
    END delete_record;

    {% if custom_procedures -%}
    {% for proc in custom_procedures -%}
    -- {{ proc.description }}
    PROCEDURE {{ proc.name }}(
        {% for param in proc.params -%}
        p_{{ param.name }} IN {{ param.type }},
        {% endfor -%}
        p_cursor OUT SYS_REFCURSOR
    ) IS
    BEGIN
        OPEN p_cursor FOR
            {{ proc.sql_query }};
    EXCEPTION
        WHEN OTHERS THEN
            log_action('{{ proc.name | upper }}_ERROR', NULL);
            RAISE;
    END {{ proc.name }};

    {% endfor %}
    {% endif -%}

    -- Helper procedure for logging
    PROCEDURE log_action(p_action VARCHAR2, p_record_id NUMBER) IS
    BEGIN
        INSERT INTO audit_log (entity_type, entity_id, operation, timestamp)
        VALUES ('{{ table_name | upper }}', p_record_id, p_action, SYSTIMESTAMP);
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            NULL; -- Silent fail on audit logging errors
    END log_action;

END pkg_{{ table_name }}_ops;
/
```
<!-- /crud_package_complete -->

## Audit Trigger with Column Tracking

<!-- audit_trigger_advanced -->
```sql
-- Comprehensive audit trigger for {{ table_name }}
CREATE OR REPLACE TRIGGER trg_{{ table_name }}_audit
BEFORE INSERT OR UPDATE OR DELETE ON {{ table_name }}
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            '{{ table_name | upper }}',
            :NEW.id,
            'INSERT',
            'Record created with values: {% for col in columns %}{{ col.name }}=' || :NEW.{{ col.name }} || '; {% endfor %}',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            '{{ table_name | upper }}',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            '{{ table_name | upper }}',
            :OLD.id,
            'DELETE',
            'Record deleted',
            USER,
            SYSTIMESTAMP
        );
    END IF;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- Continue even if audit fails
        NULL;
END trg_{{ table_name }}_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old {{ table_name }}%ROWTYPE,
    p_new {{ table_name }}%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    {% for col in columns -%}
    IF p_old.{{ col.name }} != p_new.{{ col.name }} THEN
        v_changes := v_changes || '{{ col.name }}: ' || p_old.{{ col.name }} || ' -> ' || p_new.{{ col.name }} || '; ';
    END IF;
    {% endfor -%}
    RETURN v_changes;
END CONCAT_CHANGES;
/
```
<!-- /audit_trigger_advanced -->
