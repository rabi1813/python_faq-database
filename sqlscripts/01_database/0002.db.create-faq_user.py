from yoyo import step
import globalvar

step(
    f"Create user 'faq_user' identified by '{globalvar.user_password}';",
    "Drop user 'faq_user';"
)

step(
    "FLUSH PRIVILEGES;",
    ""
)
step(
    f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, EXECUTE, CREATE VIEW,"
    f"SHOW VIEW, EVENT, TRIGGER ON {globalvar.db_name}.* TO 'faq_user' WITH GRANT OPTION;",
    ""
)
