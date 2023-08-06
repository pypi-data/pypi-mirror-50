# -*- coding: utf-8 -*-

import json
import os
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib


def send():
    file = os.path.expanduser('~/.kindle.config.json')
    kindle_email = None
    send_email = None
    send_secret = None
    file_path = None

    if not os.path.exists(file):
        kindle_email = input('kindle邮箱:').strip()
        send_email = input('发送邮箱地址:').strip()
        send_secret = input('发送邮箱密码:').strip()

        info = {
            'kindle_email': kindle_email,
            'send_email': send_email,
            'send_secret': send_secret,
        }
        with open(file, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, ensure_ascii=False)
    else:
        if os.path.exists(file):
            with open(file, 'r') as f:
                dic = json.loads(f.read())
                kindle_email = dic['kindle_email']
                send_email = dic['send_email']
                send_secret = dic['send_secret']

    file_path = input('文件或目录路径:')
    file_path = file_path.replace('\\', '')
    file_path = file_path.strip()

    if os.path.isfile(file_path):
        send_text_email(' ',
                        ' ',
                        send_email,
                        ' ',
                        send_secret,
                        kindle_email,
                        '', [file_path, ])

    elif os.path.isdir(file_path):
        upload_list = []

        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('.mobi'):
                    upload_list.append(os.path.join(root, file))

        send_text_email(' ',
                        ' ',
                        send_email,
                        ' ',
                        send_secret,
                        kindle_email,
                        '', upload_list)

    else:
        print('路径未识别!')


# 发送纯文本邮件:
def send_text_email(subject, content, from_email, from_user, pwd, to_email, to_user, file_path_list):
    smtp_server = 'smtp.126.com'
    # msg = MIMEText(content, 'plain', 'utf-8')

    msg = MIMEMultipart()
    # 添加附件:
    for file in file_path_list:
        attachment = MIMEApplication(open(file, 'rb').read())
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        msg.attach(attachment)

    msg['From'] = _format_addr(from_user + '<%s>' % from_email)
    msg['To'] = _format_addr(to_user + '<%s>' % to_email)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_email, pwd)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
    print('发送成功!')


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    send()




