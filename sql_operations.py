"""
SQL Operations
"""
import datetime
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT

from string_literals import SQLConstants, ErrorMessages
from common_utils import SecurityMethods, CommonUtilsMethods
from log_services import log_initializer

logger = log_initializer()
security_object = SecurityMethods()
common_object = CommonUtilsMethods()


class SQLUtilityMethods:
    """
    Methods for SQL Utility operations
    """
    __slots__ = ()

    def convert_datetime_to_string(self, records):
        """
        Convert all the datetime values to string
        :param records: Records fetched from DB/Request payload
        :return: Records with updated values
        """
        if isinstance(records, list):
            for item in records:
                item = self.convert_dict_datetime_to_string(item)
        elif isinstance(records, dict):
            records = self.convert_dict_datetime_to_string(records)
        return records

    @staticmethod
    def convert_dict_datetime_to_string(records):
        """
        Convert all the datetime values to string in a record of dictionary type
        :param records: Records fetched from DB/Request payload
        :return: Records with updated values
        """
        for key, value in records.items():
            if isinstance(records[key], datetime.datetime):
                records[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return records


class SQLMethods(SQLUtilityMethods, SQLConstants, ErrorMessages):
    """
    Methods for SQL operations
    """
    __slots__ = ()

    query_list = []
    config_data = security_object.decrypted_config()

    def mysql_master_connector(self):
        """
        Creates MySQL Connector
        :return: MySQL Connector object
        """
        if self.config_data.get("cursor_type") == "dict":
            cursor_class = pymysql.cursors.DictCursor
        else:
            cursor_class = pymysql.cursors.Cursor

        try:
            connection = pymysql.connect(host=self.config_data.get("host"),
                                         user=self.config_data.get("master_user"),
                                         password=self.config_data.get("db_password"),
                                         db='sys',
                                         charset='utf8mb4',
                                         cursorclass=cursor_class,
                                         client_flag=CLIENT.MULTI_STATEMENTS,
                                         autocommit=self.config_data.get("auto_commit_flag"))
            logger.info("Connected to db")
            return connection
        except pymysql.err.OperationalError as exp:
            logger.info(str(exp))
            raise pymysql.err.OperationalError

    def mysql_connector(self):
        """
        Creates MySQL Connector
        :return: MySQL Connector object
        """
        if self.config_data.get("cursor_type") == "dict":
            cursor_class = pymysql.cursors.DictCursor
        else:
            cursor_class = pymysql.cursors.Cursor

        try:
            connection = pymysql.connect(host=self.config_data.get("host"),
                                         user=self.config_data.get("user"),
                                         password=self.config_data.get("user_password"),
                                         db=self.config_data.get("db_name"),
                                         charset='utf8mb4',
                                         cursorclass=cursor_class,
                                         client_flag=CLIENT.MULTI_STATEMENTS,
                                         autocommit=self.config_data.get("auto_commit_flag"))
            logger.info("Connected to db")
            return connection
        except pymysql.err.OperationalError as exp:
            logger.info(str(exp))
            raise pymysql.err.OperationalError

    def execute_query(self, connection, query, payload=None):
        """
        Execute SQL query
        :param connection: MySQL Connector
        :param query: SQL Query
        :param payload: Query payload
        :return: Fetched details
        """
        try:
            with connection.cursor() as cursor:
                if payload:
                    query_string = query.replace("%(", "'%(").replace(")s", ")s'") % payload
                    logger.info('Querying SQL : %s', query_string)
                else:
                    logger.info('Querying SQL : %s', query)
                payload = payload if payload else {}
                cursor.execute(query, payload)
                sql_fetch = cursor.fetchall()
                if "grant" in query.lower():
                    return True, sql_fetch
                if "select" in query.lower() or "show" in query.lower() or "desc" in query.lower():
                    if not sql_fetch:
                        sql_fetch = self.generate_null_mapper(cursor)
                    result = self.convert_datetime_to_string(sql_fetch)
                    return True, result
                return True, sql_fetch
        except pymysql.err.OperationalError as exp:
            logger.error(str(exp))
            return False, str(exp)

        except pymysql.err.ProgrammingError as exp:
            logger.error(str(exp))
            return False, str(exp)

    @staticmethod
    def generate_null_mapper(cursor):
        """
        Generate Null Mapper
        :param cursor: MySQl Cursor
        :return Null Mapper
        """
        null_mapper = [{item[0]: (0 if item[1] in range(6) else "") for item in cursor.description}]
        return null_mapper

    def step_execution(self, connection, operation_type="common"):
        """
        Execute query steps
        :param connection: MySQl connection
        :param operation_type: setup/common
        :return True/False
        """
        query_list = common_object.step(operation_type=operation_type)
        count = 0
        for item in query_list:
            flag, result = self.execute_query(connection, item[1])
            if operation_type != "setup":
                update_check = self.query_update_check(connection, item[1])
                if update_check == 0:
                    self.migration_log_entry(connection, flag, item, result)
                else:
                    self.migration_log_entry(connection, True, item, "SKIPPED")
            count += 1
        if count == len(query_list):
            return True
        return False

    def migration_log_entry(self, connection, status_flag, query_tuple, error):
        """
        Function to insert log entries in log table
        :param connection: MySQl connection
        :param status_flag: True/False based on query execution
        :param query_tuple: Query details
        :param error: SKIPPED/Error message
        :return None
        """
        if error == "SKIPPED":
            version_payload = {
                "version_id": SQLConstants.VERSION_ID,
                "file_name": query_tuple[0],
                "query": query_tuple[1],
                "status": "SKIPPED",
                "error": ""
            }
            self.execute_query(connection, SQLConstants.VERSION_CONTROL, version_payload)
        elif status_flag:
            version_payload = {
                "version_id": SQLConstants.VERSION_ID,
                "file_name": query_tuple[0],
                "query": query_tuple[1],
                "status": "SUCCESS",
                "error": ""
            }
            self.execute_query(connection, SQLConstants.VERSION_CONTROL, version_payload)
        else:
            version_payload = {
                "version_id": SQLConstants.VERSION_ID,
                "file_name": query_tuple[0],
                "query": query_tuple[1],
                "status": "ERROR",
                "error": error
            }
            self.execute_query(connection, SQLConstants.VERSION_CONTROL, version_payload)

    def get_version_details(self, connection):
        """
        Get Version_number and Version_id
        :param connection: MySQl connection
        :return Version_number and Version_id
        """
        query = SQLConstants.GET_LATEST_VERSION.replace("db_name",
                                                        self.config_data.get("db_name"))
        flag, result = self.execute_query(connection, query)
        if flag:
            return result[0]
        logger.error(result)
        raise Exception(result)

    def get_version_row_count(self, connection):
        """
        Get RowCount of Version table
        :param connection: MySQl connection
        :return RowCount of Version table
        """
        query = SQLConstants.COUNT_LATEST_VERSION.replace("db_name",
                                                          self.config_data.get("db_name"))
        flag, result = self.execute_query(connection, query)
        if flag:
            return result[0]["count"]
        logger.error(result)
        raise Exception(result)

    def update_version(self, connection):
        """
        Insert/Update Version ID in Version table
        :param connection: MySQl connection
        :return None
        """
        logger.info("Updating Migration Version")
        count = self.get_version_row_count(connection)
        if count == 0:
            query = SQLConstants.INSERT_LATEST_VERSION.replace("db_name",
                                                               self.config_data.get("db_name"))
            flag, result = self.execute_query(connection, query)
            if flag is False:
                logger.error(result)
                raise Exception(result)
        else:
            version_number = self.get_version_details(connection)["version_number"]
            version_number += 1
            payload = {
                "version_number": version_number
            }
            query = SQLConstants.UPDATE_LATEST_VERSION.replace("db_name",
                                                               self.config_data.get("db_name"))
            flag, result = self.execute_query(connection, query, payload)
            if flag is False:
                logger.error(result)
                raise Exception(result)

    def query_update_check(self, connection, query):
        """
        Function to check if there is any change in SQL files.
        :param connection: MySQl connection
        :param query: Query that needs to be validated.
        :return Match Count
        """
        version_id = self.get_version_details(connection)["version_id"]
        payload = {
            "version_id": version_id,
            "query": query
        }
        flag, result = self.execute_query(connection, SQLConstants.CHECK_QUERY_UPDATES, payload)
        if flag:
            return result[0]["count"]
        logger.error(result)
        raise Exception(result)
