# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0007_detailrule_multi_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailrule',
            name='multi',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe5\xa4\x9a\xe8\xaf\xa6\xe6\x83\x85\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
        migrations.AlterField(
            model_name='detailrule',
            name='multi_unique',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe5\xa4\x9a\xe8\xaf\xa6\xe6\x83\x85\xe5\x94\xaf\xe4\xb8\x80\xe9\x94\xae\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
        migrations.AlterField(
            model_name='indexrule',
            name='list_rules',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe8\x8e\xb7\xe5\x8f\x96\xe5\x88\x97\xe8\xa1\xa8\xe9\xa1\xb9\xe7\x9a\x84\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
    ]
