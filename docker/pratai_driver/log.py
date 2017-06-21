import os
import logging

from config import parse_config


class AppFilter(logging.Filter):
    def filter(self, record):
        record.function_id = os.environ.get("function_id", 'function_id')
        record.request_id = os.environ.get("request_id", 'request_id')
        return True


def prepare_log():
    logger = logging.getLogger('pratai-driver')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(parse_config("log")['path'])
    handler.setLevel(logging.DEBUG)

    # configure logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
