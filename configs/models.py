# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
from django.db import models


def get_default_uniqueid():
    return str(long(time.time() * 1000000))


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
        verbose_name_plural = "1 站点配置"


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
    uniqueid = models.CharField(unique=True, max_length=100, default=get_default_uniqueid, verbose_name='代理参数的md5值')
    url = models.CharField(max_length=500, default='', verbose_name='url')
    kind = models.IntegerField(default=TYPE_ANONYMOUS, choices=TYPE_CHOICES, verbose_name="代理类型")
    user = models.CharField(default='', blank=True, max_length=100)
    password = models.CharField(default='', blank=True, max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=80)
    address = models.CharField(default='', blank=True, max_length=100, verbose_name="地理位置")
    speed = models.IntegerField(default=0, verbose_name="连接速度(ms)")
    status = models.IntegerField(default=STATUS_NEW, choices=STATUS_CHOICES, verbose_name="状态")
    retry = models.IntegerField(default=0, verbose_name="尝试次数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name_plural = "2 访问代理"

