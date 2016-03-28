# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
import requests
import platform
from random import sample
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from django.conf import settings

import logging
logger = logging.getLogger()
CRAWLER_CONFIG = settings.CRAWLER_CONFIG


class RequestsDownloaderBackend(object):
    """
    使用requests直接访问
    """
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        self.proxy = proxy

    def format_proxies(self):
        p = self.proxy
        if self.proxy:
            if p.user:
                data = 'http://%s:%s@%s:%s' % (p.user, p.password, p.host, p.port)
            else:
                data = 'http://%s:%s' % (p.host, p.port)
            return {
                "http": data
            }
        else:
            return None

    def download(self, url):
        header = sample(self.headers, 1)[0]
        proxies = self.format_proxies()
        #print url
        if isinstance(url, basestring):
            rsp = requests.get(url, headers=header, proxies=proxies)
            rsp.close()
            rsp.encoding = rsp.apparent_encoding
            return rsp.text
        elif isinstance(url, dict):
            link, method, data, data_type = url.get('url'), url.get('method'), url.get('data'), url.get('dataType')
            req = {'GET': requests.get, 'POST': requests.post}.get(method)
            if method == 'GET':
                rsp = req(link, params=data, headers=header, proxies=proxies)
            elif method == 'POST':
                rsp = req(link, data=data, headers=header, proxies=proxies)
            rsp.close()
            rsp.encoding = rsp.apparent_encoding
            if data_type == 'json':
                return rsp.json()
            else:
                return rsp.text


class SeleniumDownloaderBackend(object):
    """
    使用Selenium模拟浏览器访问
    """
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
        }
    ]

    def __init__(self, proxy=None):
        # 设置代理
        self.proxy = proxy

    def __enter__(self):
        # 打开界面
        self.display = self.get_display()
        #  打开浏览器
        self.browser = self.get_browser(self.proxy)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭浏览器
        try:
            if self.browser:
                self.browser.delete_all_cookies()
                self.browser.quit()
        except Exception as e:
            logging.exception(e)
        # 关闭界面
        try:
            # 关闭浏览器,关闭窗口
            self.display and self.display.stop()
        except Exception as e:
            logging.exception(e)

    def get_display(self):
        if platform.system() != 'Darwin':
            # 不是mac系统, 启动窗口
            display = Display(visible=0, size=(1024, 768))
            display.start()
        else:
            display = None
        return display

    def get_browser(self, proxy):
        # 启动浏览器
        # 禁止加载image
        firefox_profile = webdriver.FirefoxProfile()
        #firefox_profile.set_preference('permissions.default.stylesheet', 2)
        #firefox_profile.set_preference('permissions.default.image', 2)
        #firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # 代理
        if proxy and proxy.is_valid():
            myProxy = '%s:%s' % (proxy.host, proxy.port)
            ff_proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': myProxy,
                'ftpProxy': myProxy,
                'sslProxy': myProxy,
            'noProxy':''})

            browser = webdriver.Firefox(firefox_profile=firefox_profile, proxy=ff_proxy)
        else:
            browser = webdriver.Firefox(firefox_profile=firefox_profile)

        return browser

    def download(self, url):
        browser = self.browser
        # 访问首页, 输入wchatid, 点击查询
        browser.get(url)
        time.sleep(3)
        js = """
            return document.documentElement.innerHTML;
        """
        body = browser.execute_script(js)
        return body


class BrowserDownloaderBackend(object):
    def download(self):
        pass
