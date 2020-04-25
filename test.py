from flask import Flask,request
from json import loads
from urllib.parse import quote as urlencode
from googletrans import Translator
import re

app = Flask(__name__)

@app.route('/',methods=['POST'])

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

    catch = re.match(r'\/\w+', msg)
    if catch :
        return catch.group()
    else :
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
    translator = Translator(service_urls=['translate.google.cn'])
    if re.search(r'[\u4e00-\u9fa5]', txt):
        # Chinese 2 English
        txt = translator.translate(txt,src='zh-cn',dest='en').text
    else :
        # English 2 Chinese
        txt = translator.translate(txt,src='en',dest='zh-cn').text
    return txt

def server():
    data = request.get_data().decode('utf-8')
    data = loads(data)
    msg = data['raw_message']
    cmd = command(msg)
    if msg :
        if msg == 'search' :
            return search(re.sub('/search ', '', cmd))
        elif msg == 'translate' :
            return translate(re.sub('/translate ', '', cmd))
    return ''

if __name__ == '__main__':
    app.run()