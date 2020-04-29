#!/usr/bin/python3
# -*- coding:utf8 -*-
import wikipedia as wk
from urllib.request import pathname2url as urlencode
from requests import get
from random import choice
from utilities import *
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
