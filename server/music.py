#!/usr/bin/python3
# -*- coding:utf8 -*-
import requests
from utilities import *
info("Music module loaded")

def search(kwd) :
    '''
    search music
    '''
    api_addr = 'https://v1.alapi.cn/api/music/search?limit=1&keyword='
    try :
        # 暂时只支持搜索一首
        response = requests.get(api_addr + kwd).json()['data']['songs'][0]
    except :
        response = False
    return response

def format(data) :
    '''
    format data to QQ share card
    '''

    # formated = '[CQ:music,type=163,url={1},audio={2},title={3},content={4},image={5}]'
    '''
    {1} 分享链接，即点击分享后进入的音乐页面（如歌曲介绍页）。
    {2} 音频链接（如mp3链接）。
    {3} 音乐的标题，建议12字以内。
    {4} 音乐的简介，建议30字以内。该参数可被忽略。
    {5} 音乐的封面图片链接。若参数为空或被忽略，则显示默认图片
    '''
    formated = '[CQ:music,type=163,id='+ str(data['id']) +']'
    return formated

def get(kwd) :
    return format(search(kwd))
