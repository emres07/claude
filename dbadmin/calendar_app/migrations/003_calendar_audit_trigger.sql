-- Comprehensive audit trigger for calendar
CREATE OR REPLACE TRIGGER trg_calendar_audit
BEFORE INSERT OR UPDATE OR DELETE ON calendar
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'CALENDAR',
            :NEW.id,
            'INSERT',
            'Record created with values: name=' || :NEW.name || '; description=' || :NEW.description || '; ',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'CALENDAR',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'CALENDAR',
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
END trg_calendar_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old calendar%ROWTYPE,
    p_new calendar%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    IF p_old.name != p_new.name THEN
        v_changes := v_changes || 'name: ' || p_old.name || ' -> ' || p_new.name || '; ';
    END IF;
    IF p_old.description != p_new.description THEN
        v_changes := v_changes || 'description: ' || p_old.description || ' -> ' || p_new.description || '; ';
    END IF;
    RETURN v_changes;
END CONCAT_CHANGES;
/