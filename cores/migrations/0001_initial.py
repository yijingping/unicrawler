# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe8\xa7\x84\xe5\x88\x99')),
            ],
            options={
                'verbose_name_plural': '\u8be6\u60c5\u9875\u722c\u53d6\u89c4\u5219',
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
                ('desc', models.TextField(verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b')),
                ('data', models.TextField(verbose_name=b'\xe8\xaf\xa6\xe7\xbb\x86\xe7\xbb\x93\xe6\x9e\x84')),
                ('weight', models.IntegerField(default=0, verbose_name=b'\xe6\x9d\x83\xe9\x87\x8d')),
            ],
            options={
                'verbose_name_plural': '\u6a21\u677f',
            },
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe6\x9d\xa5\xe6\xba\x90\xe7\xbd\x91\xe7\xab\x99\xe5\x90\x8d\xe7\xa7\xb0')),
                ('site', models.CharField(max_length=100, verbose_name=b'\xe6\x9d\xa5\xe6\xba\x90\xe7\xbd\x91\xe7\xab\x99\xe5\x9f\x9f\xe5\x90\x8d')),
                ('url', models.CharField(max_length=100, verbose_name=b'\xe7\xb4\xa2\xe5\xbc\x95url')),
                ('next_url_rules', models.CharField(max_length=100, verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe9\xa1\xb5\xe7\xb4\xa2\xe5\xbc\x95\xe7\x9a\x84\xe8\xa7\x84\xe5\x88\x99\xe5\x88\x97\xe8\xa1\xa8')),
                ('frequency', models.IntegerField(default=60, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87,\xe5\x8d\x95\xe4\xbd\x8d\xe7\xa7\x92')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('next_crawl_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('schema', models.ForeignKey(to='cores.Schema')),
            ],
            options={
                'verbose_name_plural': '\u6765\u6e90\u79cd\u5b50',
            },
        ),
        migrations.AddField(
            model_name='rule',
            name='seed',
            field=models.ForeignKey(to='cores.Seed'),
        ),
    ]
