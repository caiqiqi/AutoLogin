#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import json
import requests

from parser import parse_to_sessionId
from parser import parse_to_post_params
from parser import check_if_captcha_wrong
import util

#caiqiqi
#普通用户通过浏览器登录`研究生管理系统`的流程:
# 1.GET `default.aspx`.由于在aspx的<script>里将三个个iframe的src属性设置为三个.aspx页面(topmenu.aspx, leftmenu.aspx, loging.aspx),于是,
# 2.GET 上面提到的三个url(其中请求头的referer都是`default.aspx`)
# 3.在发出的三个GET请求之后得到的响应中, 其中`loging.aspx`的响应码是`302 Found`,同时在响应头中的Location的值被设置为`_url_relogin`,
###而其余两个正常返回.aspx页面之后加载到对应的iframe中.
# 4.GET `_url_relogin`, 在返回的响应头中`Set-Cookie`的值被设置为一个"ASP.NET-SessionId:"开头的字符串.由于关键信息sessionid是在
###这里被设置的,所以只需要直接向这个页面发出GET请求,然后抓取这个SessionId的值,然后在之后的请求中带着这个SessionId就可以了.
# ? 另外`_url_captcha` 之后跟着一个九位的随机数,看情况酌情要不要在本地随机生成一个(不确定要不要这样做,因为看到有的网站的js代码里直接写好了生成一个随机数)

dict_user = {
    'username': '',
    'password': ''
}
_str_captcha = ''


# 获取验证码的url
_url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
# 获取验证码之后将其存储在本地图片的文件名
_file_captcha = "captcha.png"
# 登录成功之后跳转到的页面
_url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
# 要登录必须通过这个页面,POST请求也是向这个页面发出
_url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
# 传递的参数
_params_ = {'ReturnUrl': '/gstudent/loging.aspx?undefined'}
# 用于验证你是否已经登录成功(查你选了哪些课)
_url_course_query = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="

_sessionId = ""

_headers_validatecode = {
    "Accept": "image/webp,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Connection": "keep-alive",
    "Cookie": _sessionId,
    "Host": "gs.cqupt.edu.cn:8080",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
}

_headers_post = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": _sessionId,
    "Host": "gs.cqupt.edu.cn:8080",
    "Origin": "http://gs.cqupt.edu.cn:8080",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
}
#"Content-Length": "626",
dict_post_params ={
    '__VIEWSTATE': '',
    '__EVENTVALIDATION': ''
}

# 将解析到的结果告诉url_payload
_url_payload = {
    '__EVENTTARGET': 'ctl00$contentParent$btLogin',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': dict_post_params['__VIEWSTATE'],
    '__EVENTVALIDATION': dict_post_params['__EVENTVALIDATION'],
    'ctl00$contentParent$UserName': dict_user['username'],
    'ctl00$contentParent$PassWord': dict_user['password'],
    'ctl00$contentParent$ValidateCode': _str_captcha
}




# 为了得到SessionId,先得对这个地址进行一次请求
resp1 = requests.get(_url_relogin)
print resp1.headers
# 得到响应头： .headers
dict_resp1_headers = resp1.headers
# 将得到的响应头,分析出它的`SessionId`
_sessionId = parse_to_sessionId(dict_resp1_headers)
# 修改headers
_headers_validatecode["Cookie"] = _sessionId
_headers_post["Cookie"] = _sessionId

# 构造好最终发出验证码请求时的url
_url_captcha_final = _url_captcha + "?" + str(util.gen_random_int())
# 将得到的图片保存到本地
util.save_img_from_url(_url_captcha_final, _headers_validatecode, _file_captcha)
# 解析这张图片
_str_captcha = util.parse_img_to_txt(_file_captcha)

dict_post_params = parse_to_post_params(resp1.content)
dict_user = util.get_items_from_ini()

_url_payload['__VIEWSTATE'] =       dict_post_params['__VIEWSTATE']
_url_payload['__EVENTVALIDATION'] = dict_post_params['__EVENTVALIDATION']
_url_payload['ctl00$contentParent$UserName'] =     dict_user['username']
_url_payload['ctl00$contentParent$PassWord'] =     dict_user['password']
_url_payload['ctl00$contentParent$ValidateCode'] = _str_captcha


resp2 = requests.post(_url_relogin, data = json.dumps(_url_payload), headers = _headers_post)
print "当前所处的url:"
print resp2.url
# dict_resp2_headers = resp2.headers

print resp2.content
check_if_captcha_wrong(resp2.content)


#resp3 = requests.get(_url_loging)
#print "当前所处的url:"
#print resp3.url
#print resp3.headers