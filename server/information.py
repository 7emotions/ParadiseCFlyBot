#!/usr/bin/python3
# -*- coding:utf8 -*-
import wikipedia as wk
from urllib.request import pathname2url as urlencode
from requests import get
from random import choice
from utilities import *
from googletrans import Translator
info('[Information] module loaded')

iJustWantUtoStudy = ['正弦定理','余弦定理','pornhub']

def wikipedia(kwd, lang = 'zh') :
    base = 'https://'+lang+'.wikipedia.org/wiki/'
    '''
    Get information from wikipedia
    '''
    try :
        wk.set_lang(lang)
        result = wk.page(kwd)
        hr()
        info(str(result))
        hr()
        return result
    except :
        return False

def search(kwd = '') :
    search_url = "https://www.bing.com/search?q=" + urlencode(kwd)
    if kwd == '' :
        kwd = choice(iJustWantUtoStudy)
    wk_page = wikipedia(kwd)
    if (wk_page) :
        return [
            '在 Wikipedia 上找到如下信息：\n' + wk_page.url + '\n\n' + wk_page.summary,
            wk_page.images[0]
        ]
    else :
        return search_url

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

def pronounce(word,type=0):
    '''
    Pronounce English words
    Args:
        type: American pronunciation(0) or British pronunciation(1)
        word: word to pronounce
    Returns:
        String, link
    '''
    info('Geting pronunciation:'+word)
    api_url = 'http://dict.youdao.com/dictvoice?type='+str(type)+'&audio='
    return api_url + word