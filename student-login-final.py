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

from parser import parse_post_params

# 再用GET去到validateCode.aspx
# 解析验证码之后，将结果告诉url_payload
# 带着这个header，用POST提交到Relogin.aspx(这时解析ini文件中的信息)
# 测试是否登录成功

CONFIG_FILE = 'config.ini'
CONFIG_ITEM_INFO = 'info'

_username = ''
_password = ''
_result_captcha = ''

_url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
_file_captcha = "captcha.png"
_url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
_url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
_url_course_query = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="

_cookie = "Cookie"
_cookie_value = "ASP.NET_SessionId=k3cjuzqhfaojrlf23mjs2qhx; LoginType=LoginType=1; DropDownListXqu=DropDownListXqu=1; DropDownListYx_xsbh=DropDownListYx_xsbh="
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

headers_final = {
    "Accept":     "*/*",
    "Referer":    "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ==",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
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
    # 不要将四个空格喝TAB键混用了

def _save_img_from_url(imageUrl, filename):
    '''
    get the captcha by the url_captcha and save the image as 'captcha.png'
    '''
    r = _session.get(imageUrl)
    # with open(filename, 'w') as fp:
    # shutil.copyfileobj(data, fp)
    f = open(filename, 'wb')
    f.write(r.content)
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
    if is_file_empty(image_file) == False:
        result = pytesseract.image_to_string(Image.open(image_file))
        return result
    # 下面这句print并不会执行
    # print result
    else:
        print "File size zero!"
        return ""






# 全局session，重复利用
_session = requests.session()

# 从ini文件中解析出账号密码信息
_get_item_from_ini()
print(_username)
# 从向这个url发出请求,然后将得到的图片保存到本地
_save_img_from_url(_url_captcha, _file_captcha)
# 解析保存到本地的图片
_result_captcha = _parse_img_to_txt(_file_captcha)
print _result_captcha

# 先GET到`登录页面`
_r0 = _session.get(_url_loging, headers = headers0)
# 解析GET到的页面中的两个关键元素
dict_values = parse_post_params(_r0.content)
print dict_values['__VIEWSTATE']
print dict_values['__EVENTVALIDATION']


### 注意：即便你已经登录了，你再开一个浏览器标签页，然后发出一个这样的请求之后，那你之前已经登录的那个标签页再刷新的时候也失去了登录状态，返回一个重新登录的页面让你重新登录。

# if session != None:
# r = session.post(url_relogin, headers= headers)
# print r.cookies
# print r.text

# 将解析到的结果告诉url_payload
_url_payload = {
    '__EVENTTARGET': 'ctl00$contentParent$btLogin',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': dict_values['__VIEWSTATE'],
    '__EVENTVALIDATION': dict_values['__EVENTVALIDATION'],
    'ctl00$contentParent$UserName': _username,
    'ctl00$contentParent$PassWord': _password,
    'ctl00$contentParent$ValidateCode': _result_captcha
}

# _r = _session.post(_url_relogin, data=_url_payload, headers=headers)
_r = _session.post(_url_loging, data= json.dumps(_url_payload), headers=headers)
print _r.url


# 进入登录成功页面
#_r1 = _session.get(_url_loging, headers= headers1)
#print _r1.url

#_url_axd1 = "http://gs.cqupt.edu.cn:8080/WebResource.axd?d=5d5KGRMAyLvBqg6D0Z6Xhj3Bik0iH8Qt5h7ZqLwbqRWMcG_QNGx9uHHYTzhIEQhPxWH_P8u88WPt72kX0&t=635793306349294682"
#_url_axd2 = "http://gs.cqupt.edu.cn:8080/ScriptResource.axd?d=a8XuVJe3RPmNNezBCV4fnhmFCTQPZUJuIVB1PICLRIFB0h0iFOT51is_Q9pzVzBg5YWBLBKS1CWtbSPylPaRTjWmvnSuN_4Vp_BgSDtPqcL64afEn05pWbSSNySR9Mydpi-0VtLHKkLXQpp5CBE1Sm7fImxVdYLGKHFTJg2&t=72e85ccd"
#_url_axd3 = "http://gs.cqupt.edu.cn:8080/ScriptResource.axd?d=_qZPvnuQ-IwWQrnKXhnIvLRxioe9O-Ab28fk3EAfgQLrvQZtwHiPgSDxbsHi67wW8f6eI0EuCp8CTlwgUL3vc2j57a0O3cWaN1_EDEf2zcEG9MkETRna5PCL5Le_ddeJuIRt7UWsXRMwb7i8yeDTW26c9B0FuBPQG3y93LM-E-2H2qGe0&t=72e85ccd"


#_session.get(_url_axd1, headers = headers_final)
#_session.get(_url_axd2, headers = headers_final)
#_session.get(_url_axd3, headers = headers_final)

# 如何判断是非已经登陆成功


#_r2 = _session.get(_url_course_query, headers=headers2)
#print _r2.text
