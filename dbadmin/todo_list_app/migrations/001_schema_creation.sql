-- Create schema user for todo_list_app
CREATE USER todo_list_app IDENTIFIED BY welcome123;
GRANT CONNECT, RESOURCE, CREATE VIEW TO todo_list_app;
ALTER USER todo_list_app QUOTA UNLIMITED ON USERS;

COMMIT;