# -*- coding: utf-8 -*-
"""
celery 任务

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
from celery.schedules import crontab
from celery.task import periodic_task
from djcelery.models import PeriodicTask, CrontabSchedule
from common.log import logger

def add_peroid_task(task, name=None, minute='*', hour='*',day_of_week='*', day_of_month='*',month_of_year='*', args="[]", kwargs="{}"):
    """
    @summary: 添加一个周期任务
    @param task: 该task任务的模块路径名, 例如celery_sample.crontab_task
    @param name: 用户定义的任务名称, 具有唯一性
    @note: PeriodicTask有很多参数可以设置，这里只提供简单常用的
    """
    cron_param = {
        'minute': minute,
        'hour': hour,
        'day_of_week': day_of_week,
        'day_of_month': day_of_month,
        'month_of_year': month_of_year
    }
    if not name:
        name = task
    try:
        cron_schedule = CrontabSchedule.objects.get(**cron_param)
    except CrontabSchedule.DoesNotExist:
        cron_schedule = CrontabSchedule(**cron_param)
        cron_schedule.save()
    try:
        PeriodicTask.objects.create(
            name=name,
            task=task,
            crontab=cron_schedule,
            args=args,
            kwargs=kwargs,
        )
        logger.info(u"建立任务：%s" % name)
    except Exception, e:
        return False, '%s' % e
    else:
        return True, ''

def del_peroid_task_by_id(name):
    """
    @summary: 根据周期任务的id删除该任务
    @param task_id: PeriodicTask库中记录的id
    """
    try:
        PeriodicTask.objects.filter(name=name).delete()
        logger.info(u"删除任务：%s" % name)
        return True, ''
    except Exception, e:
        return False, '%s' % e
