import os
from sql_operations import SQLMethods

object = SQLMethods()


object.step(
    "master",
    f"Drop user '{object.config_data.get('user')}';",

)

object.step(
    "master",
    "FLUSH PRIVILEGES;"
)

object.step(
    "master",
    f"Create user '{object.config_data.get('user')}' identified by '{object.config_data.get('user_password')}';",

)

object.step(
    "master",
    f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, EXECUTE, CREATE VIEW,"
    f"SHOW VIEW, EVENT, TRIGGER ON {object.config_data.get('db_name')}.* "
    f"TO '{object.config_data.get('user')}' WITH GRANT OPTION;"
)
