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
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
from cores.models import Seed
from cores.util import get_redis, get_uniqueid
import logging
logger = logging.getLogger()


class MysqlBackend(object):
    @property
    def _table(self):
        return self.db_table

    def __init__(self, config):
        db_config = config['database']
        self.db = torndb.Connection(
            host=db_config.get("host"),
            database=db_config.get("name"),
            user=db_config.get("user"),
            password=db_config.get("password"),
            charset=db_config.get("charset")
        )
        self.db_table = config['table']
        self.defaults = config['defaults']
        self.unique_key = config["unique_key"]

    def process(self, params, filters=None):
        # 加上默认值
        data = params.copy()
        for k, v in self.defaults.iteritems():
            data.setdefault(k, v)

        # 设置唯一键
        unique_value = ':'.join(['%s' % data[k] for k in self.unique_key])
        data['uniqueid'] = get_uniqueid(unique_value)
        data['update_time'] = str(datetime.now())
        # 清除数据
        data.pop('seed_id', None)
        data.pop('detail_multi', None)
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
        values = params.values()
        set_placeholder = ', '.join(['`'+item+'`=%s' for item in set_keys])
        sql = 'UPDATE ' + self._table + ' SET ' + set_placeholder
        if filters:
            where_keys = filters.keys()
            where_values = filters.values()
            where_placeholder = ', '.join(['`'+item+'`=%s' for item in where_keys])
            sql = sql + ' WHERE ' + where_placeholder
            values += where_values
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
                        backend = MysqlBackend(config)
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
        if settings.DEBUG:
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
