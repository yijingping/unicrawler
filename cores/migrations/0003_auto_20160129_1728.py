# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0002_auto_20160127_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe7\xab\x99\xe7\x82\xb9\xe5\x90\x8d\xe7\xa7\xb0')),
                ('domain', models.CharField(unique=True, max_length=100, verbose_name=b'\xe7\xab\x99\xe7\x82\xb9\xe5\x9f\x9f\xe5\x90\x8d')),
                ('use_proxy', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xbd\xbf\xe7\x94\xa8\xe4\xbb\xa3\xe7\x90\x86')),
                ('use_browser', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xbd\xbf\xe7\x94\xa8\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8\xe5\xa3\xb3')),
                ('limit_speed', models.IntegerField(default=1, verbose_name=b'\xe8\xae\xbf\xe9\x97\xae\xe9\x97\xb4\xe9\x9a\x94(\xe6\xaf\xab\xe7\xa7\x92)')),
                ('status', models.IntegerField(default=1, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe7\x94\xa8', choices=[(1, b'\xe5\x90\xaf\xe7\x94\xa8'), (2, b'\xe7\xa6\x81\xe7\x94\xa8')])),
            ],
            options={
                'verbose_name_plural': '\u7ad9\u70b9\u914d\u7f6e',
            },
        ),
        migrations.AlterField(
            model_name='indexrule',
            name='next_crawl_time',
            field=models.DateTimeField(verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='seed',
            name='data',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe5\xad\x98\xe5\x82\xa8\xe6\x95\xb0\xe6\x8d\xae\xe9\x85\x8d\xe7\xbd\xae', blank=True),
        ),
    ]
