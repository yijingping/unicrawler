# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0006_detailrule_fresh_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailrule',
            name='multi_unique',
            field=jsonfield.fields.JSONField(verbose_name=b'\xe5\xa4\x9a\xe8\xaf\xa6\xe6\x83\x85\xe5\x94\xaf\xe4\xb8\x80\xe9\x94\xae\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
    ]
