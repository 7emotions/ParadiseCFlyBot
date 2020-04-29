#!/usr/bin/python3
# -*- coding:utf8 -*-
import requests

api_url = 'http://127.0.0.1:5700/send_private_msg'
bing_logo = 'https://fitsmallbusiness.com/wp-content/uploads/2019/03/Bing_logo2.png'

def info(msg, sign = '*') :
	print('\033[32m['+sign+']\033[0m ' + msg);
	return 0

def hr(n = 20) :
	print('\033[35m'+'='*n+'\033[0m ')
	return 0

def send(send_msg, qid) :
    send_data = {
        'user_id': qid,
        'message': send_msg, # 这里不要用str(), 分享音乐需要
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
