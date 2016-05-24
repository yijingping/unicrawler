# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from abc import ABCMeta
from abc import abstractmethod

import _mysql
import torndb
from datetime import datetime
from django.utils.encoding import smart_str, smart_unicode
from django.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cores.util import get_uniqueid
import logging
logger = logging.getLogger()


class BaseProcessorBackend(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process(self, data):
        pass


class MysqlBackend(BaseProcessorBackend):
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
        data.pop('rule_id', None)
        data.pop('detail_multi', None)
        # 更新或插入数据库
        #print data
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


class DjangoModelBackend(BaseProcessorBackend):
    def __init__(self, config):
        self.defaults = config['defaults']
        self.unique_key = config["unique_key"]
        modelstr = config["DjangoModel"]
        modelclass = models.get_model(modelstr.split('.')[0], modelstr.split('.')[-1])
        self._class = modelclass

    def process(self, params):
        C = self._class
        params['uniqueid'] = get_uniqueid('%s:%s' % (params['wechat_id'], params['title']))

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
        data.pop('rule_id', None)
        data.pop('detail_multi', None)
        # 更新或插入数据库
        try:
            C.objects.update_or_create(uniqueid=data['uniqueid'], defaults=data)
        except Exception as e:
            logger.exception(e)
        finally:
            logger.debug(data['url'])



class MongoDBBackend(BaseProcessorBackend):
    pass


class PostgresBackend(BaseProcessorBackend):
    @property
    def _table(self):
        return self.db_table

    def __init__(self, config):
        db_config = config['database']
        conn_url = "postgresql://%s:%s@%s/%s" % (
            db_config.get("user"), db_config.get("password"),
            db_config.get("host"), db_config.get("name")
        )
        self.engine = create_engine(conn_url)
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
        data.pop('rule_id', None)
        data.pop('detail_multi', None)
        # 更新或插入数据库
        #print data
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

        with self.engine.connect() as con:
            res = con.execute(sql, *values)

    def update(self, params, filters=None):
        set_keys = params.keys()
        values = params.values()
        set_placeholder = ', '.join([item+'=%s' for item in set_keys])
        sql = 'UPDATE ' + self._table + ' SET ' + set_placeholder
        if filters:
            where_keys = filters.keys()
            where_values = filters.values()
            where_placeholder = ', '.join([item+'=%s' for item in where_keys])
            sql = sql + ' WHERE ' + where_placeholder
            values += where_values
        rowcount = 0
        with self.engine.connect() as con:
            res = con.execute(sql, *values)
            rowcount = res.rowcount
        return rowcount

    @staticmethod
    def dict_to_sql(params, sep=', '):
        cols = []
        for k, v in params.iteritems():
            k2 = _mysql.escape_string(str(k))
            if v is None:
                col = '%s=NULL' % k2
            elif isinstance(v, (int, long, float)):
                col = '%s=%s' % (k2, v)
            elif isinstance(v, unicode):
                v2 =  v.encode('utf-8')
                col = '%s="%s"' % (k2, smart_unicode(_mysql.escape_string(smart_str(v))))
            else:
                col = '%s="%s"' % (k2, v)
            cols.append(col)
        return smart_unicode(sep.join(cols))

    @staticmethod
    def fields_to_sql(fields):
        f2 = ["%s" % item if item != "*" else "*" for item in fields]
        return _mysql.escape_string(', '.join(f2))

