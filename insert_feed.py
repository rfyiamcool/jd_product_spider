#!/usr/bin/env python
# -*- coding:utf-8 -*-

from config import rd, PLIST_FEEDS_URLS, JD_URLS_TASK, PLIST_MORE_URLS


def insert_feeds(feed_list):
    for _url in feed_list:
        print _url
        rd.sadd(JD_URLS_TASK, _url)


if __name__ == "__main__":
    select = raw_input("选择抓取的类型\n全部 all |  京东自营 ziying\n")
    if select == "all":
        insert_feeds(PLIST_MORE_URLS)
    elif select == "ziying":
        insert_feeds(PLIST_FEEDS_URLS)
    else:
        raise('all or ziying')
    print "insert feeds success !!!"
