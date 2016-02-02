# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from abc import ABCMeta
from abc import abstractmethod
import requests
import oss2
from hashlib import md5
from django.conf import settings
import logging
logger = logging.getLogger()


OSS2_CONF = settings.OSS2_CONFIG
BUCKET = None


def get_bucket():
    global BUCKET
    if not BUCKET:
        auth = oss2.Auth(OSS2_CONF['ACCESS_KEY_ID'], OSS2_CONF['ACCESS_KEY_SECRET'])
        BUCKET = oss2.Bucket(auth, 'http://%s' % OSS2_CONF['BUCKET_DOMAIN'], OSS2_CONF['BUCKET_NAME'])

    return BUCKET


def download_to_oss(image_url):
    r = requests.get(image_url)
    r.close()
    key = OSS2_CONF["IMAGES_PATH"] + md5(r.content).hexdigest()
    bucket = get_bucket()
    bucket.put_object(key, r, headers={'Content-Type': r.headers.get('Content-Type')})
    return 'http://%s/%s' % (OSS2_CONF["IMAGES_DOMAIN"], key)


class BaseExtractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract(self):
        pass


class ImageExtractor(BaseExtractor):
    def __init__(self, data):
        """ data 是图片url,或者图片url的列表
        :param data:
        :return: 如果是url,返回新的url; 如果是列表,返回新的url列表
        """
        self.data = data

    def extract(self):
        d = self.data
        new_url = None
        if not d:
            return d
        elif isinstance(d, basestring):
            new_url = download_to_oss(d)
        elif isinstance(d, list):
            new_url = map(download_to_oss, d)

        return new_url


class XPathExtractor(BaseExtractor):
    def __init__(self, tree, rule):
        self.tree = tree
        self.rule = rule

    def extract(self):
        return self.tree.xpath(self.rule)


class PythonExtractor(BaseExtractor):
    def __init__(self, code, in_val):
        self.code = code
        self.in_val = in_val

    def extract(self):
        res = self.in_val
        g, l = {}, {"in_val": self.in_val}
        try:
            exec(self.code, g, l)
            res = l["out_val"]
        except Exception as e:
            logger.exception(e)
        finally:
            return res


