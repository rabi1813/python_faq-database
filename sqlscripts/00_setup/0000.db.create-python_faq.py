from sql_operations import SQLMethods
import os
object = SQLMethods()


object.step(
    "master",
    f"DROP DATABASE IF NOT EXISTS {object.config_data.get('db_name')}"
)

object.step(
    "master",
    f"CREATE DATABASE IF NOT EXISTS {object.config_data.get('db_name')}"
)

print(__file__)
print(os.path.basename(__file__))
print(object.config_data.get('db_name'))
