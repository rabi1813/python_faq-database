"""
Common Utilities
"""
import json

import yaml
import os
from cryptography.fernet import Fernet

from log_services import log_initializer
from string_literals import Constants, QueryFolderStructure, ErrorMessages, SQLConstants

logger = log_initializer()


class CommonUtilsMethods:
    """
    Class for Common Utility Methods
    """
    @staticmethod
    def open_file(file_name):
        with open(file_name, 'r') as file_data:
            data = file_data.read().replace("\n", "")
        return data

    @staticmethod
    def semi_colon_validator(query_list):
        error_file = []
        for query in query_list:
            if ";" not in query[1]:
                error_file.append(query[0])
            elif not query[1].endswith(";"):
                error_file.append(query[0])
        if len(error_file) == 1:
            error_message = ErrorMessages.SEMI_COLON_MISSING.format(', '.join(error_file))
            logger.error(error_message)
            raise Exception(error_message)
        elif len(error_file) > 1:
            error_message = ErrorMessages.SEMI_COLON_MISSING.format(', '.join(error_file))
            logger.error(error_message)
            raise Exception(error_message)
        else:
            return query_list

    @staticmethod
    def get_query_file_list(folder):
        file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".sql")]
        return file_list

    @staticmethod
    def query_splitter(query_list):
        final_list = []
        for item in query_list:
            queries = [(item[0], query + ";") for query in item[1].split(";") if query]
            final_list.extend(queries)
        return final_list

    def step(self, operation_type="common"):
        """
        Generate steps for query execution
        :param operation_type: Setup/Common
        :return: List of query file name and query
        """
        if operation_type == "setup":
            file_list = self.get_query_file_list(QueryFolderStructure.SETUP_FOLDER)
            query_list = [(os.path.basename(file), self.open_file(file).format(**config_data)) for file in file_list]
            query_list = self.semi_colon_validator(query_list)
            query_list = self.query_splitter(query_list)
            logger.info(f"Query in queue: {json.dumps(query_list, indent=4)}")
        else:
            file_list = self.get_query_file_list(QueryFolderStructure.TABLE_FOLDER)
            file_list.extend(self.get_query_file_list(QueryFolderStructure.CUSTOM_FOLDER))
            query_list = [(os.path.basename(file), self.open_file(file).format(**config_data)) for file in file_list]
            query_list = self.semi_colon_validator(query_list)
            query_list = self.query_splitter(query_list)
            logger.info(f"Query in queue: {json.dumps(query_list, indent=4)}")
        return query_list


class SecurityMethods:
    """
    Security related methods
    """
    __slots__ = ()

    @staticmethod
    def read_config_file():
        """
        Read Config File
        :return:Config Data
        """
        with open(Constants.CONFIG_FILE, 'r') as config:
            config_details = yaml.load(config, Loader=yaml.FullLoader)
        return config_details

    @staticmethod
    def generate_key_file(file_name):
        """
        Generates a key and save it into a file
        :param file_name: Name of secret key file name
        :return: None
        """
        dir_name = os.path.dirname(file_name)
        if dir_name != "":
            os.makedirs(dir_name, exist_ok=True)
        key = Fernet.generate_key()
        file_name = os.path.join(Constants.FILE_DIR, file_name)
        with open(file_name, "wb") as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(file_name):
        """
        Load the previously generated key
        :param file_name: Name of secret key file name
        :return: Secret key
        """
        file_name = os.path.join(Constants.FILE_DIR, file_name)
        return open(file_name, "rb").read()

    def encrypt_message(self, config_details, normal_string):
        """
        Encrypts a message
        :param config_details: Config File details
        :param normal_string: Normal String
        :return: Encrypted String
        """
        key = self.load_key(config_details.get("secret"))
        encoded_message = normal_string.encode()
        fernet_object = Fernet(key)
        encrypted_message = fernet_object.encrypt(encoded_message)
        encrypted_message = fernet_object.encrypt(encrypted_message)
        encrypted_message = fernet_object.encrypt(encrypted_message)

        return encrypted_message.decode()

    def decrypt_message(self, config_details, encrypted_message):
        """
        Decrypts an encrypted message
        :param config_details: Config File details
        :param encrypted_message: Encrypted String
        :return: Decrypted String
        """
        key = self.load_key(config_details.get("secret"))
        fernet_object = Fernet(key)
        decrypted_message = fernet_object.decrypt(encrypted_message.encode())
        decrypted_message = fernet_object.decrypt(decrypted_message)
        decrypted_message = fernet_object.decrypt(decrypted_message)

        return decrypted_message.decode()

    def decrypted_config(self):
        """
        Decrypt config data
        :return:Decrypted config data
        """
        config_details = self.read_config_file()
        config_details["db_password"] = self.decrypt_message(config_details, config_details["db_password"])
        config_details["user_password"] = self.decrypt_message(config_details, config_details["user_password"])
        return config_details


security_object = SecurityMethods()
config_data = security_object.decrypted_config()
