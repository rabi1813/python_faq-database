from log_services import log_initializer
from sql_operations import SQLMethods

logger = log_initializer()

sql_obj = SQLMethods()

master_connection = sql_obj.mysql_master_connector()
flag = sql_obj.step_execution(master_connection, operation_type="setup")
if flag:
    connection = sql_obj.mysql_connector()
    sql_obj.step_execution(connection)
    sql_obj.version_operations(connection, query_type="update")