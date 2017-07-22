#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import logging
from logging.handlers import TimedRotatingFileHandler

from config import log_file


def get_logger(logfile,mark=None):
    if mark:
        logger = logging.getLogger(mark)
    else:
        logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fmt = '%(asctime)s - %(process)s - %(name)s - %(levelname)s: - %(lineno)d - %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.FileHandler(logfile)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger(log_file)


if __name__ == "__main__":
    logger.info('test')

