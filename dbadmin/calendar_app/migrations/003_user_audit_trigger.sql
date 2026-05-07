-- Comprehensive audit trigger for user
CREATE OR REPLACE TRIGGER trg_user_audit
BEFORE INSERT OR UPDATE OR DELETE ON user
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'USER',
            :NEW.id,
            'INSERT',
            'Record created with values: email=' || :NEW.email || '; name=' || :NEW.name || '; password_hash=' || :NEW.password_hash || '; ',
            USER,
            SYSTIMESTAMP
        );

    ELSIF UPDATING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'USER',
            :NEW.id,
            'UPDATE',
            CONCAT_CHANGES(:OLD, :NEW),
            USER,
            SYSTIMESTAMP
        );

    ELSIF DELETING THEN
        INSERT INTO audit_log (entity_type, entity_id, operation, changes, user_id, timestamp)
        VALUES (
            'USER',
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
END trg_user_audit;
/

-- Helper function to track column changes
CREATE OR REPLACE FUNCTION CONCAT_CHANGES(
    p_old user%ROWTYPE,
    p_new user%ROWTYPE
) RETURN CLOB IS
    v_changes CLOB := '';
BEGIN
    IF p_old.email != p_new.email THEN
        v_changes := v_changes || 'email: ' || p_old.email || ' -> ' || p_new.email || '; ';
    END IF;
    IF p_old.name != p_new.name THEN
        v_changes := v_changes || 'name: ' || p_old.name || ' -> ' || p_new.name || '; ';
    END IF;
    IF p_old.password_hash != p_new.password_hash THEN
        v_changes := v_changes || 'password_hash: ' || p_old.password_hash || ' -> ' || p_new.password_hash || '; ';
    END IF;
    RETURN v_changes;
END CONCAT_CHANGES;
/