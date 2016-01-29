# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0004_auto_20160129_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='use_browser',
        ),
        migrations.RemoveField(
            model_name='site',
            name='use_proxy',
        ),
        migrations.AddField(
            model_name='site',
            name='browser',
            field=models.IntegerField(default=1, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe5\xa3\xb3'),
        ),
        migrations.AddField(
            model_name='site',
            name='proxy',
            field=models.IntegerField(default=1, verbose_name=b'\xe4\xbb\xa3\xe7\x90\x86'),
        ),
        migrations.AlterField(
            model_name='site',
            name='limit_speed',
            field=models.IntegerField(default=100, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe9\x97\xb4\xe9\x9a\x94(\xe6\xaf\xab\xe7\xa7\x92)'),
        ),
    ]
