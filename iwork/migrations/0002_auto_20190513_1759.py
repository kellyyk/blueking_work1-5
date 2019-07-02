# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diskinfo',
            name='diskpath',
            field=models.CharField(max_length=128, verbose_name='\u5e38\u7528\u78c1\u76d8\u76ee\u5f55'),
        ),
    ]
