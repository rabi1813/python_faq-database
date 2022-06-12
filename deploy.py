"""
Main Deployment file
"""
from log_services import log_initializer
from sql_operations import SQLMethods

logger = log_initializer()

sql_obj = SQLMethods()

if __name__ == "__main__":
    master_connection = sql_obj.mysql_master_connector()
    FLAG = sql_obj.step_execution(master_connection, operation_type="setup")
    if FLAG:
        connection = sql_obj.mysql_connector()
        sql_obj.step_execution(connection)
    sql_obj.update_version(master_connection)
    logger.info("Migration Complete")
