# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.db import models


class Schema(models.Model):
    name = models.CharField(max_length=100, verbose_name='模板名称')
    desc = models.TextField(verbose_name='简介')
    data = models.TextField(verbose_name='详细结构')
    weight = models.IntegerField(default=0, verbose_name='权重')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "模板"


class Seed(models.Model):
    schema = models.ForeignKey(Schema)
    name = models.CharField(max_length=100, verbose_name='来源网站名称')
    site = models.CharField(max_length=100, verbose_name='来源网站域名')
    url = models.CharField(max_length=100, verbose_name='索引url')
    list_rules = models.TextField(verbose_name='获取列表项的规则')
    next_url_rules = models.TextField(verbose_name='下一页索引的规则列表')
    frequency = models.IntegerField(default=60, verbose_name='爬取频率,单位秒')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    next_crawl_time = models.DateTimeField(auto_now_add=True, verbose_name='下次爬取时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "来源种子"


class Rule(models.Model):
    seed = models.ForeignKey(Seed)
    data = models.TextField(verbose_name='详细规则')

    def __unicode__(self):
        return '%s, %s' % (self.seed.name, self.seed.url)

    class Meta:
        verbose_name_plural = "详情页爬取规则"