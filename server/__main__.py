from flask import Flask,request
from json import loads
from urllib.request import pathname2url as urlencode
from googletrans import Translator
from random import random
from utilities import *
import music
import re
import os
import requests

app = Flask(__name__)

def command(msg) :
    '''
    Fetch command from a raw message

    Args:
        msg: message
    Returns:
        String, command.
        example:
            search
            translate
    '''

    catch = re.match(r'\/\w+', msg)
    if catch :
        info('Catched command: ' + catch.group())
        return catch.group()
    else :
        return False

def search(kwd) :
    '''
    search something from the net

    Args:
        kwd: keyword
    Returns:
        string, whatever it is, you just fuckin return it to client !
    '''
    # base = 'https://google.com/search?q='
    # base = 'https://baidu.com/s?wd='
    base = 'https://cn.bing.com/search?q='
    info('Searching '+ kwd)
    link = base + urlencode(kwd)
    return shareLink(link, kwd + ' 的搜索结果', kwd + ' 在bing上的搜索结果')

def translate(txt) :
    '''
    translate btween Chinese and English

    Args:
        txt: text to translate
    Returns:
        String, result
    '''
    info('Translating: ' + txt)
    translator = Translator(service_urls=['translate.google.cn'])
    Chinese = re.compile('[\u4e00-\u9fa5]')
    if Chinese.search(txt) :
        info('Translate Chinese to English')
        txt = translator.translate(txt,src='zh-cn',dest='en').text
    else :
        info('Translate English to Chinese')
        txt = translator.translate(txt,src='en',dest='zh-cn').text
    return txt

def execute(py_cmd) :
    '''
    run a command
    '''

#     f_name = str(random()) + '.py'
#     run_cmd = '''
# echo """
# ''' + py_cmd + '''
# """ > ''' + f_name + '''
# python ''' + f_name + '''
# rm ''' + f_name + '''
#     '''
    # return os.popen(run_cmd).read()
    return os.popen(py_cmd).read()

@app.route('/',methods=['POST'])
def server() :
    data = request.get_data().decode('utf-8')
    data = loads(data)
    r_msg = data['raw_message']   # 消息体
    c_type = data['message_type'] # 消息来源类型
    qid = data['user_id'] # qq号
    cmd = command(r_msg) # 命令请求

    if r_msg and c_type == 'private' :
        #        ^^^^^^^^^^^^^^^^^^^ 调试期间先只用私聊

        hr()
        info("Received data:\n" + str(data))
        hr()

        if cmd == '/search' :
            send_msg = search(r_msg.replace('/search ',''))
        elif cmd == '/translate' :
            send_msg = translate(r_msg.replace('/translate ',''))
        elif cmd == '/music' :
            send_msg = music.get(r_msg.replace('/music ',''))
        elif cmd == '/exec' :
            send_msg = execute(r_msg.replace('/exec ',''))
        else :
            send_r_msg = ''

        send_data = {
            'user_id': qid,
            'message': send_msg, # 这里不要用str(), 分享音乐需要
            'auto_escape': False
        }

        api_url = 'http://127.0.0.1:5700/send_private_msg'
        status = requests.post(api_url,data=send_data)

        hr()
        info("Sended data:\n" + str(send_data))
        hr()
        info("Send status: " + status.text)
    return ''

if __name__ == '__main__':
    app.run(host='127.0.0.1')
