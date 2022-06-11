Drop user '{db_name}';
FLUSH PRIVILEGES;
Create user '{user}' identified by '{user_password}';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, EXECUTE, CREATE VIEW,
SHOW VIEW, EVENT, TRIGGER ON {db_name}.* TO '{user}' WITH GRANT OPTION;