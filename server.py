from flask import Flask,request
from json import loads
from urllib.request import pathname2url as urlencode
from googletrans import Translator
import re
import requests

app = Flask(__name__)

def command(msg):
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

    #catch = re.match(r'\/\w+', msg)
    '''
    print(catch)
    if catch :
        return catch.group()
    else :
        return False
    '''

    if 'search' in msg:
        return 'search'
    elif 'translate' in msg:
        return 'translate'
    else:
        return False

def search(kwd):
    '''
    search something from the net

    Args:
        kwd: keyword
    Returns:
        string, whatever it is, you just fuckin return it to client !
    '''
    # base = 'https://google.com/search?q='
    # base = 'https://baidu.com/s?wd='
    print('searching...')
    base = 'https://cn.bing.com/search?q='
    return base + urlencode(kwd)

def translate(txt):
    '''
    translate btween Chinese and English

    Args:
        txt: text to translate
    Returns:
        String, result
    '''
    print('Translating...')
    translator = Translator(service_urls=['translate.google.cn'])
    result = re.compile('[\u4e00-\u9fa5]')
    print(txt)
    if result.search(txt):
        print('C2E')
        # Chinese 2 English
        txt = translator.translate(txt,src='zh-cn',dest='en').text
    else :
        print('E2C')
        # English 2 Chinese
        txt = translator.translate(txt,src='en',dest='zh-cn').text
    return txt
'''
def is_contains_chinese(strs):
    for ch in strs:
        if '\\u4e00' <= ch <= '\\u9fff':
            return True
    return False
'''
@app.route('/',methods=['POST'])
def server():
    data = request.get_data().decode('utf-8')
    data = loads(data)
    print(data)
    msg = data['raw_message']
    qid = data['user_id']
    print(msg)
    cmd = command(msg)



    if msg :
        if cmd == 'search' :
            rmsg = search(msg.replace('search',''))
        elif cmd == 'translate' :
            rmsg = translate(msg.replace('translate',''))
        #print rmsg
        rdata = {
            'user_id':qid,
            'message':str(rmsg),
            'auto_escape':False
        }
        # api_url = 'http://172.17.0.1:5700/send_private_msg'
        api_url = 'http://127.0.0.1:5700/send_private_msg'
        r = requests.post(api_url,data=data)
        print(r)
    return ''

if __name__ == '__main__':
    # app.run(host='172.18.0.1')
    #  ^--- fuckin docker
    app.run()

