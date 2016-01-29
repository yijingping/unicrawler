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
from cores.models import Seed, IndexRule, DetailRule
from cores.constants import KIND_LIST_URL
from django.conf import settings
import logging
logger = logging.getLogger()
from datetime import datetime, timedelta
import time

class Scheduler():
    def run(self):
        r = redis.StrictRedis(**settings.REDIS_OPTIONS)
        while True:
            now = datetime.now()
            for item in Seed.objects.filter(status=Seed.STATUS_ENABLE).order_by('-weight'):
                rules = IndexRule.objects.filter(seed=item, status=IndexRule.STATUS_ENABLE, next_crawl_time__lte=now)
                for rule in rules:
                    try:
                        deital_rule = DetailRule.objects.get(index_rule=rule)
                    except DetailRule.DoesNotExist as e:
                        print e
                        continue

                    data = {
                        'url': rule.url,
                        'kind': KIND_LIST_URL,
                        'rule_id': rule.pk,
                        'site_config': rule.site.get_config(),
                        'list_rules': rule.list_rules,
                        'next_url_rules': rule.next_url_rules,
                        'detail_rules': deital_rule.data,
                        "seed_id": item.pk,
                        "fresh_pages": rule.fresh_pages
                    }
                    r.lpush('unicrawler:urls', json.dumps(data))
                    # 更新index_rule
                    rule.next_crawl_time = now + timedelta(seconds=rule.frequency)
                    rule.save()

                    logging.debug(data)

            #print r.rpop('unicrawler:urls')
            time.sleep(1)

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()