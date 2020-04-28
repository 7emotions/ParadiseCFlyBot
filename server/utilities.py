#!/usr/bin/python3
# -*- coding:utf8 -*-

bing_logo = 'https://fitsmallbusiness.com/wp-content/uploads/2019/03/Bing_logo2.png'

def info(msg, sign = '*') :
	print('\033[32m['+sign+']\033[0m ' + msg);
	return 0

def hr(n = 20) :
	print('\033[35m'+'='*n+'\033[0m ')
	return 0
