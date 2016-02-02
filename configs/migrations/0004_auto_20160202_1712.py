# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import configs.models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0003_proxy_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='uniqueid',
            field=models.CharField(default=configs.models.get_default_uniqueid, unique=True, max_length=100, verbose_name=b'\xe4\xbb\xa3\xe7\x90\x86\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84md5\xe5\x80\xbc'),
        ),
        migrations.AlterField(
            model_name='proxy',
            name='url',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'url'),
        ),
    ]
