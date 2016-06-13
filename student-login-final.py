#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import requests
import os
import json
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser

import pytesseract
from PIL import Image

from parser import parse_to_post_params

# 再用GET去到validateCode.aspx
# 解析验证码之后，将结果告诉url_payload
# 带着这个header，用POST提交到Relogin.aspx(这时解析ini文件中的信息)
# 测试是否登录成功

# 开始就用一个session来维持整个回话，这样在之后请求中可以沿用之前的headers，
# 而且可以往headers里添加已有的字段以覆盖之前的字段，这样connection才是『keep-alive』，而不是close
s = requests.Session()

CONFIG_FILE = 'config.ini'
CONFIG_ITEM_INFO = 'info'

_username = ''
_password = ''
_result_captcha = ''

_file_captcha     = "captcha.png"
_url_captcha      = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
_url_loging       = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
_url_relogin      = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
_url_course_query = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="

_cookie = "Cookie"
_cookie_value_318_2055 = "ASP.NET_SessionId=nembjmva4ig4uw43l0rna5ae"

headers0 = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Upgrade-Insecure-Requests": "1"
}

headers_image = {
    "Host": "gs.cqupt.edu.cn:8080",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
    "Accept": "image/webp,image/*,*/*;q=0.8",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4"
} 
# 要POST给登录页面的
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Origin": "http://gs.cqupt.edu.cn:8080",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
}
# 登录成功页面的
headers1 = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
}
# 查询课程详情的
headers2 = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Origin": "http://gs.cqupt.edu.cn:8080"
}



def _get_item_from_ini():
    '''
    从.ini文件中载入账户密码信息
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)
    # 在python2中,对于全局变量,如果只是在函数中使用了它的值(而没对它赋值),那么不需要声明`global`
    # 若在函数中声明了`global`,则表示是在给全局变量赋值,而不是局部变量赋值
    global _username
    global _password
    _username = cf.get(CONFIG_ITEM_INFO, 'username')
    _password = cf.get(CONFIG_ITEM_INFO, 'password')
    # 不要将四个空格和TAB键混用了

def _save_img_from_url(imageUrl, filename):
    '''
    get the captcha by the url_captcha and save the image as 'captcha.png'
    '''
    r = s.get(imageUrl, headers= headers_image)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()

def _is_file_empty(filepath):
    '''
    判断文件内容是否为空
    '''
    file_size = os.stat(filepath).st_size
    if 0 == file_size:
        return True
    else:
        return False

def _parse_img_to_txt(image_file):
    if not _is_file_empty(image_file):
        result = pytesseract.image_to_string(Image.open(image_file))
        return result
    else:
        print "File size zero!"
        return ""






# 从ini文件中解析出账号密码信息
_get_item_from_ini()
print(_username)


# 先GET到`登录页面`
_r0 = s.get(_url_loging, headers = headers0)
# 解析GET到的页面中的两个关键元素
# dict_post_params = parse_to_post_params(_r0.content)
# print dict_post_params['__VIEWSTATE']
# print dict_post_params['__EVENTVALIDATION']
VIEWSTATE, EVENTVALIDATION, _url_captcha_tmp = parse_to_post_params(_r0.content)
# 分割出从页面中得到的参数并将其连接到验证码的url上去
_url_captcha = _url_captcha + "?" + _url_captcha_tmp.split('?')[1]
print VIEWSTATE
print EVENTVALIDATION
print "待访问的带随机数字的验证码的url："
print _url_captcha

# 从向这个url发出请求,然后将得到的图片保存到本地
_save_img_from_url(_url_captcha, _file_captcha)
# 解析保存到本地的图片
_result_captcha = _parse_img_to_txt(_file_captcha)
print "验证码："
print _result_captcha

### 注意：即便你已经登录了，你再开一个浏览器标签页，然后发出一个这样的请求之后，那你之前已经登录的那个标签页再刷新的时候也失去了登录状态，返回一个重新登录的页面让你重新登录。

# if session != None:
# r = session.post(url_relogin, headers= headers)
# print r.cookies
# print r.text

# 将解析到的结果告诉url_payload
_url_payload = {
    '__EVENTTARGET': 'ctl00$contentParent$btLogin',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': VIEWSTATE,
    '__EVENTVALIDATION': EVENTVALIDATION,
    'ctl00$contentParent$UserName': _username,
    'ctl00$contentParent$PassWord': _password,
    'ctl00$contentParent$ValidateCode': _result_captcha
}

'''
__EVENTTARGET=ctl00%24contentParent%24btLogin&
__EVENTARGUMENT=&
__VIEWSTATE=%2FwEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg%2FaW1hZ2U9MTkzMTkxNDc0OGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U%3D&
__EVENTVALIDATION=%2FwEdAAZ%2BE1NX%2B%2Fbbjbsz%2BB%2BD%2BrDncybtMhw0mn0LtKqAHeD%2F6LR%2FVkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls%3D&
ctl00%24contentParent%24UserName=s150231003&
ctl00%24contentParent%24PassWord=HBJMcqq2215746&
ctl00%24contentParent%24ValidateCode=0607
'''
# _r = _session.post(_url_relogin, data=_url_payload, headers=headers)
_r = s.post(_url_loging, data= _url_payload, headers=headers)
print _r.url


# 进入登录成功页面
#_r1 = _session.get(_url_loging, headers= headers1)
#print _r1.url

# 如何判断是非已经登陆成功


_r2 = s.get(_url_course_query, headers=headers2)
print _r2.url
#print _r2.content
