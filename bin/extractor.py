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
import redis
from lxml import etree
from cores.models import Seed, Rule
from io import StringIO


class Extractor():
    def run(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=3)
        r.delete('unicrawler:urls-body')
        while True:
            try:
                data = r.brpop('unicrawler:urls-body')
            except Exception as e:
                print e
                continue
            #print data
            data = json.loads(data[1])
            htmlparser = etree.HTMLParser()
            body = data['body']
            tree = etree.parse(StringIO(body), htmlparser)
            # 列表页
            if data["kind"] == 0:
                # 找下一页
                next_urls = tree.xpath(data['next_url_rules'])
                for item in next_urls:
                    item_data = data.copy()
                    item_data['url'] = item
                    print 'list:', data['url']
                    r.lpush('unicrawler:urls', json.dumps(item_data))

                # 找详情页
                detail_urls = tree.xpath(data['list_rules'])
                #print 'detail_urls:', detail_urls
                for item in detail_urls:
                    item_data = {
                        "url": item,
                        'kind': 1,
                        'seed_id': data['seed_id']
                    }
                    r.lpush('unicrawler:urls', json.dumps(item_data))
            # 详情页
            elif data["kind"] == 1:
                print 'detail:', data['url']
                rule = Rule.objects.get(seed_id=data['seed_id'])
                seed = Seed.objects.get(pk=data['seed_id'])
                schema = seed.schema
                rules = json.loads(rule.data)
                result = {
                    "seed_id": data['seed_id'],
                    "url": data['url']
                }
                table = json.loads(schema.data)
                for col, format_ in table.iteritems():
                    kind = rules[col]["kind"]
                    if kind == "STRING":
                        result[col] = rules[col]["data"]
                    elif kind == "XPATH":
                        _data = tree.xpath(rules[col]["rule"])
                        if len(_data) > 0:
                            result[col] = _data[0]
                        else:
                            result[col] = ""
                    else:
                        result[col] = ""

                r.lpush('unicrawler:data', json.dumps(result))
                print result


if __name__ == '__main__':
    extractor = Extractor()
    extractor.run()
