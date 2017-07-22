#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from config import *


def queue_push_url(url):
    return rd.sadd(JD_URLS_TASK, url)


def queue_pop_url():
    url = rd.spop(JD_URLS_TASK)
    return url


def queue_push_result(data):
    return rd.rpush(JD_URLS_RESULT, json.dumps(data))


def queue_pop_result():
    url, view = None, None
    if DEBUG:
        res = rd.lrange(JD_URLS_RESULT,0,1)[0]  # for test
    else:
        res = rd.lpop(JD_URLS_RESULT)
    if res:
        data = json.loads(res)
        url, view = data['url'], data['view']
    return url, view


def perfect_href(url):
    if url.startswith('http:'):
        return url
    else:
        return "http:" + url

