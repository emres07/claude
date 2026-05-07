-- Complete CRUD Package for user
CREATE OR REPLACE PACKAGE pkg_user_ops AS
    -- Insert operation
    PROCEDURE insert_record(
        p_email IN VARCHAR2(255),
        p_name IN VARCHAR2(255),
        p_password_hash IN VARCHAR2(255),
        
        p_id OUT NUMBER
    );

    -- Select operation
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);

    -- Select all operation
    PROCEDURE get_all_records(p_cursor OUT SYS_REFCURSOR);

    -- Update operation
    PROCEDURE update_record(
        p_id IN NUMBER,
        p_email IN VARCHAR2(255),
        p_name IN VARCHAR2(255),
        p_password_hash IN VARCHAR2(255),
        
        p_success OUT NUMBER
    );

    -- Delete operation
    PROCEDURE delete_record(p_id IN NUMBER, p_success OUT NUMBER);

    END pkg_user_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_user_ops AS

    -- Insert record
    PROCEDURE insert_record(
        p_email IN VARCHAR2(255),
        p_name IN VARCHAR2(255),
        p_password_hash IN VARCHAR2(255),
        
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO user (
            email,
            name,
            password_hash
            
            ) VALUES (
            p_email,
            p_name,
            p_password_hash
            
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
            SELECT * FROM user
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
            SELECT * FROM user
            ORDER BY created_at DESC;
    EXCEPTION
        WHEN OTHERS THEN
            log_action('GET_ALL_ERROR', NULL);
            RAISE;
    END get_all_records;

    -- Update record
    PROCEDURE update_record(
        p_id IN NUMBER,
        p_email IN VARCHAR2(255),
        p_name IN VARCHAR2(255),
        p_password_hash IN VARCHAR2(255),
        
        p_success OUT NUMBER
    ) IS
        v_rows_updated NUMBER;
    BEGIN
        UPDATE user SET
            email = p_email,
            name = p_name,
            password_hash = p_password_hash
            
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
        DELETE FROM user WHERE id = p_id;
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

    -- Helper procedure for logging
    PROCEDURE log_action(p_action VARCHAR2, p_record_id NUMBER) IS
    BEGIN
        INSERT INTO audit_log (entity_type, entity_id, operation, timestamp)
        VALUES ('USER', p_record_id, p_action, SYSTIMESTAMP);
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            NULL; -- Silent fail on audit logging errors
    END log_action;

END pkg_user_ops;
/