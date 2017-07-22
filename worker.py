#!/usr/bin/env python
# -*- coding:utf-8 -*-

from log import logger

from spider import spider_worker
from extractor import extractor_worker


#你的业务逻辑
def spider_handler():
    spider_worker()
    logger.info('this is spider_worker')


def extractor_handler():
    extractor_worker()
    logger.info('this is extractor_worker')

ALLOW_METHOD = [{"func":spider_handler, "counte":2}, {"func":extractor_handler, "count":1}]

