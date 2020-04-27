#!/usr/bin/python3
# -*- coding:utf8 -*-

bing_logo = 'https://fitsmallbusiness.com/wp-content/uploads/2019/03/Bing_logo2.png'

def info(msg, sign = '*') :
	print('\033[32m['+sign+']\033[0m ' + msg);
	return 0

def hr(n = 20) :
	print('\033[35m'+'='*n+'\033[0m ')
	return 0

def shareLink(link, title, desc = '', image = bing_logo) :
	'''
	create a share link
	'''

	# msg = '[CQ:share,url={1},title={2},content={3},image={4}]'
	'''
	{1} 分享链接。
	{2} 分享的标题，建议12字以内。
	{3} 分享的简介，建议30字以内。该参数可被忽略。
	{4} 分享的图片链接。若参数为空或被忽略，则显示默认图片。
	'''

	# 这个卡片分享链接好像用不了
	return '[CQ:share,url='+link+',title='+title+',content='+desc+',image='+image+']'
