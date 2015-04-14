#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.db import models
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
import time
import datetime

MODE_TYPE = (('PORT', 'PORT'), ('PASV', 'PASV'))
MSG_TYPE = (('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'))

class ServicePlatform(models.Model):
    """
    ServicePlatform class
    """
    title = models.CharField(_('title'), max_length=128)
    secret_key = models.CharField(_('secret key'), max_length=64, unique=True)
    mode = models.CharField(_('mode'), max_length=16, choices=MODE_TYPE, default='PASV')
    tag = models.CharField(_('tag'), max_length=255, blank=True, null=True)
    status = models.BooleanField(_('status'), default=True)
    mail_list = models.TextField(_('mail_list'), blank=True, null=True)
    frequency = models.CharField(_('frequecy'), max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), default='0000-00-00 00:00:00')
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'service_platform'

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        super(ServicePlatform, self).save(*args, **kwargs)

    def get_service_platform_by_secret_key(self, secret_key):
        """
        :param secret_key:
        :return:
        """
        try:
            record = ServicePlatform.objects.get(secret_key=secret_key)
        except:
            record = None
        return record

    def get_service_platform_by_secret_key_dict(self, secret_key):
        """
        :param secret_key:
        :return:
        """
        record = self.get_service_platform_by_secret_key(secret_key)
        if record is not None:
            result = model_to_dict(record)
        else:
            result = None
        return result

    def get_service_platform(self):
        """
        :param
        :return:
        """
        try:
            records = ServicePlatform.objects.filter(status=True)
        except:
            records = None
        return records

class ControlPoint(models.Model):
    """
    ControlPoint class
    """
    sid = models.IntegerField(_('sid'), max_length=11)
    title = models.CharField(_('title'), max_length=128)
    slot = models.CharField(_('slot'), max_length=64, db_index=True)
    url = models.CharField(_('url'), max_length=255, blank=True, null=True)
    description = models.CharField(_('description'), max_length=255, blank=True, null=True)
    match_point = models.CharField(_('match_point'), max_length=255, blank=True, null=True)
    interval = models.IntegerField(_('interval'), max_length=11, default=300)
    tag = models.CharField(_('tag'), max_length=255, blank=True, null=True)
    status = models.BooleanField(_('status'), default=False)
    created_at = models.DateTimeField(_('created_at'), default='0000-00-00 00:00:00')
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'control_point'

    def get_control_point_by_sid(self, sid):
        """
        :param sid:
        :return:
        """
        try:
            records = ControlPoint.objects.filter(sid=sid, status=True)
        except:
            records = None
        result = []
        if records is not None:
            for record in records:
                result.append(model_to_dict(record))
        return result

    def get_control_point_by_slot(self, sid, slot):
        """
        :param slot:
        :return:
        """
        try:
            record = ControlPoint.objects.get(sid=sid, slot=slot)
        except:
            record = None
        if record is not None:
            result = model_to_dict(record)
        else:
            result = None
        return result


class HeartBeat(models.Model):
    """
    HeartBeat class
    """
    cid = models.IntegerField(_('cid'), max_length=11, db_index=True)
    slot = models.CharField(_('slot'), max_length=64)
    content = models.CharField(_('content'), max_length=255, blank=True, null=True)
    tag = models.CharField(_('tag'), max_length=255, blank=True, null=True)
    ip_address = models.CharField(_('ip_address'), max_length=16, blank=True, null=True)
    has_error = models.BooleanField(_('has_error'), default=False)
    status = models.BooleanField(_('status'), default=True)
    created_at = models.DateTimeField(_('created_at'))
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'heart_beat'

    def save_heartbeat(self, cid, slot, content, ip_addr, has_error=False, created_at=None):
        """
        :param cid:
        :param slot:
        :param content:
        :param ip_addr:
        :param created_at:
        :return:
        """
        if created_at is None:
            created_at = time.strftime('%Y-%m-%d %H:%M:%S')
        hb = HeartBeat()
        hb.cid = cid
        hb.slot = slot
        hb.content = content
        hb.ip_address = ip_addr
        hb.has_error = has_error
        hb.created_at = created_at
        hb.save()
        return True


    def get_heartbeat(self, limit=0, offset=0):
        """
        :param limit:
        :param offset:
        :return:
        """
        if limit == 0:
            records = HeartBeat.objects.all()
        else:
            records = HeartBeat.objects.all()[offset:(limit+offset)]
        result = []
        for record in records:
            result.append(model_to_dict(record))
        return result

    def count_heartbeat(self, cid, interval=300):
        """
        :param interval:
        :return:
        """
        d1 = datetime.datetime.now()
        d2 = d1 + datetime.timedelta(seconds=-interval)
        start_time = datetime.datetime.strftime(d2, '%Y-%m-%d %H:%M:%S')
        num = HeartBeat.objects.filter(cid=cid, created_at__gte=start_time).count()
        return num

class ErrorPicker(models.Model):
    """
    DailyStatistics class
    """
    sid = models.IntegerField(_('sid'), max_length=11)
    cid = models.IntegerField(_('cid'), max_length=11)
    content = models.TextField(_('content'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'))
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True, auto_now=True)



    class Meta:
        db_table = 'error_picker'

    def save_error(self, sid, cid, content, created_at=None):
        """
        :param sid:
        :param cid:
        :param content:
        :param created_at:
        :return:
        """
        if created_at is None:
            created_at = time.strftime('%Y-%m-%d %H:%M:%S')
        e = ErrorPicker()
        e.sid = sid
        e.cid = cid
        e.content = content
        e.created_at = created_at
        e.save()
        return True

    def get_error(self, cid, start_time=None, end_time=None):
        """
        :param cid:
        :param start_time:
        :param end_time:
        """
        today = datetime.date.today
        if start_time is None:
            d1 = today + datetime.timedelta(-1)
            start_time = d1.strftime('%Y-%m-%d') + ' 09:00:00'
        if end_time is None:
            end_time = today.strftime('%Y-%m-%d') + ' 09:00:00'
        es = ErrorPicker.objects.filter(cid=cid, created_at__gte=start_time, created_at__lte=end_time)
        return es
