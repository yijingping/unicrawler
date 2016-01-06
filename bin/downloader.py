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


class Downloader():
    def run(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=3)
        r.delete('unicrawler:urls')
        while True:
            try:
                data = r.brpop('unicrawler:urls')
            except Exception as e:
                print e
                continue

            data = json.loads(data[1])
            print data["url"]
            rsp = requests.get(data["url"])
            data['body'] = rsp.text
            #print data
            r.lpush('unicrawler:urls-body', json.dumps(data))


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
