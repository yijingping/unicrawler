# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0003_auto_20160129_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexrule',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'\xe6\x9d\xa5\xe6\xba\x90'),
        ),
        migrations.AlterField(
            model_name='indexrule',
            name='site',
            field=models.ForeignKey(to='cores.Site'),
        ),
    ]
