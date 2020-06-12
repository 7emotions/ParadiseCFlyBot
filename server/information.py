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
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib import parse
from selenium.webdriver.support import expected_conditions as EC

info('[Information] module loaded')

iJustWantUtoStudy = ['正弦定理','余弦定理','pornhub']

def help() :
    with open('./../data/help.txt','r',encoding='utf-8') as fileObj :
        data = fileObj.read()
        print(data)
        return data

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

def poem( title ):
    def test_url( soup ) :
        result = soup.find( text=re.compile("百度汉语中没有收录相关结果") )
        if result :
            return False
        else:
            return True

    def getpoem( soup ) :
        if soup.find( class_="poem-detail-item-content" ) :
            poem = soup.find( class_="poem-detail-item-content" ).text
            print(poem)
            return poem

    def start( title ):
        keyword = urllib.parse.urlencode( {"title" : title} )
        response = urllib.request.urlopen( "https://hanyu.baidu.com/s?wd=%s&from=poem" % keyword )
        html = response.read()
        soup = BeautifulSoup( html , "html.parser" )
        if test_url( soup ) :
            return getpoem( soup )
        else :
            return ''
    
    try :
        result = start( title )
        print(result)
        return result
    except AttributeError :
        msg = "百度汉语中没有收录相关结果"
        print(msg)
        return msg

def poem( msg ):
    arg = msg.split('#')
    title = arg[0]
    author = ''
    if '#' in msg :
        author = arg[1]
    browser = webdriver.Chrome()
    print("Opening")
    url = r'https://hanyu.baidu.com/s?wd='+parse.quote(title)
    browser.get(url)
    print('Wating...')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID,"main")))
    soup = BeautifulSoup(browser.page_source,'html.parser')
    browser.close()
    #print(soup.prettify)
    text = soup.findAll(id="body_p")
    for tag in soup.findAll() :
        if tag.name == 'em' :
            tag.decompose()
        if tag.name == 'span' and '朝代' in tag.get_text() :
            tag.decompose()
    if text == [] :
        if author == '' :
            return '无法获取，试试加上作者吧~PS：题目与作者要用#隔开哦'
        authors = soup.findAll(name="span", attrs={"class" :"poem-list-item-author"})
        poem_body = soup.findAll(name="div", attrs={"class" :"poem-list-item-body"})
        #print(poem_body)
        for i,tauthor in enumerate(authors) :
            #print(tauthor)
            if author in tauthor.get_text() :
                Bpoem = poem_body[i].get_text()
    else :
        Bpoem = ''
        for item in text:
            Bpoem += item.get_text()
    return Bpoem
