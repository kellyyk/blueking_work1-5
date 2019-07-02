# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwork', '0005_auto_20190515_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeroidTaskRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('excute_param', models.TextField(verbose_name='\u4efb\u52a1\u6267\u884c\u53c2\u6570')),
                ('excute_result', models.TextField(verbose_name='\u4efb\u52a1\u6267\u884c\u7ed3\u679c')),
                ('excute_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4efb\u52a1\u6267\u884c\u65f6\u95f4')),
                ('periodic_task_id', models.IntegerField(default=0, verbose_name='\u5468\u671f\u6027\u4efb\u52a1\u7684id')),
            ],
            options={
                'ordering': ['-excute_time'],
                'verbose_name': '\u5468\u671f\u6027\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
                'verbose_name_plural': '\u5468\u671f\u6027\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
            },
        ),
    ]
