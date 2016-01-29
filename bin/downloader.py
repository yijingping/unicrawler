# -*- coding: utf-8 -*-
__author__ = 'yijingping'
# 加载django环境
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'unicrawler.settings'
import django
django.setup()

import time
import json
import redis
import requests
from django.conf import settings
from cores.models import Site, Proxy
from random import sample

import logging
logger = logging.getLogger()


class RequestsDownloaderBackend(object):
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        self.proxy = proxy

    def format_proxies(self):
        p = self.proxy
        if self.proxy:
            if p.user:
                data = 'http://%s:%s@%s:%s' % (p.user, p.password, p.host, p.port)
            else:
                data = 'http://%s:%s' % (p.host, p.port)
            return {
                "http": data
            }
        else:
            return None

    def download(self, url):
        header = sample(self.headers, 1)[0]
        proxies = self.format_proxies()
        rsp = requests.get(url, headers=header, proxies=proxies)
        rsp.encoding = rsp.apparent_encoding
        return rsp.text


class BrowserDownloaderBackend(object):
    def download(self):
        pass


class MysqlProxyBackend(object):
    def __init__(self):
        proxy = Proxy.objects.order_by('?').first()
        self.user = proxy.user
        self.password = proxy.password
        self.host = proxy.host
        self.port = proxy.port

    def __str__(self):
        return ':'.join([str(self.user), str(self.password), str(self.host), str(self.port)])



class Downloader(object):
    def __init__(self):
        self.redis = redis.StrictRedis(**settings.REDIS_OPTIONS)

    def get_proxy(self, kind):
        if kind == Site.PROXY_MYSQL:
            return MysqlProxyBackend()
        else:
            return None

    def check_limit_speed(self, config):
        if config["limit_speed"] <= 0:
            return False, None
        else:
            proxy = self.get_proxy(config['proxy'])
            key = 'unicrawler:limit_speed:%s:%s' % (config['domain'], proxy)
            if self.redis.exists(key):
                return True, proxy
            else:
                self.redis.psetex(key, config["limit_speed"], config["limit_speed"])
                return False, proxy

    def run(self):
        r = self.redis
        r.delete('unicrawler:urls')
        while True:
            try:
                resp_data = r.brpop('unicrawler:urls')
            except Exception as e:
                print e
                continue

            try:
                data = json.loads(resp_data[1])
                set_config = data['site_config']
                logger.debug(data["url"])
                is_limited, proxy = self.check_limit_speed(set_config)
                if is_limited:
                    print '# 被限制, 放回去, 下次下载'
                    time.sleep(1)  # 休息一秒, 延迟放回去的时间
                    r.lpush('unicrawler:urls', resp_data[1])
                else:
                    print '# 未被限制,可以下载'
                    if set_config['browser'] == Site.BROWSER_NONE:
                        browser = RequestsDownloaderBackend(proxy=proxy)
                    else:
                        return

                    # 清理site_config
                    data.pop('site_config', None)
                    data['body'] = browser.download(data["url"])

                    logger.debug(data)
                    r.lpush('unicrawler:urls-body', json.dumps(data))
            except Exception as e:
                print e
                raise


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
