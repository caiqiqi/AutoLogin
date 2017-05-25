#coding=utf-8
import sys
import logging


logging.addLevelName(15, "INFO")
logger = logging.getLogger('AutoLogin')
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
LOGGER_HANDLER.setFormatter(FORMATTER)
logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.DEBUG)
