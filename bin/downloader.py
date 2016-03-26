# -*- coding: utf-8 -*-
__author__ = 'yijingping'
# 加载django环境
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8') 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'unicrawler.settings'
import django
django.setup()

import time
import json
from django.conf import settings
from cores.models import Site
from cores.util import get_redis, get_uniqueid
from cores.constants import KIND_DETAIL_URL
from cores.downloaders import RequestsDownloaderBackend, SeleniumDownloaderBackend
from configs.proxies import MysqlProxyBackend

import logging
logger = logging.getLogger()


class Downloader(object):
    def __init__(self):
        self.redis = get_redis()

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

    def check_detail_fresh_time(self, data):
        unique_key, fresh_time, rule_id = data['unique_key'], data["detail_fresh_time"], data["rule_id"]
        if fresh_time <= 0:
            return False
        else:
            unique_value = ''.join([data.get(item) for item in unique_key])
            key = 'unicrawler:detail_fresh_time:%s:%s' % (rule_id, get_uniqueid(unique_value))
            if self.redis.exists(key):
                return True
            else:
                self.redis.setex(key, fresh_time, fresh_time)
                return False

    def run(self):
        r = self.redis
        if settings.CRAWLER_DEBUG:
            r.delete(settings.CRAWLER_CONFIG["downloader"])
        while True:
            try:
                resp_data = r.brpop(settings.CRAWLER_CONFIG["downloader"])
            except Exception as e:
                print e
                continue

            try:
                data = json.loads(resp_data[1])
                site_config = data['site_config']
                logger.debug(data["url"])
                is_limited, proxy = self.check_limit_speed(site_config)
                if is_limited:
                    print '# 被限制, 放回去, 下次下载'
                    time.sleep(1)  # 休息一秒, 延迟放回去的时间
                    r.lpush(settings.CRAWLER_CONFIG["downloader"], resp_data[1])
                elif (data["kind"] == KIND_DETAIL_URL
                    and self.check_detail_fresh_time(data)):
                    print '# 该详情页已下载过, 不下载了'
                else:
                    print '# 未被限制,可以下载'
                    if site_config['browser'] == Site.BROWSER_NONE:
                        browser = RequestsDownloaderBackend(proxy=proxy)
                    elif site_config['browser'] == Site.BROWSER_NORMAL:
                        browser = SeleniumDownloaderBackend(proxy=proxy)
                    else:
                        return

                    data['body'] = browser.download(data["url"])
                    r.lpush(settings.CRAWLER_CONFIG["extractor"], json.dumps(data))
                    logger.debug(data)
            except Exception as e:
                print e
                raise


if __name__ == '__main__':
    downloader = Downloader()
    downloader.run()
