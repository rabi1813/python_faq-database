"""
File to store all constant values
"""
import os
from uuid import uuid4

class Constants:
    """
    General Constants
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    DESC_QUERY = "DESC {table_name};"

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(FILE_DIR, "config", "config.yaml")


class SQLConstants:
    """
    SQL related constants
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """
    VERSION_ID = uuid4()
    COUNT_LATEST_VERSION = "SELECT count(*) as count FROM db_name._latest_version;"
    GET_LATEST_VERSION = "SELECT version_number, version_id FROM db_name._latest_version;"
    INSERT_LATEST_VERSION = f"INSERT INTO db_name._latest_version (version_id) " \
                            f"VALUES ('{VERSION_ID}');"
    UPDATE_LATEST_VERSION = f"UPDATE db_name._latest_version set " \
                            f"version_number = %(version_number)s, version_id = '{VERSION_ID}'"
    CHECK_QUERY_UPDATES = "SELECT count(*) as count from _migration_version_log " \
                          "where version_id = %(version_id)s " \
                          "and status in ('SUCCESS', 'SKIPPED') and query = %(query)s;"
    VERSION_CONTROL = "INSERT INTO _migration_version_log (version_id, file_name, query, status, " \
                      "error, execution_datetime, executed_by) VALUES (%(version_id)s, " \
                      "%(file_name)s, %(query)s, %(status)s, %(error)s, now(), 'System');"



class ErrorMessages:
    """
    Error Messages
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """
    GENERAL_ERROR_MESSAGE = "Error Occurred"
    DB_CONNECTION_FAIL = "Failed to connect DB"
    SEMI_COLON_MISSING = "';' is missing in the SQL files: {0}"
    ERROR_MESSAGE_TEMPLATE = {}

class QueryFolderStructure:
    """
    Constant class to store folder path
    """
    __slots__ = ()

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def bypass_pylint():
        """
        Test Function
        :return: None
        """

    QUERY_FOLDER = "sql_queries"
    SETUP_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "00_setup")
    TABLE_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "01_table")
    INDEX_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "02_index")
    VIEW_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "03_view")
    FUNCTION_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "04_function")
    STORED_PROCEDURE_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "05_storedprocedure")
    REFERENCE_DATA_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "06_referencedata")
    CUSTOM_FOLDER = os.path.join(Constants.FILE_DIR, QUERY_FOLDER, "07_custom")
