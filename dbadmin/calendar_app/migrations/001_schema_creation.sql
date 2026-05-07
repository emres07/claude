-- Create schema user for calendar_app
CREATE USER calendar_app IDENTIFIED BY welcome123;
GRANT CONNECT, RESOURCE, CREATE VIEW TO calendar_app;
ALTER USER calendar_app QUOTA UNLIMITED ON USERS;

COMMIT;