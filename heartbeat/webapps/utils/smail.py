#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'robin'

import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class SMail:
    def __init__(self, host, from_user, from_user_pwd, to_users):
        self.host = host
        self.from_user = from_user
        self.from_user_pwd = from_user_pwd
        self.to_users = to_users

    def send_mail(self, subject, content, mtype="text", attachment=None):
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = self.from_user
        if type(self.to_users) == list:
            msg['To'] = ';'.join(self.to_users)
        else:
            msg['To'] = self.to_users

        body = MIMEText(content, mtype, _charset='UTF-8')
        msg.attach(body)

        if attachment:
            for f in attachment:
                ctx = open(f, 'rb').read()
                att = MIMEText(ctx, 'base64', 'utf8')
                att['Content-Type'] = 'application/octet-stream'
                att['Content-Disposition'] = 'attachment; filename=' + f[f.rfind('/')+1:]
                msg.attach(att)
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.login(self.from_user, self.from_user_pwd)
            server.sendmail(self.from_user, self.to_users, msg.as_string())
            server.close()
            return True
        except Exception, e:
            return False

    def template(self, body):
        html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/ xhtml1-strict.dtd"> \n'
        html += '<html xmlns="http://www.w3.org/1999/xhtml"> \n'
        html += '<meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />\n'
        html += '''<head>\n 
           <title>Notice Mail</title> \n
           <style type="text/css"> \n
           h3 {margin:4px 0;} \n
           table {text-align:left; width:90%; border-collapse:collapse; border-spacing:0; margin-bottom:10px;} \n
           th,td {padding:2px 4px; text-align:center; border:1px solid #CECECE; height:30px;}\n
           th {background-color:#DDD; color:#272A2C; font-weight:700;} \n
           th.center {text-align:center;}
           th.left {text-align:left;}
           td.center {text-align:center;}
           td.left {text-align:left;}
           table.col4 th, table.col4 .td {width:25%;}
           </style> \n
           </head> \n
    '''
        html += '<body> \n'
        html += body
        html += '</body> \n'
        html += '</html>'
        return html
        
