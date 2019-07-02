# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0002_auto_20190513_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diskinfo',
            name='os',
            field=models.CharField(max_length=128, verbose_name='\u7cfb\u7edf\u7248\u672c', choices=[(1, 'linux'), (2, 'windows')]),
        ),
    ]
