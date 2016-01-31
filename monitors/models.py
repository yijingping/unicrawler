# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import collections
from django.db import models
from jsonfield import JSONField


class Service(models.Model):
    scheduler = models.IntegerField(default=0, verbose_name='未执行的计划数')
    downloader = models.IntegerField(default=0, verbose_name='未下载的url数')
    extractor = models.IntegerField(default=0, verbose_name='未抽取的url数')
    processor = models.IntegerField(default=0, verbose_name='未入库的记录数')
    create_time = models.DateTimeField(verbose_name='创建时间', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1 服务队列积压"


