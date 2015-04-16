#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import signal
import urllib
import urllib2
import httplib
import datetime
import cookielib
import subprocess

def exec_command(command, timeout=20):
    """
    Execute command 
    """
    cmd = command.strip().split(' ')
    start = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
    return process.stdout.readlines()

def build_opener(url, account):
    """
    Build opener by cookielib
    """
    cookie_lib = cookielib.LWPCookieJar()
    cookie_processor = urllib2.HTTPCookieProcessor(cookie_lib)
    auth_handler = urllib2.HTTPDigestAuthHandler()
    auth_handler.add_password('', url, account.get('username'), account.get('password'))
    opener = urllib2.build_opener(cookie_processor, auth_handler)
    return opener

def http_request(url):
    """
    Http request
    """
    code = 0
    error = ''
    content = ''
    try:
        res = urllib2.urlopen(url)
        code = res.getcode()
        content = res.read()
    except urllib2.URLError as ex:
        error = ex
    return code, error, content

def http_request_with_cookie(opener, url):
    """
    Http request with cookie
    """
    code = 0
    error = ''
    content = ''
    try:
        req = urllib2.Request(url)
        res = opener.open(req)
        code = res.getcode()
        content = res.read()
    except urllib2.URLError as ex:
        error = ex
    try:
        content = content.decode('gbk').encode('utf8')
    except:
        pass
    return code, error, content
    

def get_http_header(host, url):
    """
    Get http header
    """
    conn = httplib.HTTPConnection(host)
    conn.request('GET', url)
    res = conn.getresponse()
    headers = res.getheaders()
    return headers

def get_http_header_value(headers, key):
    """
    Get http header value
    """
    value = None
    for header in headers:
        if header[0] == key:
            value = header[1]
            break
    return value
