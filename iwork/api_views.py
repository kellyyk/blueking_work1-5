# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from common.mymako import render_mako_context,render_json
from blueking.component.shortcuts import get_client_by_user
from iwork.service import api_start_job
from account.decorators import login_exempt

@login_exempt
def get_host_capacity(request):
    biz = request.GET.get('bk_biz_id', 0)
    ip = request.GET.get('ip', '')
    disk = request.GET.get('disk', '')
    ret = {
        "result": False,
        "message": '',
        "data": []
    }
    if biz == 0:
        ret['message'] = u'bk_biz_id不正确'
        return render_json(ret)
    if ip == '':
        ret['message'] = u'ip不正确'
        return render_json(ret)
    print disk
    disks = ['/','C:','D:','E:','F:']
    if disk not in disks:
        ret['message'] = u'分区不正确'
        return render_json(ret)

    kwargs = {
        'ip': ip,
        'biz': biz,
        'diskpath':disk
    }
    rqt = api_start_job('admin',kwargs)
    ret['result'] = True
    ret['message'] = u'api调用成功'
    ret['data'] = rqt
    return render_json(ret)