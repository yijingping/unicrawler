# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0005_detailrule_multi'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailrule',
            name='fresh_time',
            field=models.IntegerField(default=2592000, verbose_name=b'\xe6\x96\xb0\xe9\xb2\x9c\xe5\xba\xa6\xe7\xbb\xb4\xe6\x8c\x81\xe6\x97\xb6\xe9\x97\xb4(\xe7\xa7\x92),\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9c\x88'),
        ),
    ]
