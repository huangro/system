#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse
from core.models import *
import json
import time

def heartbeat(request):
    """
    :param request:
    :return:
    """
    if request.POST:
        params = request.POST
    else:
        params = request.GET

    if params.get('secret_key', None) is None:
        result = {"code":"-1", "msg":"secret_key is required"}
        return HttpResponse(json.dumps(result), content_type='application/json')
    if params.get('slot', None) is None:
        result = {"code":"-1", "msg":"slot is required"}
        return HttpResponse(json.dumps(result), content_type='application/json')
    service_platform = ServicePlatform()
    sp = service_platform.get_service_platform_by_secret_key_dict(params.get('secret_key'))
    if sp is None:
        result = {"code":"-2", "msg":"secret_key is not exists"}
        return HttpResponse(json.dumps(result), content_type='application/json')
    control_point = ControlPoint()
    cp = control_point.get_control_point_by_slot(sp.get('id'), params.get('slot'))
    if cp is None:
        result = {"code":"-2", "msg":"slot is not exists"}
        return HttpResponse(json.dumps(result), content_type='application/json')
    heart_beat = HeartBeat()
    heart_beat.save_heartbeat(cp.get('id'), params.get('slot'), params.get('content', ''), request.META['REMOTE_ADDR'], params.get('has_error', False), time.strftime("%Y-%m-%d %H:%M:%S"))
    result = {"code":"200", "msg":"success"}
    return HttpResponse(json.dumps(result), content_type='application/json')


