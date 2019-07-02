# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.conf.urls import patterns
from iwork.views import DiskInfos,Get_Disk

urlpatterns = patterns(
    'iwork.views',
    (r'^$', 'home'),
    (r'^textjob/$','textjob'),
    (r'^diskinfo/$', DiskInfos.as_view()),
    (r'^get_disk/$', Get_Disk.as_view()),
    (r'^get_biz_list/$', 'get_biz_list'),
    (r'^get_ip_by_bizid/$', 'get_ip_by_bizid'),
    (r'^celery_task/$', 'celery_task'),
    (r'^select_celery_log/$', 'select_celery_log')
)
