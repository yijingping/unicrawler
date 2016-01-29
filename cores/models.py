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
        verbose_name_plural = "1 种子"


class Site(models.Model):
    STATUS_ENABLE = 1
    STATUS_DISABLE = 2
    STATUS_CHOICES = (
        (STATUS_ENABLE, '启用'),
        (STATUS_DISABLE, '禁用')
    )
    PROXY_NONE = 1
    PROXY_MYSQL = 2
    PROXY_CHOICES = (
        (PROXY_NONE, '不使用代理'),
        (PROXY_MYSQL, '存储在Mysql数据库中的代理')
    )
    BROWSER_NONE = 1
    BROWSER_NORMAL = 2
    BROWSER_CHOICES = (
        (BROWSER_NONE, '不使用浏览器壳'),
        (BROWSER_NORMAL, '普通浏览器')
    )
    name = models.CharField(max_length=100, verbose_name='站点名称')
    domain = models.CharField(unique=True, max_length=100, verbose_name='站点域名')
    proxy = models.IntegerField(default=PROXY_NONE, choices=PROXY_CHOICES, verbose_name='代理')
    browser = models.IntegerField(default=BROWSER_NONE, choices=BROWSER_CHOICES, verbose_name='浏览器壳')
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
        verbose_name_plural = "2 站点配置"


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
        verbose_name_plural = "3 索引和列表规则"


class DetailRule(models.Model):
    index_rule = models.ForeignKey(IndexRule)
    data = JSONField(verbose_name='详情页规则', load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return '%s, %s' % (self.index_rule.name, self.index_rule.url)

    class Meta:
        verbose_name_plural = "4 详情页爬取规则"


class Proxy(models.Model):
    TYPE_TRANSPARENT = 0
    TYPE_ANONYMOUS = 1
    TYPE_CHOICES = (
        (TYPE_TRANSPARENT, '透明代理'),
        (TYPE_ANONYMOUS, '高度匿名'),
    )

    STATUS_NEW = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2
    STATUS_CHOICES = (
        (STATUS_NEW,'未检测'),
        (STATUS_SUCCESS,'检测成功'),
        (STATUS_FAIL,'检测失败'),
    )

    kind = models.IntegerField(default=TYPE_ANONYMOUS, choices=TYPE_CHOICES, verbose_name="代理类型")
    user = models.CharField(default='', blank=True, max_length=100)
    password = models.CharField(default='', blank=True, max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=80)
    address = models.CharField(default='', blank=True, max_length=100, verbose_name="地理位置")
    speed = models.IntegerField(default=0, verbose_name="连接速度(ms)")
    status = models.IntegerField(default=STATUS_NEW, choices=STATUS_CHOICES, verbose_name="状态")
    retry = models.IntegerField(default=0, verbose_name="尝试次数")

    class Meta:
        verbose_name_plural = "5 访问代理"