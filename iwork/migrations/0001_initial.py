# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiskInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=128, verbose_name='IP\u5730\u5740')),
                ('os', models.IntegerField(verbose_name='\u7cfb\u7edf\u7248\u672c', choices=[(1, 'linux'), (2, 'windows')])),
                ('diskpath', models.CharField(unique=True, max_length=128, verbose_name='\u5e38\u7528\u78c1\u76d8\u76ee\u5f55')),
            ],
            options={
                'verbose_name_plural': '\u78c1\u76d8\u4fe1\u606f\u8868',
            },
        ),
    ]
