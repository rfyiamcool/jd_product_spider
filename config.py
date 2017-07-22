#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

DEBUG = False

pid_file = 'pid.sock'

max_requests = 100000

daemon_flag = False

process_num = 2

max_page_limiter = 30

spider_limiter = {
    'timeout': 10,
    'success_t': 0.3,
    'faild_t': 10
}

log_file = "std.log"

mysql_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": 'root',
    "passwd": '123123',
    "db": 'jd_spider',
}

redis_config = {
    "host": "127.0.0.1",
    "host": 6379
}

rd = redis.StrictRedis()

JD_URLS_TASK = "jd_urls_task"

JD_URLS_RESULT = "jd_urls_result"

PLIST_FEEDS_URLS = [
    'http://list.jd.com/list.html?cat=6196,6197,6199&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6200&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6202&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6201&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6203&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6204&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6205&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6206&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,6207&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6197,11976&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6223&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6224&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6220&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6221&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,11979&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6850&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6225&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6214,6215&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6214,6218&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6214,11977&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6214,6216&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6214,11978&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6227,6228&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6227,6230&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6227,6231&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6227,6232&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6227,11975&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11149,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11150,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11155,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11151,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11152,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11153,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11154,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,11143,11156,11148&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6219,6222&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,6211&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,6212&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,6209&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,6210&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,11980&page=1&delivery=1&trans=1&JL=4_10_0#J_main',
    'http://list.jd.com/list.html?cat=6196,6198,11981&page=1&delivery=1&trans=1&JL=4_10_0#J_main'
]


PLIST_MORE_URLS = [
    'http://list.jd.com/list.html?cat=6196,6197,6199&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6200&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6202&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6201&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6203&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6204&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6205&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6206&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,6207&page=1',
    'http://list.jd.com/list.html?cat=6196,6197,11976&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6223&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6224&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6220&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6221&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,11979&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6850&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6225&page=1',
    'http://list.jd.com/list.html?cat=6196,6214,6215&page=1',
    'http://list.jd.com/list.html?cat=6196,6214,6218&page=1',
    'http://list.jd.com/list.html?cat=6196,6214,11977&page=1',
    'http://list.jd.com/list.html?cat=6196,6214,6216&page=1',
    'http://list.jd.com/list.html?cat=6196,6214,11978&page=1',
    'http://list.jd.com/list.html?cat=6196,6227,6228&page=1',
    'http://list.jd.com/list.html?cat=6196,6227,6230&page=1',
    'http://list.jd.com/list.html?cat=6196,6227,6231&page=1',
    'http://list.jd.com/list.html?cat=6196,6227,6232&page=1',
    'http://list.jd.com/list.html?cat=6196,6227,11975&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11149,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11150,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11155,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11151,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11152,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11153,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11154,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,11143,11156,11148&page=1',
    'http://list.jd.com/list.html?cat=6196,6219,6222&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,6211&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,6212&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,6209&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,6210&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,11980&page=1',
    'http://list.jd.com/list.html?cat=6196,6198,11981&page=1'
]
