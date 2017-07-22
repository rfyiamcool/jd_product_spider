#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import json
import socket
import logging
import traceback

import redis
import requests
from user_agent import generate_user_agent

from utils import *
from config import *
from log import logger


logging.getLogger("requests").setLevel(logging.WARNING)


def fetch(url):
    user_agent = {'User-Agent': generate_user_agent()}
    res = None
    try:
        res = requests.get(url, headers=user_agent, timeout=spider_limiter['timeout'])
    except requests.exceptions.Timeout as e:
        logger.error("fetch faild !!! url:%s connect timeout", url)
    except requests.exceptions.TooManyRedirects as e:
        logger.error("fetch faild !!! url:%s redirect more than 3 times", url)
    except requests.exceptions.ConnectionError as e:
        logger.error("fetch faild !!! url:%s connect error", url)
    except socket.timeout as e:
        logger.error("fetch faild !!! url:%s recv timetout", url)
    except:
        logger.error("fetch faild !!! url:%s %s"%(url, traceback.format_exc()))

    if res and res.status_code == 200:
        logger.info("fetch success code: %s , url: %s"%(res.status_code, url))
    else:
        queue_push_url(url)
        logger.error("fetch faild !!!  url: %s"%(url))
    return res


def spider_worker():
    while 1:
        url = queue_pop_url()
        if not url:
            time.sleep(1)
            continue
        res = fetch(url)
        if res and res.status_code == 200:
            data = {'url': url, 'view': res.text}
            queue_push_result(data)
            time.sleep(spider_limiter['success_t'])
        else:
            time.sleep(spider_limiter['faild_t'])
            logger.warning('spdier error will sleep ...')


if __name__ == "__main__":
    spider_worker()

