# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scheduler', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\xaa\xe6\x89\xa7\xe8\xa1\x8c\xe7\x9a\x84\xe8\xae\xa1\xe5\x88\x92\xe6\x95\xb0')),
                ('downloader', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\xaa\xe4\xb8\x8b\xe8\xbd\xbd\xe7\x9a\x84url\xe6\x95\xb0')),
                ('extractor', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\xaa\xe6\x8a\xbd\xe5\x8f\x96\xe7\x9a\x84url\xe6\x95\xb0')),
                ('processor', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\xaa\xe5\x85\xa5\xe5\xba\x93\xe7\x9a\x84\xe8\xae\xb0\xe5\xbd\x95\xe6\x95\xb0')),
                ('create_time', models.DateTimeField(unique=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '1 \u670d\u52a1\u961f\u5217\u79ef\u538b',
            },
        ),
    ]
