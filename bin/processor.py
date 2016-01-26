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
from hashlib import md5
from django.conf import settings
import logging
logger = logging.getLogger()


class Processor():
    def run(self):
        r = redis.StrictRedis(**settings.REDIS_OPTIONS)
        r.delete('unicrawler:data')
        while True:
            try:
                data = r.brpop('unicrawler:data:topics')
            except Exception as e:
                print e
                continue

            data = json.loads(data[1])
            print json.dumps(data, encoding="UTF-8", ensure_ascii=False)
            print '--------------------------------------------------------------'


if __name__ == '__main__':
    processor = Processor()
    processor.run()
