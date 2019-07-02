# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0004_host_celery_log_host_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host_list',
            name='status',
            field=models.CharField(max_length=128, verbose_name='\u72b6\u6001'),
        ),
    ]
