from flask import Flask,request
from base64 import b64encode
from json import loads
# from googletrans import Translator
from youdao_tr import youdao_tr
from random import random
from utilities import *
import music
import information
import re
import os

app = Flask(__name__)

cmds = {
    '/search' : '搜索中 ...',
    '/translate' : '翻译中 ...',
    '/music' : '音乐加载中 ...',
    '/exec' : '',
    '/python' : ''
}

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
        catch = catch.group()
        info('Catched command: ' + catch)
        if catch in cmds :
            return catch
    return False

def translate(txt) :
    '''
    translate btween Chinese and English

    Args:
        txt: text to translate
    Returns:
        String, result
    '''
    info('Translating: ' + txt)
    # translator = Translator(service_urls=['translate.google.cn'])
    # Chinese = re.compile('[\u4e00-\u9fa5]')
    # if Chinese.search(txt) :
    #     info('Translate Chinese to English')
    #     txt = translator.translate(txt,src='zh-cn',dest='en').text
    # else :
    #     info('Translate English to Chinese')
    #     txt = translator.translate(txt,src='en',dest='zh-cn').text
    txt = youdao_tr(txt)
    return txt

def execute(cmd) :
    '''
    run a command
    '''
    info('Running :'+cmd)
    return os.popen(cmd).read()

def pyExec(py_cmd):
    '''
    run a python command
    '''
    info('Running python: '+py_cmd)
    f_name = str(random()) + '.py'
    py_cmd = py_cmd.replace("\"", '\\"')#.replace("'", "\\'")
    run_cmd = '''
echo """
''' + py_cmd + '''
""" > ''' + f_name + '''
python ''' + f_name + '''
rm ''' + f_name + '''
    '''
    return execute(run_cmd)

@app.route('/',methods=['POST'])
def server() :
    data = request.get_data().decode('utf-8')
    data = loads(data)
    r_msg = data['raw_message']   # 消息体
    c_type = data['message_type'] # 消息来源类型

    if 'discuss_id' in data :
        id = data['discuss_id']
    elif 'group_id' in data :
        id = data['group_id']
    else :
        id = data['user_id']

    cmd = command(r_msg) # 命令请求

    if r_msg and cmd :
        if cmds[cmd] != '' :
            send(cmds[cmd], id, c_type)
        hr()
        info("Received data:\n" + str(data))
        hr()

        if cmd == '/search' :
            search_result = information.search(re.sub(r'^/search *', '', r_msg))
            send_msg = search_result[0]
            send('[CQ:image,file='+search_result[1]+']', id, c_type)
        elif cmd == '/translate' :
            send_msg = translate(re.sub(r'^/translate *', '', r_msg))
        elif cmd == '/music' :
            send_msg = music.get(re.sub(r'^/music *', '', r_msg))
        elif cmd == '/exec' :
            if c_type == 'group': 
                if not data['sender']['role'] == 'admin':
                    return ''
            send_msg = execute(re.sub(r'^/exec *', '', r_msg))
        elif cmd == '/python' :
            send_msg = pyExec(re.sub(r'^/python *', '', r_msg))
        else :
            send_msg = ''

        send(send_msg, id, c_type)
    return ''

if __name__ == '__main__':
    app.run(host='127.0.0.1')

