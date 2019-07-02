# -*- coding: utf-8 -*-
import time, datetime
from blueking.component.shortcuts import get_client_by_request,get_client_by_user
import base64
from iwork.models import Host_Celery_log
from common.log import logger
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

def get_all_host_list(request):
    client = get_client_by_request(request)
    ret = client.cc.search_host(bk_biz_id=4)
    if ret['result']:
        count = 1
        data = []
        for item in ret['data']['info']:
            host = {}
            host['id'] = count
            host['text'] = str(item['host']['bk_host_innerip'])
            data.append(host)
            count = count + 1
    return data

def get_host_ostype(client, biz_id, ip):
    kwargs = {
        "bk_biz_id": biz_id,
        "ip": {
            "data": [ip],
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": ["bk_os_type"],
                "condition": []
            }]
    }
    rqt = client.cc.search_host(**kwargs)
    if rqt.get('result'):
        info = rqt.get('data',{}).get('info',{})
        print info
        os_type = info[0]['host']['bk_os_name']
        print os_type
        return os_type

@task()
def start_job(*args, **kwargs):
    user = args[0]
    logger.info(u"接受到的消息：%s  %s" % (user,kwargs))
    os = str(kwargs.get('os'))
    ip = kwargs.get('ip')
    biz = kwargs.get('biz')
    diskpath = kwargs.get('diskpath')

    cmd = "info=`df -h /|grep / |awk -F ' ' '{print $4}'`&&echo $info"
    script_type = 1
    account = "root"
    if 'win' in os:
        cmd = "import psutil" \
              "disk = psutil.disk_usage(r'c:')" \
              "print('%s%' % disk[3])"
        script_type = 4
        account = "Administrator"

    kwargs = {
        "bk_biz_id": biz,
        "script_content": base64.b64encode(cmd),
        "account": account,
        "script_type": script_type,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": ip
            }]
    }
    logger.info(u"参数：%s" % kwargs)
    client = get_client_by_user('admin')
    logger.info(u"执行client返回：%s" % client.__dict__)
    ret = client.job.fast_execute_script(**kwargs)
    logger.info(u"执行脚本返回：%s" % ret)
    if ret.get('result'):
        job_instance_id = ret.get('data').get('job_instance_id')

    poll_result = poll_job_task(client, biz, job_instance_id)

    # 查询日志
    resp = client.job.get_job_instance_log(job_instance_id=job_instance_id, bk_biz_id=biz)
    status = resp['data'][0]['status']
    result = True if status == 3 else False
    ip_logs = resp['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
    logger.info(u"执行脚本返回：%s" % ip_logs)
    Host_Celery_log.objects.create(biz=biz,ip=ip,os=os,diskpath=diskpath,occupy=ip_logs)

def poll_job_task(client, biz_id, job_instance_id):
    """true/false/timeout"""

    count = 0

    res = client.job.get_job_instance_status(job_instance_id=job_instance_id, bk_biz_id=biz_id)

    while res.get('data', {}).get('is_finished') is False and count < 30:
        res = client.job.get_job_instance_status(job_instance_id=job_instance_id, bk_biz_id=biz_id)
        count += 1
        time.sleep(3)

    return res

def api_start_job(user, kwargs):
    client = get_client_by_user(user)
    logger.info(u"接受到的消息：%s  %s" % (user,kwargs))
    biz = kwargs.get('biz')
    ip = kwargs.get('ip')
    os = get_host_ostype(client,biz,ip)
    diskpath = kwargs.get('diskpath')

    cmd = "info=`df -h /|grep / |awk -F ' ' '{print $4}'`&&echo $info"
    script_type = 1
    account = "root"
    if 'win' in os:
        cmd = "import psutil" \
              "disk = psutil.disk_usage(r'c:')" \
              "print('%s%' % disk[3])"
        script_type = 4
        account = "Administrator"

    kwargs = {
        "bk_biz_id": biz,
        "script_content": base64.b64encode(cmd),
        "account": account,
        "script_type": script_type,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": ip
            }]
    }
    logger.info(u"参数：%s" % kwargs)
    ret = client.job.fast_execute_script(**kwargs)
    logger.info(u"执行脚本返回：%s" % ret)
    if ret.get('result'):
        job_instance_id = ret.get('data').get('job_instance_id')

    poll_result = poll_job_task(client, biz, job_instance_id)

    # 查询日志
    resp = client.job.get_job_instance_log(job_instance_id=job_instance_id, bk_biz_id=biz)
    status = resp['data'][0]['status']
    result = True if status == 3 else False
    ip_logs = resp['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
    logger.info(u"执行脚本返回：%s" % ip_logs)
    data = {
        'ip': ip,
        'bk_biz_id': biz,
        'disk': diskpath,
        'capacity': ip_logs,
        'datatime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return data