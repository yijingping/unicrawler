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
import requests
from django.conf import settings

import logging
logger = logging.getLogger()
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
}

class Downloader():
    def run(self):
        r = redis.StrictRedis(**settings.REDIS_OPTIONS)
        r.delete('unicrawler:urls')
        while True:
            try:
                data = r.brpop('unicrawler:urls')
            except Exception as e:
                print e
                continue

            try:
                data = json.loads(data[1])
                print data["url"]
                rsp = requests.get(data["url"], headers=HEADER)
                data['body'] = rsp.text
                logging.debug(data)
                r.lpush('unicrawler:urls-body', json.dumps(data))
            except Exception as e:
                print e


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
