# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0002_auto_20160201_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='url',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x9a\x84url'),
        ),
    ]
