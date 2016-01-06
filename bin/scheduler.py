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
from cores.models import Schema, Seed


class Scheduler():
    def run(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=3)
        for item in Schema.objects.all().order_by('-weight'):
            seeds = Seed.objects.filter(schema=item)
            for seed in seeds:
                r.lpush('unicrawler:urls',json.dumps({
                    'url': seed.url, 'kind':0, 'seed_id':seed.pk,
                    'list_rules':seed.list_rules, 'next_url_rules': seed.next_url_rules
                }))

        #print r.rpop('unicrawler:urls')

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()