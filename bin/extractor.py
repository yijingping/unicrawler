# -*- coding: utf-8 -*-
__author__ = 'yijingping'
# 加载django环境
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'unicrawler.settings'
import django
django.setup()

import json
from lxml import etree
from cores.constants import KIND_LIST_URL, KIND_DETAIL_URL
from io import StringIO
from django.conf import settings
from cores.util import get_redis
import logging
logger = logging.getLogger()


class Extractor(object):
    def __init__(self):
        self.redis = get_redis()

    def extract(self, tree, rules):
        res = []
        for rule in rules:
            if rule["kind"] == "xpath":
                res = tree.xpath(rule["data"])
            elif rule["kind"] == "python":
                g, l = {}, {"in_val": res}
                try:
                    exec(rule["data"], g, l)
                    res = l["out_val"]
                except Exception as e:
                    logger.exception(e)

        return res

    def get_detail(self, tree, data):
        # 检查是否在exclude规则内. 如果在,放弃存储
        exclude_rules = data['detail_exclude']
        if self.extract(tree, exclude_rules):
            logger.debug('# url in excludes, abort!')
            return

        # 不在exclude规则内,可以存储
        result = {
            "url": data['url'],
            "seed_id": data['seed_id'],
            'detail_multi': data['detail_multi']
        }
        rules = data['detail_rules']
        for item in rules:
            col = item["key"]
            print col
            col_rules = item["rules"]
            col_value = self.extract(tree, col_rules)
            result[col] = col_value

        self.redis.lpush(settings.CRAWLER_CONFIG["processor"], json.dumps(result))
        logger.debug('extracted:%s' % result)

    def run(self):
        r = get_redis()
        r.delete(settings.CRAWLER_CONFIG["extractor"])
        while True:
            try:
                data = r.brpop(settings.CRAWLER_CONFIG["extractor"])
            except Exception as e:
                print e
                continue
            #print data
            data = json.loads(data[1])
            body = data['body']
            htmlparser = etree.HTMLParser()
            tree = etree.parse(StringIO(body), htmlparser)
            # 如果当前接卸的页面是列表页
            if data["kind"] == KIND_LIST_URL:
                # 先找详情页
                detail_urls = self.extract(tree, data['list_rules'])
                #logger.debug('detail_urls: %s' % detail_urls)
                for item in detail_urls:
                    item_data = {
                        "url": item,
                        'kind': KIND_DETAIL_URL,
                        'seed_id': data['seed_id'],
                        'rule_id': data['rule_id'],
                        #'fresh_pages': '',
                        #'list_rules': '',
                        #'next_url_rules': '',
                        'site_config': data['site_config'],
                        'detail_rules': data['detail_rules'],
                        'detail_exclude': data['detail_exclude'],
                        'detail_multi': data['detail_multi']
                    }
                    r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(item_data))

                # 后找下一页
                next_urls = self.extract(tree, data["next_url_rules"])
                print 'next_urls: %s' % next_urls
                for item in next_urls:
                    item_data = {
                        "url": item,
                        'kind': KIND_LIST_URL,
                        'seed_id': data['seed_id'],
                        'rule_id': data['rule_id'],
                        'fresh_pages': data['fresh_pages'] - 1,
                        'site_config': data['site_config'],
                        'list_rules': data['list_rules'],
                        'next_url_rules': data['next_url_rules'],
                        'detail_rules': data['detail_rules'],
                        'detail_exclude': data['detail_exclude'],
                        'detail_multi': data['detail_multi']
                    }
                    if item_data['fresh_pages'] > 0:
                        logger.debug('list:%s' % data['url'])
                        r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(item_data))
            # 如果当前解析的页面是详情页
            elif data["kind"] == KIND_DETAIL_URL:
                logger.debug('detail:%s' % data['url'])
                # 检查详情页是否有多项详情
                multi_rules = data['detail_multi']
                if multi_rules:
                    multi_parts = self.extract(tree, multi_rules)
                    for part in multi_parts:
                        tree = etree.parse(StringIO(part), htmlparser)
                        self.get_detail(tree, data)
                else:
                    # 如果没有多项详情,则只是单项
                    self.get_detail(tree, data)


if __name__ == '__main__':
    extractor = Extractor()
    extractor.run()
