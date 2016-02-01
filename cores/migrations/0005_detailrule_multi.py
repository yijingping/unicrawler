# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0004_auto_20160201_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailrule',
            name='multi',
            field=jsonfield.fields.JSONField(verbose_name=b'\xe5\xa4\x9a\xe8\xaf\xa6\xe6\x83\x85\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
    ]
