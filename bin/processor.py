# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'yijingping'
# 加载django环境
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'unicrawler.settings'
import django
django.setup()

import _mysql
import torndb
from datetime import datetime
import json
import redis
from hashlib import md5
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
from cores.models import Seed
import logging
logger = logging.getLogger()


def get_uniqueid(url):
    return md5(url).hexdigest()


class MysqlBackend(object):
    @property
    def _table(self):
        return self.db_table

    def __init__(self, db_config, db_table, defaults):
        self.db = torndb.Connection(
            host=db_config.get("host"),
            database=db_config.get("name"),
            user=db_config.get("user"),
            password=db_config.get("password"),
            charset=db_config.get("charset")
        )
        self.db_table = db_table
        self.defaults = defaults

    def process(self, params, filters=None):
        # 加上默认值
        data = params.copy()
        for k, v in self.defaults.iteritems():
            data.setdefault(k, v)
        # 清除数据
        data.pop('seed_id', None)
        data['uniqueid'] = get_uniqueid(data['url'])
        data['update_time'] = str(datetime.now())
        # 更新或插入数据库
        try:
            # try update
            affected = self.update(data, {'uniqueid': data['uniqueid']})
            if affected == 0:
                # row not exists, try create
                data['create_time'] = str(datetime.now())
                self.create(data)
        except Exception as e:
            logger.exception(e)
        finally:
            logger.debug(data['url'])

    def create(self, params):
        keys = params.keys()
        values = params.values()
        cols = ','.join(map(lambda s:str(s), keys))
        placeholder = ','.join(['%s' for _ in range(len(keys))])
        sql = 'INSERT INTO ' + self._table + ' (' + cols + ') ' + ' VALUES (' + placeholder + ');'

        return self.db.insert(sql, *values)

    def update(self, params, filters=None):
        set_keys = params.keys()
        set_values = params.values()
        set_placeholder = ', '.join(['`'+item+'`=%s' for item in set_keys])
        sql = 'UPDATE ' + self._table + ' SET ' + set_placeholder
        if filters:
            where_keys = filters.keys()
            where_values = filters.values()
            where_placeholder = ', '.join(['`'+item+'`=%s' for item in where_keys])
            sql = sql + ' WHERE ' + where_placeholder
            values = set_values + where_values
        return self.db.update(sql, *values)

    @staticmethod
    def dict_to_sql(params, sep=', '):
        cols = []
        for k, v in params.iteritems():
            k2 = _mysql.escape_string(str(k))
            if v is None:
                col = '`%s`=NULL' % k2
            elif isinstance(v, (int, long, float)):
                col = '`%s`=%s' % (k2, v)
            elif isinstance(v, unicode):
                v2 =  v.encode('utf-8')
                col = '`%s`="%s"' % (k2, smart_unicode(_mysql.escape_string(smart_str(v))))
            else:
                col = '`%s`="%s"' % (k2, v)
            cols.append(col)
        return smart_unicode(sep.join(cols))

    @staticmethod
    def fields_to_sql(fields):
        f2 = ["`%s`" % item if item != "*" else "*" for item in fields]
        return _mysql.escape_string(', '.join(f2))


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
                        backend = MysqlBackend(config["database"], config["table"], config["defaults"])
                        my_config = self.pools.get(seed_id, [])
                        my_config.append(backend)
                        self.pools[seed_id] = my_config

                return self.pools.get(seed_id, [])

    def process(self, data):
        backends = self.get_backends(data['seed_id'])
        for backend in backends:
            backend.process(data)

    def run(self):
        r = redis.StrictRedis(**settings.REDIS_OPTIONS)
        #r.delete('unicrawler:data')
        while True:
            try:
                rsp = r.brpop('unicrawler:data')
            except Exception as e:
                print e
                continue

            data = json.loads(rsp[1])
            #logger.info(json.dumps(data, encoding="UTF-8", ensure_ascii=False))
            self.process(data)


if __name__ == '__main__':
    processor = Processor()
    processor.run()
