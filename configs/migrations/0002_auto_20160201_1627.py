# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import configs.models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='create_time',
            field=models.DateTimeField(default=None, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proxy',
            name='uniqueid',
            field=models.CharField(default=configs.models.get_default_uniqueid, unique=True, max_length=100, verbose_name=b'url\xe7\x9a\x84md5\xe5\x80\xbc'),
        ),
        migrations.AddField(
            model_name='proxy',
            name='update_time',
            field=models.DateTimeField(default=None, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True),
            preserve_default=False,
        ),
    ]
