#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.conf import settings
from core.models import *
from utils.smail import SMail
import datetime

MAIL_INFO = settings.MAIL_INFO

def check_heartbeat_status():
    """
    :return:
    """
    service_platform = ServicePlatform()
    sps = service_platform.get_service_platform()
    for sp in sps:
        title = sp.title
        mail_list = sp.mail_list
        body = ''
        control_point = ControlPoint()
        cps = control_point.get_control_point_by_sid(sp.id)
        for cp in cps:
            heart_beat = HeartBeat()
            num = heart_beat.count_heartbeat(cp.get('id'), cp.get('interval', 300))
            if num == 0:
                if body == '':
                    body += u'<table border="0" cellspacing="0" cellpadding="0" width="98%"> \n'
                body += u'<tr><th colspan="2">%s [异常]</th></tr> \n' % cp.get('title')
                body += u'<tr><td width="80">监控点</td><td>%s</td></tr> \n' % cp.get('slot')
                body += u'<tr><td>错误信息</td><td>超过 %s 秒未接收到心跳数据</td></tr> \n' % cp.get('interval', 300)
                body += u'<tr><td colspan="2">&nbsp;&nbsp;</td></tr> \n'
                # write to exceptional
                e = ErrorPicker()
                e.save_error(sp.id, cp.get('id'), '超过 %s 秒未接收到心跳数据' % cp.get('interval', 300))
        if body != '':
            body += u'</table> \n'
            ml = SMail(MAIL_INFO.get('host'), MAIL_INFO.get('user'), MAIL_INFO.get('pwd'), mail_list)
            html = ml.template(body)
            ml.send_mail(title, html, 'html')

def check_daily_status(start_time=None, end_time=None):
    """
    :param: start_time
    :param: end_time
    :return:
    """
    today = datetime.date.today()
    if start_time is None:
        d1 = today + datetime.timedelta(-1)
        start_time = d1.strftime('%Y-%m-%d') + ' 09:00:00'
    if end_time is None:
        end_time = today.strftime('%Y-%m-%d') + ' 09:00:00'
    service_platform = ServicePlatform()
    sps = service_platform.get_service_platform()
    for sp in sps:
        title = sp.title
        mail_list = sp.mail_list
        body = ''
        control_point = ControlPoint()
        cps = control_point.get_control_point_by_sid(sp.id)
        for cp in cps:
            e = ErrorPicker()
            records = e.get_error(cp.get('id'), start_time, end_time)
            for record in records:
                if body == '':
                    body += u'<table border="0" cellspacing="0" cellpadding="0" width="90%"> \n'
                body += u'<tr><th colspan="2">%s [异常]</th></tr> \n' % cp.get('title')
                body += u'<tr><td width="80">监控点</td><td>%s</td></tr> \n' % cp.get('slot')
                body += u'<tr><td>错误信息</td><td>%s</td></tr> \n' % record.get('content')
                body += u'<tr><td colspan="2">&nbsp;&nbsp;</td></tr> \n'
        if body != '':
            body += u'</table> \n'
        else:
            body = u'系统运行正常，心跳监控正常！<br/> \n'
        body = u'统计时间段：%s - %s <br/><br/> \n' % (start_time, end_time) + body
        ml = SMail(MAIL_INFO.get('host'), MAIL_INFO.get('user'), MAIL_INFO.get('pwd'), mail_list)
        html = ml.template(body)
        ml.send_mail(title, html, 'html')

