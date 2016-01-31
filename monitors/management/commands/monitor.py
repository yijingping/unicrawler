# -*- coding: utf-8 -*-
__author__ = 'yijingping'
import time
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from monitors.models import Service
from cores.util import get_redis
from django.conf import settings
from cores.models import Seed, IndexRule

class Command(BaseCommand):
    help = '获取监控数据'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('action', choices=['service', 'stats'], help='选择要监控的服务类型')

    def handle(self, *args, **options):
        if options["action"] == 'service':
            self.monitor_service()

    def monitor_service(self):
        conf = settings.CRAWLER_CONFIG
        r = get_redis()
        now = datetime.now().replace(second=0, microsecond=0)
        pipe = r.pipeline()
        result = pipe.llen(conf['downloader']).llen(conf['extractor']).llen(conf['processor']).execute()
        scheduler = IndexRule.objects.filter(seed__status=Seed.STATUS_ENABLE, status=IndexRule.STATUS_ENABLE,
                                             next_crawl_time__lte=now).count()
        print result
        Service.objects.create(
            scheduler=scheduler,
            downloader=result[0],
            extractor=result[1],
            processor=result[2],
            create_time=now
        )

