-- Meeting Management CRUD Procedures
-- CRUD Procedures for meeting

CREATE OR REPLACE PACKAGE pkg_meeting_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_meeting_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_meeting_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO meeting (
            ) VALUES (
            );
        SELECT id INTO p_id FROM meeting WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM meeting WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        ) IS
    BEGIN
        UPDATE meeting SET
            WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM meeting WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_meeting_ops;
/

-- CRUD Procedures for calendar

CREATE OR REPLACE PACKAGE pkg_calendar_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_calendar_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_calendar_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO calendar (
            ) VALUES (
            );
        SELECT id INTO p_id FROM calendar WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM calendar WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        ) IS
    BEGIN
        UPDATE calendar SET
            WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM calendar WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_calendar_ops;
/

-- CRUD Procedures for timeslot

CREATE OR REPLACE PACKAGE pkg_timeslot_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_timeslot_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_timeslot_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO timeslot (
            ) VALUES (
            );
        SELECT id INTO p_id FROM timeslot WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM timeslot WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        ) IS
    BEGIN
        UPDATE timeslot SET
            WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM timeslot WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_timeslot_ops;
/

-- CRUD Procedures for attendee

CREATE OR REPLACE PACKAGE pkg_attendee_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    );
    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR);
    PROCEDURE update_record(
        p_id IN NUMBER,
        );
    PROCEDURE delete_record(p_id IN NUMBER);
END pkg_attendee_ops;
/

CREATE OR REPLACE PACKAGE BODY pkg_attendee_ops AS
    PROCEDURE insert_record(
        p_id OUT NUMBER
    ) IS
    BEGIN
        INSERT INTO attendee (
            ) VALUES (
            );
        SELECT id INTO p_id FROM attendee WHERE ROWNUM = 1;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END insert_record;

    PROCEDURE get_record(p_id IN NUMBER, p_cursor OUT SYS_REFCURSOR) IS
    BEGIN
        OPEN p_cursor FOR
            SELECT * FROM attendee WHERE id = p_id;
    END get_record;

    PROCEDURE update_record(
        p_id IN NUMBER,
        ) IS
    BEGIN
        UPDATE attendee SET
            WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_record;

    PROCEDURE delete_record(p_id IN NUMBER) IS
    BEGIN
        DELETE FROM attendee WHERE id = p_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END delete_record;
END pkg_attendee_ops;
/

