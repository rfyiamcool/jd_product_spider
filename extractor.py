#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import time
import traceback
from urlparse import parse_qs, urlparse

import requests
from peewee import IntegrityError
from lxml.html import tostring, fromstring

from config import *
from utils import *
from log import logger
from spider import fetch
from models import Product, Category, ProductAndCategory


rd = redis.StrictRedis()


def parse_category(url, doc, res=''):
    '''
        desc:
            用来解析面包屑, 分析出具体商品所属的cat层
    '''
    save_list = []
    _sum_url = doc.xpath('//*[@id="root-nav"]/div/div/span[1]/a[2]/@href')[0]
    _cat_list = parse_qs(urlparse(_sum_url).query, keep_blank_values=False).get('cat')[0]
    cat_list = [int(x) for x in _cat_list.split(',')]
    assert len(cat_list) == 3
    l1_name = doc.xpath('//*[@id="root-nav"]/div/div/strong/a')[0].text_content()
    l1_url = doc.xpath('//*[@id="root-nav"]/div/div/strong/a/@href')[0]
    l2_url = doc.xpath('//*[@id="root-nav"]/div/div/span[1]/a[1]/@href')[0]
    l2_name = doc.xpath('//*[@id="root-nav"]/div/div/span[1]/a[1]')[0].text_content()
    l3_url = doc.xpath('//*[@id="root-nav"]/div/div/span[1]/a[2]/@href')[0]
    l3_name = doc.xpath('//*[@id="root-nav"]/div/div/span[1]/a[2]/text()')[0]

    save_list.append({"cat_id": cat_list[0], "cat_name": l1_name, "cat_url": l1_url, "level":'1'})
    save_list.append({"cat_id": cat_list[1], "cat_name": l2_name, "cat_url": l2_url, "level":'2'})
    save_list.append({"cat_id": cat_list[2], "cat_name": l3_name, "cat_url": l3_url, "level":'3'})
    for _d  in save_list:
        try:
            _d['cat_name'] = _d['cat_name'].encode('utf-8')
            _d['cat_url'] = perfect_href(_d['cat_url'])
            Category.create(**_d)
        except IntegrityError:
            logger.info('category faild repeat --- cat_id: %s , url:%s'%(_d['cat_id'], url))
    res = {
        'top_id': cat_list[0],
        'second_id': cat_list[1],
        'third_id': cat_list[2],
        'top_name': l1_name.encode('utf-8'),
        'second_name': l2_name.encode('utf-8'),
        'third_name': l3_name.encode('utf-8'),
    }
    return res


def extract_plist_url(url, doc, res=''):
    '''
        desc:
            从list.jd.com里抽出分页及产品url,扔到队列里
        example url:
            http://list.jd.com/list.html?cat=6196,6197,6199&page=1&delivery=1&trans=1&JL=4_10_0#J_main
    '''
    _page = parse_qs(urlparse(url).query, keep_blank_values=False).get('page')
    if _page and int(_page[0]) == 1:
        max_page = int(doc.xpath('//span[@class="p-skip"]/em/b')[0].text_content())  # 获取该类别最大的页码
        if isinstance(max_page,int) and max_page > 1:
            for _p in range(2,max_page):
                if _p > max_page_limiter:
                    continue
                print re.sub('page=1',"page=%s"%_p, url)
                queue_push_url(re.sub('page=1',"page=%s"%_p, url))

    plist_doc = doc.xpath('//ul[@class="gl-warp clearfix "]')[0]  # 拿到商品列表的标签
    plist = re.findall('//item.jd.com/\d*.html', tostring(plist_doc))
    for _one in plist:
        purl = "http:" + _one
        if Product.select().where(Product.purl == purl).first():
            logger.info('extract_plist_url --- product %s exist'%(purl))
            continue
        else:
            queue_push_url(purl)


def extract_product_detail(url, doc, res=''):
    '''
        desc:
            通过详情页获取一系列信息,入库
    '''
    if not doc.xpath('//div[@class="breadcrumb"]'):
        logger.info('extract_product_detail --- url %s  %s'%(url, u'全球购不处理!!!'))
        return

    if doc.xpath('//div[@class="breadcrumb"]//a/text()')[0] == u"首页":
        logger.info('extract_product_detail --- url %s  %s'%(url, u'闪购页面暂时不处理!!!'))
        return

    _this_dao = Product.select().where(Product.purl == url).first()
    if _this_dao:
        logger.info('extract_product_detail --- product %s exist'%(url))
        return

    # pid
    pid = re.search('http://item.jd.com/(?P<id>\d*).html', url).groupdict()['id']

    # product brand
    brand = doc.xpath('//*[@id="parameter-brand"]/li/a[1]')[0].text_content()
    # same detail page not contains brand img ,so set null
    _brand_img = doc.xpath('//*[@id="extInfo"]/div[1]/a/img/@src')
    if _brand_img:
        brand_img = _brand_img[0]
        brand_img = perfect_href(brand_img)
    else:
        brand_img = ''

    # product img
    imgs = doc.xpath('//div[@class="spec-items"]/ul/li/img/@src')
    fix_img = lambda x: re.sub('/n5/','/imgzone/', "http:" + x)
    imgs = map(fix_img, imgs)
    img_first = imgs.pop(0)

    # pname
    pname = doc.xpath('//div[@id="product-intro"]//div[@id="itemInfo"]//h1')[0].text_content()

    # 价格
    _price_url = "http://p.3.cn/prices/get?skuid=J_{pid}"
    price = None
    _price_res = fetch(_price_url.format(pid=pid))


    if _price_res.status_code == 200:
        price = json.loads(_price_res.text)[0]['p']
    else:
        raise("Not Parse Price")

    # 面包屑 == category
    _cat_body = parse_category(url, doc, res)
    if not ProductAndCategory.select().where(ProductAndCategory.pid== pid).first():
        _cat_body.update({'pid':int(pid)})
        ProductAndCategory.create(**_cat_body)

    data = {
        'pid': pid,
        'purl': url,
        'pname': pname.encode('utf-8'),
        'brand': brand.encode('utf-8'),
        'brand_img': brand_img,
        'product_img': img_first,
        'price': price,
        'extra': json.dumps({'img':imgs})
    }
    try:
        Product.create(**data)
        logger.info('product success save--- url: %s'%(url))
    except IntegrityError:
        logger.info('product faild repeat --- url: %s'%(url))
    except Exception, e:
        ex = traceback.format_exc()
        logger.error('product faild exception --- url: %s\n %s'%(url, ex))


def extractor_worker():
    func_map = {
        #re.compile('http:\/\/list.jd.com\/list.html\?cat=.*&page=\d*&delivery'): extract_plist_url,
        re.compile('http:\/\/list.jd.com\/list.html\?cat=.*&page=\d*'): extract_plist_url,
        re.compile('^http:\/\/item.jd.com/\d*.html$'): extract_product_detail
    }

    while 1:
        url, view = queue_pop_result()
        if not url:
            time.sleep(1)
            continue
        mark = False
        for reg, func in func_map.items():
            if reg.search(url):
                mark = True
                doc = fromstring(view)
                try:
                    func(url, doc, view)
                except Exception, e:
                    logger.error('''Raise Error:\n
                            url: %s\n
                            error: %s\n'''%(url, traceback.format_exc()))
        if not mark:
            logger.error('not match any regex | func -- url: %s'%url)
        time.sleep(0.01)


def test_one():
    import pdb;pdb.set_trace()
    res = fetch(url)
    doc = fromstring(d.text.decode('utf-8', errors='ignore'))
    parse_category(doc)


if __name__ == "__main__":
    extractor_worker()

