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
from cores.constants import KIND_LIST_URL, KIND_DETAIL_URL
from django.conf import settings
from cores.util import get_redis, get_uniqueid
from cores.extractors import XPathExtractor, PythonExtractor, ImageExtractor, VideoExtractor
import logging
logger = logging.getLogger()


class Extractor(object):
    def __init__(self):
        self.redis = get_redis()

    def extract(self, content, rules, context):
        res = content
        for rule in rules:
            extractor = None
            if rule["kind"] == "xpath":
                extractor = XPathExtractor(res, rule["data"])
            elif rule["kind"] == "python":
                extractor = PythonExtractor(rule["data"], res, context=context)
            elif rule["kind"] == "image":
                extractor = ImageExtractor(res)
            elif rule["kind"] == "video":
                extractor = VideoExtractor(res)

            res = extractor.extract()

        return res

    def check_detail_fresh_time(self, unique_url, fresh_time):
        if fresh_time <= 0:
            return False
        else:
            key = 'unicrawler:detail_fresh_time:%s' % get_uniqueid(unique_url)
            if self.redis.exists(key):
                return True
            else:
                self.redis.setex(key, fresh_time, fresh_time)
                return False

    def get_detail(self, content, data):
        # 检查是否在exclude规则内. 如果在,放弃存储
        exclude_rules = data['detail_exclude']
        excluded = self.extract(content, exclude_rules, {'data': data})
        if excluded and excluded != content:
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
            col_value = self.extract(content, col_rules, {'data': data})
            result[col] = col_value

        # 检查多项详情新鲜度
        if data['detail_multi']:
            if self.check_detail_fresh_time(result['url'], data["detail_fresh_time"]):
                # 未过期,不更新
                logger.info('检查多项详情未过期,不更新')
            else:
                # 已过期,更新
                self.redis.lpush(settings.CRAWLER_CONFIG["processor"], json.dumps(result))
                logger.debug('extracted:%s' % result)
        else:
            # 已过期,更新
            self.redis.lpush(settings.CRAWLER_CONFIG["processor"], json.dumps(result))
            logger.debug('extracted:%s' % result)

    def run(self):
        r = get_redis()
        if settings.CRAWLER_DEBUG:
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
            # 1 如果当前接卸的页面是列表页
            if data["kind"] == KIND_LIST_URL:
                # 1.1先找详情页
                # 检查详情的内容是否都包含在列表页中
                multi_rules = data['detail_multi']
                if multi_rules:
                    # 1.1.1 详情都包含在列表页中
                    multi_parts = self.extract(body, multi_rules, {'data': data})
                    for part in multi_parts:
                        self.get_detail(part, data)
                else:
                    # 1.1.2 详情不在列表中,通过列表url去访问详情
                    detail_urls = self.extract(body, data['list_rules'], {'data': data})
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
                            'detail_multi': data['detail_multi'],
                            'detail_multi_unique': data['detail_multi_unique'],
                            'detail_fresh_time': data['detail_fresh_time'],
                            'unique_key': data['unique_key']
                        }
                        r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(item_data))

                # 1.2后找下一页
                next_urls = self.extract(body, data["next_url_rules"], {'data': data})
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
                        'detail_multi': data['detail_multi'],
                        'detail_multi_unique': data['detail_multi_unique'],
                        'detail_fresh_time': data['detail_fresh_time'],
                        'unique_key': data['unique_key']
                    }
                    if item_data['fresh_pages'] > 0:
                        logger.debug('list:%s' % data['url'])
                        r.lpush(settings.CRAWLER_CONFIG["downloader"], json.dumps(item_data))
            # 2 如果当前解析的页面是详情页
            elif data["kind"] == KIND_DETAIL_URL:
                logger.debug('detail:%s' % data['url'])
                # 如果没有多项详情,则只是单项
                self.get_detail(body, data)


if __name__ == '__main__':
    my_extractor = Extractor()
    my_extractor.run()
