# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from common.mymako import render_mako_context,render_json
from django.views.generic import View
from models import DiskInfo, Host_Celery_log, Host_List
from account.accounts import Account
from blueking.component.shortcuts import get_client_by_request
from iwork.service import get_all_host_list,get_host_ostype
import json
from djcelery.models import PeriodicTask, CrontabSchedule
from iwork.celery_tasks import add_peroid_task,del_peroid_task_by_id
from iwork.service import start_job

def home(request):
    """
    首页 输出hello world
    :param request:
    :return:
    """
    return render_mako_context(request,'iwork/home.html')

def textjob(request):
    data = request.POST.get('data')
    data = data.replace('&nbsp;', ' ')
    print data
    if data == "Hello Blueking":
        out = "Congratulation！"
        data = {
            "result": True,
            'message': out
        }
    else:
        out = u"输入错误"
        data = {
            "result": False,
            'message': out
        }
    return render_json(data)

class DiskInfos(View):
    def dispatch(self, request, *args, **kwargs):
        return super(DiskInfos, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        磁盘信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        account = Account()
        username = account.get_username(request)
        if username == 'admin':
            result = True
        else:
            result = False
        diskdata = DiskInfo.objects.all().values()
        diskdata = list(diskdata)
        ostype = [
            {'id': 1, 'text': 'liunx'},
            {'id': 2, 'text': 'windows'}
        ]
        return render_mako_context(request, 'iwork/diskinfo.html',{'result':result, 'diskdata':json.dumps(diskdata), 'ostype': ostype})

    def post(self, request, *args, **kwargs):
        """
        post 方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ipaddr = request.POST.get('ipaddr')
        os = request.POST.get('ostype')
        diskpath = request.POST.get('diskpath')
        print os
        try:
            DiskInfo.objects.create(ip=ipaddr, os=os, diskpath=diskpath)
            data = DiskInfo.objects.all().values()
            data = list(data)
        except Exception as e:
            print e
            return render_json({'result': False,'data':[], 'message': u'添加信息出错'})

        return render_json({'result': True, 'data': data, 'message': u'添加信息成功'})

class Get_Disk(View):
    def dispatch(self, request, *args, **kwargs):
        return super(Get_Disk, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        设置后台任务及查询接口
        :param request:
        :return:
        """
        try:
            host_lists = Host_List.objects.all().values()
            host_list = []
            for h in host_lists:
                obj = {}
                obj['id'] = h['id']
                obj['biz'] = h['biz']
                obj['ip'] = h['ip']
                obj['os'] = h['os']
                obj['diskpath'] = h['diskpath']
                obj['star_time'] = h['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
                obj['status'] = h['status']
                host_list.append(obj)
        except Exception as e:
            print e
            host_list = []
        return render_mako_context(request, 'iwork/get_disk.html',{"host_list": json.dumps(host_list)})

    def post(self,request):
        biz_id = request.POST.get('biz_id')
        ip = request.POST.get('ip')
        disk = request.POST.get('disk')
        client = get_client_by_request(request)
        os_type = get_host_ostype(client, biz_id, ip)
        try:
            Host_List.objects.create(
                biz=biz_id,
                ip= ip,
                diskpath= disk,
                os= os_type,
                status= 2
            )
            host_lists = Host_List.objects.all().values()
            host_list = []
            for h in host_lists:
                obj = {}
                obj['id'] = h['id']
                obj['biz'] = h['biz']
                obj['ip'] = h['ip']
                obj['os'] = h['os']
                obj['diskpath'] = h['diskpath']
                obj['star_time'] = h['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
                obj['status'] = h['status']
                host_list.append(obj)
            data = {
                "result": True,
                "data": host_list,
                "message": u"新建任务成功"
            }
        except Exception as e:
            print e
            data = {
                "result": False,
                "data": [],
                "message": u"新建任务失败"
            }
            return render_json(data)
        return render_json(data)

def get_biz_list(request):
    """
    获取所有业务
    """
    biz_list = []
    client = get_client_by_request(request)
    kwargs = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    resp = client.cc.search_business(**kwargs)

    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            biz_list.append({
                'name': _d.get('bk_biz_name'),
                'id': _d.get('bk_biz_id'),
            })

    result = {'result': resp.get('result'), 'data': biz_list}
    return render_json(result)


def get_ip_by_bizid(request):
    """
    获取业务下IP
    """
    biz_id = int(request.GET.get('biz_id'))
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': biz_id,
              'condition': [
                  {
                      'bk_obj_id': 'biz',
                      'fields': ['bk_biz_id'],
                      'condition': [
                          {
                              'field': 'bk_biz_id',
                              'operator': '$eq',
                              'value': biz_id
                          }
                      ]
                  }
              ]
              }
    resp = client.cc.search_host(**kwargs)

    ip_list = []
    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            _hostinfo = _d.get('host', {})
            if _hostinfo.get('bk_host_innerip') not in ip_list:
                ip_list.append(_hostinfo.get('bk_host_innerip'))

    ip_all = [{'ip': _ip} for _ip in ip_list]
    result = {'result': resp.get('result'), 'data': ip_all}
    return render_json(result)


def celery_task(request):
    """
    控制celery_task
    :param request:
    :return:
    """
    user = request.user.username
    id = request.POST.get('id')
    type = request.POST.get('type')
    host_info = Host_List.objects.get(id=id).to_dict()
    ip = host_info.get('ip')
    try:
        id = PeriodicTask.objects.get(name=ip)
    except Exception as e:
        id = False
    if type == 'star':
        if id:
            data = {
                "result": False,
                "message": u"后台任务已存在"
            }
            render_json(data)
        else:
            args = json.dumps([user])
            kwargs = json.dumps(host_info)
            res, msg = add_peroid_task('iwork.service.start_job',ip,'*/60','*','*','*','*',args,kwargs)
            if res:
                Host_List.objects.filter(ip=ip).update(status=1)
                return render_json({"result": res,"message": u"任务创建成功"})
            else:
                return render_json({"result": res, "message": msg})
    elif type == 'stop':
        if id:
            res, msg = del_peroid_task_by_id(ip)
            if res:
                Host_List.objects.filter(ip=ip).update(status=2)
                return render_json({"result": res,"message": u"任务删除成功"})
            else:
                return render_json({"result": res, "message": msg})

def select_celery_log(request):
    ip = request.POST.get('ip')
    try:
        rqt = Host_Celery_log.objects.filter(ip=ip).values()
        if len(rqt) > 0:
            host_list = []
            for h in rqt:
                obj = {}
                obj['biz'] = h['biz']
                obj['ip'] = h['ip']
                obj['os'] = h['os']
                obj['diskpath'] = h['diskpath']
                obj['star_time'] = h['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
                obj['occupy'] = h['occupy']
                host_list.append(obj)
            ret = {
                'result': True,
                'data': host_list,
                'message': 'ok'
            }
            return render_json(ret)
        else:
            ret = {
                'result': False,
                'data': [],
                'message': u'没有数据！！'
            }
            return render_json(ret)
    except Exception as e:
        print e
        ret = {
            'result': False,
            'data': [],
            'message': u'出错啦！！'
        }
        return render_json(ret)