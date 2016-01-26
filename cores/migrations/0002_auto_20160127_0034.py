# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexrule',
            name='status',
            field=models.IntegerField(default=1, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe7\x94\xa8', choices=[(1, b'\xe5\x90\xaf\xe7\x94\xa8'), (2, b'\xe7\xa6\x81\xe7\x94\xa8')]),
        ),
        migrations.AlterField(
            model_name='indexrule',
            name='next_url_rules',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe9\xa1\xb5\xe7\xb4\xa2\xe5\xbc\x95\xe7\x9a\x84\xe8\xa7\x84\xe5\x88\x99\xe5\x88\x97\xe8\xa1\xa8', blank=True),
        ),
    ]
