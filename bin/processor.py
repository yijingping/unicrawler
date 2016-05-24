# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

import json
from django.conf import settings
from cores.models import Seed
from cores.util import get_redis
from cores.processors import MysqlBackend, PostgresBackend, DjangoModelBackend, MongoDBBackend

import logging
logger = logging.getLogger()


class Processor():
    def __init__(self):
        self.pools = {}

    def get_backends(self, seed_id):
        cache = self.pools.get(seed_id, None)
        if cache:
            return cache
        else:
            try:
               seed = Seed.objects.get(pk=seed_id)
            except Seed.DoesNotExist as e:
                logger.exception(e)
                return []
            else:
                for config in seed.data:
                    if config["kind"] == "mysql":
                        backend = MysqlBackend(config)
                    elif config["kind"] == "mongodb":
                        backend = MongoDBBackend(config)
                    elif config["kind"] == "postgres":
                        backend = PostgresBackend(config)
                    elif config["kind"] == "DjangoModel":
                        backend = DjangoModelBackend(config)

                    my_config = self.pools.get(seed_id, [])
                    my_config.append(backend)
                    self.pools[seed_id] = my_config

                return self.pools.get(seed_id, [])

    def process(self, data):
        backends = self.get_backends(data['seed_id'])
        for backend in backends:
            backend.process(data)

    def run(self):
        r = get_redis()
        if settings.CRAWLER_DEBUG:
            r.delete(settings.CRAWLER_CONFIG["processor"])
        while True:
            try:
                rsp = r.brpop(settings.CRAWLER_CONFIG["processor"])
            except Exception as e:
                print e
                continue

            data = json.loads(rsp[1])
            #logger.info(json.dumps(data, encoding="UTF-8", ensure_ascii=False))
            self.process(data)


if __name__ == '__main__':
    processor = Processor()
    processor.run()
