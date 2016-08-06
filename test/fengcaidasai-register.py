#coding=utf-8
__author__ = 'caiqiqi'

import sys
# 用于解析命令行参数
import argparse

import requests


def parse_command():
    """ 命令行参数解析和设置 """
    parse = argparse.ArgumentParser(description='Please input your register info.')

    info = parse.add_argument_group('info')
    info.add_argument('--name', type=str, required=True, dest='NAME')
    info.add_argument('--sex', type=str, required=True, dest='SEX')
    info.add_argument('--college', type=str, required=True, dest='COLLEGE')
    info.add_argument('--num', type=str, required=True, dest='NUM')
    info.add_argument('--phone', type=str, required=True, dest='PHONE')
    info.add_argument('--mail', type=str, required=True, dest='MAIL')

    return parse.parse_args()


register_url =        "http://m.hy323220.icoc.in/col.jsp?id=106"
register_post_url =   "http://m.hy323220.icoc.in/ajax/mobiForm_h.jsp"

get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Cache-Control":"max-age=0",
    "Connection": "keep-alive",
    "Host": "m.hy323220.icoc.in",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
}

# 先GET，为了得到cookie用于之后的POST
resp_get = requests.get(register_url, headers=get_headers)
# 先得到CookieJar
cookiejar = resp_get.cookies
cookies_get_dict = {'__cfduid': cookiejar['__cfduid'], '_cliid': cookiejar['_cliid']}

post_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": cookies_get_dict,
    "Host": "m.hy323220.icoc.in",
    "Origin": "http://m.hy323220.icoc.in",
    "Referer": "http://m.hy323220.icoc.in/col.jsp?id=106",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


#接收命令行参数
submitContentList = parse_command()
_name    = submitContentList.NAME
_sex     = submitContentList.SEX
_colloge = submitContentList.COLLEGE
_stuNum  = submitContentList.NUM
_phoneNum= submitContentList.PHONE
_mail    = submitContentList.MAIL


post_payload = {
    "cmd": "addSubmit",
    "formId": "2",
    "submitContentList": [{"id":0,"val":_name},{"id":1,"val":_sex},{"id":2,"val":_colloge},{"id":3,"val":_stuNum},{"id":4,"val":_phoneNum},{"id":5,"val":_mail}],
    "vCodeId": "3162",
    "validateCode": "undefined",
    "tmpFileList": "[]",
    "_TOKEN": "undefined"
}

# 带着请求头headers和表单发起POST请求
resp_post= requests.post(register_post_url, data=post_payload, headers=post_headers)

if resp_post != None:
	print "#1: title"
	print resp_post.url
	print "#2: cookie"
	print resp_post.cookies
	print "#3: content"
	print resp_post.content
