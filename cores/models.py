# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import collections
from django.db import models
from jsonfield import JSONField
from configs.models import Site


class Seed(models.Model):
    STATUS_ENABLE = 1
    STATUS_DISABLE = 2
    STATUS_CHOICES = (
        (STATUS_ENABLE, '启用'),
        (STATUS_DISABLE, '禁用')
    )
    name = models.CharField(max_length=100, verbose_name='模板名称')
    desc = models.TextField(verbose_name='简介')
    data = JSONField(verbose_name='存储数据配置', load_kwargs={'object_pairs_hook': collections.OrderedDict},
                     blank=True, default=[])
    weight = models.IntegerField(default=0, verbose_name='权重')
    status = models.IntegerField(default=STATUS_ENABLE, choices=STATUS_CHOICES, verbose_name="是否启用")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1 种子"


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
    url = JSONField(verbose_name='索引url列表', load_kwargs={'object_pairs_hook': collections.OrderedDict})
    list_rules = JSONField(verbose_name='获取列表项的规则', load_kwargs={'object_pairs_hook': collections.OrderedDict},
                           blank=True, default=[])
    next_url_rules = JSONField(verbose_name='下一页索引的规则列表',
                               load_kwargs={'object_pairs_hook': collections.OrderedDict}, blank=True, default=[])
    frequency = models.IntegerField(default=60, verbose_name='爬取频率,单位秒')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    next_crawl_time = models.DateTimeField(verbose_name='下次爬取时间')
    fresh_pages = models.IntegerField(default=2, verbose_name='爬取页面数')
    status = models.IntegerField(default=STATUS_ENABLE, choices=STATUS_CHOICES, verbose_name="是否启用")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "2 索引和列表规则"


class DetailRule(models.Model):
    index_rule = models.ForeignKey(IndexRule)
    data = JSONField(verbose_name='详情页规则', load_kwargs={'object_pairs_hook': collections.OrderedDict})
    exclude = JSONField(verbose_name='排除规则', load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        blank=True, default=[])
    multi = JSONField(verbose_name='多详情规则', load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        blank=True, default=[])
    multi_unique = JSONField(verbose_name='多详情唯一键规则', load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        blank=True, default=[])
    fresh_time = models.IntegerField(default=2592000, verbose_name='新鲜度维持时间(秒),默认一个月')

    def __unicode__(self):
        return '%s, %s' % (self.index_rule.name, self.index_rule.url)

    class Meta:
        verbose_name_plural = "3 详情页爬取规则"

