# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seed',
            name='list_rules',
            field=models.TextField(default='', verbose_name=b'\xe8\x8e\xb7\xe5\x8f\x96\xe5\x88\x97\xe8\xa1\xa8\xe9\xa1\xb9\xe7\x9a\x84\xe8\xa7\x84\xe5\x88\x99'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seed',
            name='next_url_rules',
            field=models.TextField(verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe9\xa1\xb5\xe7\xb4\xa2\xe5\xbc\x95\xe7\x9a\x84\xe8\xa7\x84\xe5\x88\x99\xe5\x88\x97\xe8\xa1\xa8'),
        ),
    ]
