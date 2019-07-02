# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0006_peroidtaskrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host_celery_log',
            name='ip',
            field=models.CharField(max_length=128, verbose_name='IP\u5730\u5740'),
        ),
    ]
