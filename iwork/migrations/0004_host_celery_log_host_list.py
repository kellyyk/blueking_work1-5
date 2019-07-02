# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0003_auto_20190513_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host_Celery_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biz', models.CharField(max_length=128, verbose_name='bk_biz_id')),
                ('ip', models.CharField(unique=True, max_length=128, verbose_name='IP\u5730\u5740')),
                ('os', models.CharField(max_length=128, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('diskpath', models.CharField(max_length=128, verbose_name='\u5e38\u7528\u78c1\u76d8\u76ee\u5f55')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('occupy', models.CharField(max_length=128, verbose_name='\u5360\u7528\u7a7a\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Host_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biz', models.CharField(max_length=128, verbose_name='bk_biz_id')),
                ('ip', models.CharField(unique=True, max_length=128, verbose_name='IP\u5730\u5740')),
                ('os', models.CharField(max_length=128, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('diskpath', models.CharField(max_length=128, verbose_name='\u5e38\u7528\u78c1\u76d8\u76ee\u5f55')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(unique=True, max_length=128, verbose_name='\u72b6\u6001')),
            ],
        ),
    ]
