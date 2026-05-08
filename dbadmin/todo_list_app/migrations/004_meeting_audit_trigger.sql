-- Comprehensive audit trigger for meeting
CREATE OR REPLACE TRIGGER trg_meeting_audit
BEFORE INSERT OR UPDATE OR DELETE ON meeting
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETING',
            :NEW.id,
            'INSERT',
            'Record created with values: title=' || :NEW.title || '; description=' || :NEW.description || '; start_time=' || :NEW.start_time || '; end_time=' || :NEW.end_time || '; location=' || :NEW.location || '; ',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETING',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETING',
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
END trg_meeting_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old meeting%ROWTYPE,
    p_new meeting%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    IF p_old.title != p_new.title THEN
        v_changes := v_changes || 'title: ' || p_old.title || ' -> ' || p_new.title || '; ';
    END IF;
    IF p_old.description != p_new.description THEN
        v_changes := v_changes || 'description: ' || p_old.description || ' -> ' || p_new.description || '; ';
    END IF;
    IF p_old.start_time != p_new.start_time THEN
        v_changes := v_changes || 'start_time: ' || p_old.start_time || ' -> ' || p_new.start_time || '; ';
    END IF;
    IF p_old.end_time != p_new.end_time THEN
        v_changes := v_changes || 'end_time: ' || p_old.end_time || ' -> ' || p_new.end_time || '; ';
    END IF;
    IF p_old.location != p_new.location THEN
        v_changes := v_changes || 'location: ' || p_old.location || ' -> ' || p_new.location || '; ';
    END IF;
    RETURN v_changes;
END CONCAT_CHANGES;
/