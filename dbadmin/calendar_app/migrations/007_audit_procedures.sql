-- Audit Stored Procedures
-- CRUD Procedures for audit

CREATE OR REPLACE PACKAGE pkg_audit_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_audit_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_audit_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO audit (
            ) VALUES (
            );
        SELECT id INTO p_id FROM audit WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM audit WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        ) IS
    BEGIN
        UPDATE audit SET
            WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM audit WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_audit_ops;
/
