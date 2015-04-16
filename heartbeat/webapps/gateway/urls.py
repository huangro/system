#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('gateway.views',
    url(r'heartbeat', 'heartbeat', name='gateway_heartbeat'),
)