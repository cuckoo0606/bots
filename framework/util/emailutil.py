#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: lixingtie
# Email: lixingtie@barfoo.com.cn
# Create Date: 2014-04-16

#
# SMTP邮件工具类
# 通过在根目录的settings目录配置DEFAULT_EMAIL_SERVER,DEFAULT_EMAIL_PORT,DEFAULT_EMAIL_USER,DEFAULT_EMAIL_PASS设置默认SMTP连接信息
# SMTP连接信息也可以在调用发送函数时动态传入。
#

import os
import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

try:
    from settings import DEFAULT_EMAIL_SERVER, DEFAULT_EMAIL_PORT, \
                        DEFAULT_EMAIL_USER, DEFAULT_EMAIL_PASS
except:
    DEFAULT_EMAIL_SERVER = DEFAULT_EMAIL_PORT = None
    DEFAULT_EMAIL_USER = DEFAULT_EMAIL_PASS = None


def send(sender, receiver, subject, message, attachments = [], settings = {}, **kwargs):
    """
        发送SMTP邮件
        sender : 发件人email地址
        receiver : 收件人email地址
        subject : 邮件标题
        message : 邮件内容
        attachments : 附件列表(可以为路径，也可以是二进制文件流)
        settings : smtp邮件服务器连接信息
            server : SMTP邮件服务器地址
            port : SMTP邮件服务器端口
            user : SMTP验证用户
            password : SMTP验证密码
        kwargs : 附加参数

        e.g.:
            emailutil.send("sender@sample.com", "receiver@sample.com", "sample", "this is a sample mail")
    """
    server = settings.get("server") or DEFAULT_EMAIL_SERVER
    port = settings.get("port") or DEFAULT_EMAIL_PORT
    user = settings.get("user") or DEFAULT_EMAIL_USER
    password = settings.get("password") or DEFAULT_EMAIL_PASS

    if not server or not port or not user or not password:
        raise EmailError("缺少SMTP服务器信息，请在settings文件中配置或作为参数传入。")

    if not user or not password:
        raise EmailError("缺少SMTP用户信息，请在settings文件中配置或作为参数传入。")

    #if user != sender:
    #    raise EmailError("发信人地址必须和SMTP验证用户一致。")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    
    txt = MIMEText(message)
    msg.attach(txt)

    for att in attachments:
        path = att
        subtype = None
        if os.path.isfile(att):
            ctype, encoding = mimetypes.guess_type(att)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split('/', 1)

            with open(path, "rb") as f:
                att = f.read()

        att = MIMEImage(att, subtype or "octet-stream")
        att.add_header('Content-Disposition', 'attachment', filename = os.path.basename(path) or "attachment")
        msg.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect('{0}:{1}'.format(server, port))
    smtp.login(user, password)
    status = smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    return status


class EmailError(Exception):
    pass


if __name__ == "__main__":
    settings = {
            "server" : "smtp05.sherwebcloud.com",
            "port" : 25,
            "user" : "barefoot@sandpiperrental.com",
            "password" : "BAREfoot1*",
        }
    send("rent@sandpiperrental.com", "260031207@qq.com", "测试附件", "测试邮件", settings = settings)
