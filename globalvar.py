"""
Fetch Config Details
"""
import configparser
from cryptography.fernet import Fernet

config = configparser.ConfigParser()
config.read("config.ini")


def load_key(file_name):
    """
    Load the previously generated key
    :param file_name: Name of secret key file name
    :return: Secret key
    """
    return open(file_name, "rb").read()


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    :param config_details: Config File details
    :param encrypted_message: Encrypted String
    :return: Decrypted String
    """
    key = load_key("secret/secret.key")
    fernet_object = Fernet(key)
    decrypted_message = fernet_object.decrypt(encrypted_message.encode())
    decrypted_message = fernet_object.decrypt(decrypted_message)
    decrypted_message = fernet_object.decrypt(decrypted_message)

    return decrypted_message.decode()


db_host = config['DEFAULT']["DB_HOST"]
db_name = config['DEFAULT']["DB_NAME"]
db_user = config['DEFAULT']["DB_USER_NAME"]
db_password = decrypt_message(config['DEFAULT']['DB_PASSWORD'])
path_query_file = 'queries.txt'
path_db_scripts = 'sqlscripts'