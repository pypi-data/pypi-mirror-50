"""Personal Formatting on Loguru"""

__version__ = "0.0.1"
__author__ = "Aditya Kelvianto Sidharta"

import datetime
import logging
import os
import sys

from loguru import logger as loguru_logger


def _get_datetime():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


class Logger:
    """
    Setting up logger for the project. The log will be logged within the file as well
    logger.setup_logger(script_name) must be called first before using the logger.
    """

    def __init__(self):
        self.name = None
        self.datetime = None
        self.level = None
        self.format = None
        self.logger = None
        self.is_setup = False

    def setup_logger(self, name, logger_file, level=logging.INFO):
        self.name = name
        self.datetime = _get_datetime()
        self.level = level
        self.format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> |" \
                      " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        self.logger = loguru_logger
        self.logger.add(sys.stderr, format=self.format, level=self.level)
        self.logger.add(
            os.path.join(logger_file, "{}_{}.log".format(self.name, self.datetime)),
            format=self.format,
            level=self.level,
        )
        self.is_setup = True

    def info(self, msg):
        assert self.is_setup, "Please Setup the Logger First"
        return self.logger.info(msg)

    def debug(self, msg):
        assert self.is_setup, "Please Setup the Logger First"
        return self.logger.debug(msg)

    def error(self, msg):
        assert self.is_setup, "Please Setup the Logger First"
        return self.logger.error(msg)

    def warning(self, msg):
        assert self.is_setup, "Please Setup the Logger First"
        return self.logger.warning(msg)


logger = Logger()
