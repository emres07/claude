-- Audit Stored Procedures
-- ============================================================
-- CRUD Stored Procedures for AUDIT
-- ============================================================

-- CREATE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_audit_insert (
  p_name IN VARCHAR2,
  p_description IN VARCHAR2,
  p_status IN VARCHAR2 DEFAULT 'ACTIVE',
  p_id OUT NUMBER
)
IS
BEGIN
  INSERT INTO audit (id, name, description, status, created_at, updated_at)
  VALUES (audit_seq.NEXTVAL, p_name, p_description, p_status, SYSTIMESTAMP, SYSTIMESTAMP)
  RETURNING id INTO p_id;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('Record inserted successfully with ID: ' || p_id);
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error inserting record: ' || SQLERRM);
    RAISE;
END sp_audit_insert;
/

-- READ PROCEDURE (Single Record)
CREATE OR REPLACE PROCEDURE sp_audit_get (
  p_id IN NUMBER,
  p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
  OPEN p_cursor FOR
    SELECT id, name, description, status, created_at, updated_at
    FROM audit
    WHERE id = p_id;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Record not found with ID: ' || p_id);
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error reading record: ' || SQLERRM);
    RAISE;
END sp_audit_get;
/

-- READ PROCEDURE (All Records)
CREATE OR REPLACE PROCEDURE sp_audit_get_all (
  p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
  OPEN p_cursor FOR
    SELECT id, name, description, status, created_at, updated_at
    FROM audit
    ORDER BY created_at DESC;
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error retrieving records: ' || SQLERRM);
    RAISE;
END sp_audit_get_all;
/

-- UPDATE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_audit_update (
  p_id IN NUMBER,
  p_name IN VARCHAR2 DEFAULT NULL,
  p_description IN VARCHAR2 DEFAULT NULL,
  p_status IN VARCHAR2 DEFAULT NULL
)
IS
  v_rows_updated NUMBER;
BEGIN
  UPDATE audit
  SET
    name = COALESCE(p_name, name),
    description = COALESCE(p_description, description),
    status = COALESCE(p_status, status),
    updated_at = SYSTIMESTAMP
  WHERE id = p_id;

  v_rows_updated := SQL%ROWCOUNT;

  IF v_rows_updated > 0 THEN
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Record updated successfully');
  ELSE
    DBMS_OUTPUT.PUT_LINE('No records found to update with ID: ' || p_id);
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error updating record: ' || SQLERRM);
    RAISE;
END sp_audit_update;
/

-- DELETE PROCEDURE
CREATE OR REPLACE PROCEDURE sp_audit_delete (
  p_id IN NUMBER
)
IS
  v_rows_deleted NUMBER;
BEGIN
  DELETE FROM audit
  WHERE id = p_id;

  v_rows_deleted := SQL%ROWCOUNT;

  IF v_rows_deleted > 0 THEN
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Record deleted successfully');
  ELSE
    DBMS_OUTPUT.PUT_LINE('No records found to delete with ID: ' || p_id);
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    DBMS_OUTPUT.PUT_LINE('Error deleting record: ' || SQLERRM);
    RAISE;
END sp_audit_delete;
/

-- ============================================================
-- Package for AUDIT Operations
-- ============================================================

CREATE OR REPLACE PACKAGE pkg_audit_ops IS
  PROCEDURE insert_record(
    p_name IN VARCHAR2,
    p_description IN VARCHAR2,
    p_id OUT NUMBER
  );

  PROCEDURE get_record(
    p_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
  );

  PROCEDURE get_all_records(
    p_cursor OUT SYS_REFCURSOR
  );

  PROCEDURE update_record(
    p_id IN NUMBER,
    p_name IN VARCHAR2,
    p_description IN VARCHAR2
  );

  PROCEDURE delete_record(
    p_id IN NUMBER
  );
END pkg_audit_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_audit_ops IS

  PROCEDURE insert_record(
    p_name IN VARCHAR2,
    p_description IN VARCHAR2,
    p_id OUT NUMBER
  ) IS
  BEGIN
    sp_audit_insert(p_name, p_description, 'ACTIVE', p_id);
  END insert_record;

  PROCEDURE get_record(
    p_id IN NUMBER,
    p_cursor OUT SYS_REFCURSOR
  ) IS
  BEGIN
    sp_audit_get(p_id, p_cursor);
  END get_record;

  PROCEDURE get_all_records(
    p_cursor OUT SYS_REFCURSOR
  ) IS
  BEGIN
    sp_audit_get_all(p_cursor);
  END get_all_records;

  PROCEDURE update_record(
    p_id IN NUMBER,
    p_name IN VARCHAR2,
    p_description IN VARCHAR2
  ) IS
  BEGIN
    sp_audit_update(p_id, p_name, p_description, NULL);
  END update_record;

  PROCEDURE delete_record(
    p_id IN NUMBER
  ) IS
  BEGIN
    sp_audit_delete(p_id);
  END delete_record;

END pkg_audit_ops;
/

-- ============================================================
-- End of CRUD Procedures
-- ============================================================

