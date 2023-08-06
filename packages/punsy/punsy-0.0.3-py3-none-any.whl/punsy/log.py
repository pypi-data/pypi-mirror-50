'Define our logging format'

import logging
import os
import sys

LOG_BASE_NAME = 'punsy'

def init():
    'Create logger for lexer-ml'
    logger = logging.getLogger(LOG_BASE_NAME)
    logger.setLevel(logging.INFO)

    if os.getenv('ENV', 'dev') != 'test' and not logger.handlers:
        channel = logging.StreamHandler(sys.stdout)
        channel.setLevel(logging.INFO)
        channel.setFormatter(logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        ))
        logger.addHandler(channel)


def get_logger(module_name):
    'Return a new logger object for this library'
    init()
    return logging.getLogger('{}.{}'.format(LOG_BASE_NAME, module_name))

