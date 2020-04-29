#!/usr/bin/python3
# -*- coding:utf8 -*-
from urllib.request import pathname2url as urlencode
from random import choice
import wikipedia as wk
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
        # result = wk.page(kwd)
        # 这里只加载summary以提高响应速度
        summary = wk.summary(kwd)
        hr()
        info(str({
            'summary' : summary,
            'url' : base + kwd
        }))
        hr()
        # return result
        return {
            'summary' : summary,
            'url' : base + kwd
        }
    except :
        return False

def search(kwd = '') :
    search_url = "https://www.bing.com/search?q=" + urlencode(kwd)
    if kwd == '' :
        kwd = choice(iJustWantUtoStudy)
    wk_page = wikipedia(kwd)
    if (wk_page) :
        return ("在 Wikipedia 上找到如下内容:\n" +
            wk_page['url'] + "\n\n" +
            wk_page['summary'])
    else :
        return search_url
