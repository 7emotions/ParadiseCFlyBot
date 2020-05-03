#!/usr/bin/python3
# -*- coding:utf8 -*-
import requests
import os

api_url = 'http://172.17.0.1:5700/send_msg'
bing_logo = 'https://fitsmallbusiness.com/wp-content/uploads/2019/03/Bing_logo2.png'

def info(msg, sign = '*') :
    # Windows 的终端好像不支持颜色输出 T_T
    # print('\033[32m['+sign+']\033[0m ' + msg)
    print('['+sign+'] ' + str(msg))
    return 0

def hr(n = 20) :
    # print('\033[35m'+'='*n+'\033[0m ')
    print('='*n)
    return 0

def send(send_msg, id, type = "private") :
    send_data = {
        'user_id': id, # qq号， 私聊时用
        'group_id': id,# 群组号
        'discuss_id': id,# 讨论组号
        'message_type': type,#究竟是发消息给谁是由这个消息的来源类型决定的
        'message': str(send_msg),
        'auto_escape': False
    }
    hr()
    info("Sending data:\n" + str(send_data))
    hr()
    status = requests.post(api_url,data=send_data).json()['status']
    if status != 'ok' :
        return False
    info("Send status: " + status)
    return True

def execute(cmd = '') :
    return os.popen(cmd).read()
