-- Comprehensive audit trigger for auditlog
CREATE OR REPLACE TRIGGER trg_auditlog_audit
BEFORE INSERT OR UPDATE OR DELETE ON auditlog
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'AUDITLOG',
            :NEW.id,
            'INSERT',
            'Record created with values: entity_type=' || :NEW.entity_type || '; entity_id=' || :NEW.entity_id || '; operation=' || :NEW.operation || '; changes=' || :NEW.changes || '; user_id=' || :NEW.user_id || '; ',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'AUDITLOG',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'AUDITLOG',
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
END trg_auditlog_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old auditlog%ROWTYPE,
    p_new auditlog%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    IF p_old.entity_type != p_new.entity_type THEN
        v_changes := v_changes || 'entity_type: ' || p_old.entity_type || ' -> ' || p_new.entity_type || '; ';
    END IF;
    IF p_old.entity_id != p_new.entity_id THEN
        v_changes := v_changes || 'entity_id: ' || p_old.entity_id || ' -> ' || p_new.entity_id || '; ';
    END IF;
    IF p_old.operation != p_new.operation THEN
        v_changes := v_changes || 'operation: ' || p_old.operation || ' -> ' || p_new.operation || '; ';
    END IF;
    IF p_old.changes != p_new.changes THEN
        v_changes := v_changes || 'changes: ' || p_old.changes || ' -> ' || p_new.changes || '; ';
    END IF;
    IF p_old.user_id != p_new.user_id THEN
        v_changes := v_changes || 'user_id: ' || p_old.user_id || ' -> ' || p_new.user_id || '; ';
    END IF;
    RETURN v_changes;
END CONCAT_CHANGES;
/