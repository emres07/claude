-- Comprehensive audit trigger for meetingnotes
CREATE OR REPLACE TRIGGER trg_meetingnotes_audit
BEFORE INSERT OR UPDATE OR DELETE ON meetingnotes
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETINGNOTES',
            :NEW.id,
            'INSERT',
            'Record created with values: content=' || :NEW.content || '; summary=' || :NEW.summary || '; ',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETINGNOTES',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'MEETINGNOTES',
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
END trg_meetingnotes_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old meetingnotes%ROWTYPE,
    p_new meetingnotes%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    IF p_old.content != p_new.content THEN
        v_changes := v_changes || 'content: ' || p_old.content || ' -> ' || p_new.content || '; ';
    END IF;
    IF p_old.summary != p_new.summary THEN
        v_changes := v_changes || 'summary: ' || p_old.summary || ' -> ' || p_new.summary || '; ';
    END IF;
    RETURN v_changes;
END CONCAT_CHANGES;
/