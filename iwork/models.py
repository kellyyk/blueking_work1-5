# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class DiskInfo(models.Model):
    os_type = (
        (1, u'linux'),
        (2, u'windows')
    )
    ip = models.CharField(u"IP地址", max_length=128, unique=True)
    os = models.CharField(u'系统版本', max_length=128,choices=os_type)
    diskpath = models.CharField(u"常用磁盘目录", max_length=128)

    class Meta:
        verbose_name_plural = "磁盘信息表"

class Host_List(models.Model):
    status_type = {
        "1": u"运行",
        "2": u"停止"
    }

    biz = models.CharField(u"bk_biz_id", max_length=128)
    ip = models.CharField(u"IP地址", max_length=128, unique=True)
    os = models.CharField(u'系统版本', max_length=128)
    diskpath = models.CharField(u"常用磁盘目录", max_length=128)
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(u"状态", max_length=128)

    def to_dict(self):
        return {
            "id": self.id,
            "biz": self.biz,
            "ip": self.ip,
            "os": self.os,
            "diskpath": self.diskpath,
            "star_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status_type[self.status]
        }

    def all_list(self):
        return [{
            "id": self.id,
            "biz": self.biz,
            "ip": self.ip,
            "os": self.os,
            "diskpath": self.diskpath,
            "star_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status_type[self.status]
        }]

class Host_Celery_log(models.Model):
    biz = models.CharField(u"bk_biz_id", max_length=128)
    ip = models.CharField(u"IP地址", max_length=128)
    os = models.CharField(u'系统版本', max_length=128)
    diskpath = models.CharField(u"常用磁盘目录", max_length=128)
    start_time = models.DateTimeField(auto_now_add=True)
    occupy = models.CharField(u"占用空间", max_length=128)

    def to_dict(self):
        return {
            "id": self.id,
            "biz": self.biz,
            "ip": self.ip,
            "os": self.os,
            "diskpath": self.diskpath,
            "star_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "occupy": self.occupy
        }

class PeroidTaskRecord(models.Model):
    """
    周期任务纪录
    """
    excute_param = models.TextField(u"任务执行参数")
    excute_result = models.TextField(u"任务执行结果")
    excute_time = models.DateTimeField(u"任务执行时间", auto_now_add=True)
    periodic_task_id = models.IntegerField(u"周期性任务的id", default=0)

    def __unicode__(self):
        return '%s--%s--%s' % (self.periodic_task_id, self.excute_param, self.excute_time)

    class Meta:
        verbose_name = u"周期性任务执行记录"
        verbose_name_plural = u"周期性任务执行记录"
        ordering = ['-excute_time']