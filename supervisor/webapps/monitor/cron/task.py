#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'robin'


import os
import sys
import time
from django.core.management import execute_from_command_line

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = SCRIPT_DIR.replace('/monitor/cron', '')

sys.path.append(PROJ_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervisor.settings')

from monitor.views import *

