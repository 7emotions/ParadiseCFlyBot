#!/usr/bin/python3
# -*- coding : utf8 -*-
import wikipedia as wk
import urllib.request
import urllib.parse
import re
from urllib.request import pathname2url as urlencode
from requests import get
from random import choice
from utilities import *
from youdao_tr import youdao_tr

from bs4 import BeautifulSoup

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
    txt = youdao_tr(txt)
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
    return api_url + urlencode(word)


def baike( word ) :
    '''
    Get Summary from Baidu Baike
    Args:
        word: key word for searching
    Returns:
        String, Summary or Error
    '''
    def test_url( soup ) :
        result = soup.find( text=re.compile("百度百科未收录该词条") )
        if result :
            return False
        else:
            return True

    def summary( soup ) :
        word = soup.h1.text 
        if soup.h2 :
            word += soup.h2.text
            print( word )
        if soup.find( class_="lemma-summary" ) :
            sum = soup.find( class_="lemma-summary" ).text
            print(sum)
            return sum

    def start( word ):
        keyword = urllib.parse.urlencode( {"word" : word} )
        response = urllib.request.urlopen( "http://baike.baidu.com/search/word?%s" % keyword )
        html = response.read()
        soup = BeautifulSoup( html , "html.parser" )
        if test_url( soup ) :
            return summary( soup )
        else :
            return ''
    
    try :
        return start( word )
    except AttributeError :
        msg = "百度百科未收录该词条"
        print(msg)
        return msg