# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cores', '0003_auto_20160131_2226'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Proxy',
        ),
        migrations.AlterModelOptions(
            name='detailrule',
            options={'verbose_name_plural': '3 \u8be6\u60c5\u9875\u722c\u53d6\u89c4\u5219'},
        ),
        migrations.AlterModelOptions(
            name='indexrule',
            options={'verbose_name_plural': '2 \u7d22\u5f15\u548c\u5217\u8868\u89c4\u5219'},
        ),
        migrations.AlterField(
            model_name='indexrule',
            name='site',
            field=models.ForeignKey(to='configs.Site'),
        ),
        migrations.DeleteModel(
            name='Site',
        ),
    ]
