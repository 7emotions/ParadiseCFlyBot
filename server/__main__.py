from flask import Flask,request
from json import loads
from utilities import *
import information
import programrunning
import music
import re
import IniFileHelper

app = Flask(__name__)

cmds = {
    '/search' : '搜索中 ...',
    '/translate' : '翻译中 ...',
    '/music' : '音乐加载中 ...',
    '/exec' : '',
    '/py' : '',
    '/pronounce' : '查找中...',
    '/baike' : '查找中...',
    '/addqid' : '添加中...',
    '/help' : '',
    '/poem' : '查找中...'
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


@app.route('/',methods=['POST'])
def server() :
    data = request.get_data().decode('utf-8')
    data = loads(data)

    qid = data['user_id']
    r_msg = data['raw_message']   # 消息体
    c_type = data['message_type'] # 消息来源类型
	
    if 'discuss_id' in data :
        id = data['discuss_id']
    elif 'group_id' in data :
        id = data['group_id']
    else :
        id = qid

    if (not qid in IniFileHelper.getHAQid()) and c_type == 'private':
        send('您没有使用权限，请添加3393103594激活', id, c_type)
        return ''
    
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
            send_msg = information.translate(re.sub(r'^/translate *', '', r_msg))
        elif cmd == '/music' :
            send_msg = music.get(re.sub(r'^/music *', '', r_msg))
        elif cmd == '/exec' :
            if qid in IniFileHelper.getAdminQid() :
                send_msg= execute(re.sub(r'^/exec *','',r_msg))
            else :
                send_msg = 'Permission denied.'
        elif cmd == '/py' :
            send_msg = programrunning._(qid, re.sub(r'^/py *', '', r_msg))
        elif cmd == '/pronounce':
            send_msg = information.pronounce(re.sub(r'^/pronounce *','',r_msg))
        elif cmd == '/baike':
            send_msg = information.baike(re.sub(r'^/baike *','',r_msg))
        elif cmd == '/help' :
            send_msg = information.help()
        elif cmd == '/poem' :
            send_msg = information.poem(re.sub(r'^/poem *','',r_msg))
        elif cmd == '/addqid' :
            if qid in IniFileHelper.getAdminQid() :
                send_msg = 'Successfully Added!' if IniFileHelper.addHAQid(re.sub(r'^/addqid *','',r_msg)) else 'Failed to add!'
            else :
                send_msg = 'Permission denied.'
        else :
            send_msg = ''

        send(send_msg, id, c_type)
    return ''

if __name__ == '__main__':
    app.run(host='127.0.0.1')
