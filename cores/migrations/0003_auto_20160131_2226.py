# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0002_detailrule_exclude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailrule',
            name='exclude',
            field=jsonfield.fields.JSONField(default=[], verbose_name=b'\xe6\x8e\x92\xe9\x99\xa4\xe8\xa7\x84\xe5\x88\x99', blank=True),
        ),
    ]
