# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import collections
from django.db import models
from jsonfield import JSONField


class Seed(models.Model):
    STATUS_ENABLE = 1
    STATUS_DISABLE = 2
    STATUS_CHOICES = (
        (STATUS_ENABLE, '启用'),
        (STATUS_DISABLE, '禁用')
    )
    name = models.CharField(max_length=100, verbose_name='模板名称')
    desc = models.TextField(verbose_name='简介')
    data = JSONField(verbose_name='存储数据配置', load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, default=[])
    weight = models.IntegerField(default=0, verbose_name='权重')
    status = models.IntegerField(default=STATUS_ENABLE, choices=STATUS_CHOICES, verbose_name="是否启用")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "种子"


class Site(models.Model):
    STATUS_ENABLE = 1
    STATUS_DISABLE = 2
    STATUS_CHOICES = (
        (STATUS_ENABLE, '启用'),
        (STATUS_DISABLE, '禁用')
    )
    PROXY_NONE = 1
    PROXY_NORMAL = 2
    PROXY_CHOICES = (
        (PROXY_NONE, '不使用代理'),
        (PROXY_NORMAL, '普通代理')
    )
    BROWSER_NONE = 1
    BROWSER_NORMAL = 2
    BROWSER_CHOICES = (
        (BROWSER_NONE, '不使用浏览器壳'),
        (BROWSER_NORMAL, '普通浏览器')
    )
    name = models.CharField(max_length=100, verbose_name='站点名称')
    domain = models.CharField(unique=True, max_length=100, verbose_name='站点域名')
    proxy = models.IntegerField(default=PROXY_NONE, verbose_name='代理')
    browser = models.IntegerField(default=BROWSER_NONE, verbose_name='浏览器壳')
    limit_speed = models.IntegerField(default=100, verbose_name='访问间隔(毫秒)')
    status = models.IntegerField(default=STATUS_ENABLE, choices=STATUS_CHOICES, verbose_name="是否启用")

    def get_config(self):
        if self.status == self.STATUS_ENABLE:
            return {
                'domain': self.domain,
                'proxy': self.proxy,
                'browser': self.browser,
                'limit_speed': self.limit_speed
            }
        else:
            return {
                'domain': self.domain,
                'proxy': self.PROXY_NONE,
                'browser': self.BROWSER_NONE,
                'limit_speed': 0
            }

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "站点配置"


class IndexRule(models.Model):
    STATUS_ENABLE = 1
    STATUS_DISABLE = 2
    STATUS_CHOICES = (
        (STATUS_ENABLE, '启用'),
        (STATUS_DISABLE, '禁用')
    )
    seed = models.ForeignKey(Seed)
    name = models.CharField(max_length=100, verbose_name='来源')
    site = models.ForeignKey(Site)
    url = models.CharField(max_length=100, verbose_name='索引url')
    list_rules = JSONField(verbose_name='获取列表项的规则', load_kwargs={'object_pairs_hook': collections.OrderedDict})
    next_url_rules = JSONField(verbose_name='下一页索引的规则列表', load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, default=[])
    frequency = models.IntegerField(default=60, verbose_name='爬取频率,单位秒')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    next_crawl_time = models.DateTimeField(verbose_name='下次爬取时间')
    fresh_pages = models.IntegerField(default=2, verbose_name='爬取页面数')
    status = models.IntegerField(default=STATUS_ENABLE, choices=STATUS_CHOICES, verbose_name="是否启用")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "索引和列表规则"


class DetailRule(models.Model):
    index_rule = models.ForeignKey(IndexRule)
    data = JSONField(verbose_name='详情页规则', load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return '%s, %s' % (self.index_rule.name, self.index_rule.url)

    class Meta:
        verbose_name_plural = "详情页爬取规则"