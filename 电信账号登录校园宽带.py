#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import os
import re
import random

import requests

import pytesseract
from PIL import Image
# random.random(),同javascript的Math.random(),返回[0.0,1)之间的浮点数
# random.uniform(a, b),返回[a,b]之间的浮点数
# _url_login = "http://cq.189.cn/ttcollege/login"
_url_imagecode = "http://cq.189.cn/ttcollege/imageCode?"+ str(random.random())
_url_post  = "http://cq.189.cn/ttcollege/loginAjax"

_cookie = ""

_file_captcha = "captcha.png"
_result_captcha = ''

_pattern_1 = "Set-Cookie"
_pattern_2 = ";"
_str_example = "Set-Cookie:imagecode=893B36A9BBA82AD2;"
# str.split()之后得到的是一个list，取这个list的第二个[1]，然后再将得到的结果，一个list，取其第一部分[0]
#_str_set_cookie.split(_pattern_1)[1].split(_pattern_2)[0]


def parse_resp_headers(html_headers):
	''' 这是根据返回的response.headers这个dict中的信息特征写的'''
	return dict_headers[_pattern_1].split(_pattern_2)[0]

def _save_img_from_resp(resp, filename):
    '''
    get the captcha by the url_captcha and save the image as 'captcha.png'
    '''
    #r = requests.get(imageUrl)
    # with open(filename, 'w') as fp:
    # shutil.copyfileobj(data, fp)
    f = open(filename, 'wb')
    f.write(resp.content)
    f.close()

def is_file_empty(filepath):
    '''
    判断文件内容是否为空
    '''
    file_size = os.stat(filepath).st_size
    if 0 == file_size:
        return True
    else:
        return False

def _parse_img_to_txt(image_file):
    if not is_file_empty(image_file):
        result = pytesseract.image_to_string(Image.open(image_file))
        print result
        return result
    # 下面这句print并不会执行
    # print result
    else:
        print "File size zero!"
        return ""

# 1. 先get(_url_login)得到imagecode的cookie，然后post登录
_resp1 = requests.get(_url_imagecode)
# 得到响应头： .headers
dict_headers = _resp1.headers

# 经过解析headers之后可以将 `imagecode`提取出来，以便之后通过后续的post请求发出去
_cookie = parse_resp_headers(dict_headers)

_save_img_from_resp(_resp1, _file_captcha)
_result_captcha = _parse_img_to_txt(_file_captcha)

headers = {
	"Accept": "application/json, text/javascript, */*; q=0.01",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
	"Connection": "keep-alive",
	"Content-Length": "56",
	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	"Cookie": _cookie,
	"Host": "cq.189.cn",
	"Origin": "http://cq.189.cn",
	"Referer": "http://cq.189.cn/ttcollege/login",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
	"X-Requested-With": "XMLHttpRequest"
}

form_data = {
	"accountId": "1620600@cqupt",
	"accountPwd": "000000",
	"imgcode": _result_captcha
}

# 2. POST登录
_resp2 = requests.post(_url_post, data= form_data,headers= headers)
print _resp2.url
print _resp2


#if "__name__" == "__main__":
#	init()
