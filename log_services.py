"""
Code to initialize logger
"""
import logging


def log_initializer():
    """
    Log Initializer
    :return: Logger object
    """
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    return logger
