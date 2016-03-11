# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'
import requests
import urllib2
# import shutil
import os
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser

import pytesseract
from PIL import Image


config_file = 'config.ini'
config_item_info = 'info'

def get_item_from_ini():
	cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    username = cf.get(config_item_info, 'username')
    password = cf.get(config_item_info, 'password')

url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
file_captcha = "captcha.png"
url_payload = {
	"__EVENTTARGET": "ctl00$contentParent$btLogin"
	"__EVENTARGUMENT":
	"__VIEWSTATE": "/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MjAwODQ2NTQ5NWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U="
	"__EVENTVALIDATION": "/wEdAAZ25z2YGnHhHaodt21WSyV/cybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=
	"ctl00$contentParent$UserName": username
	"ctl00$contentParent$PassWord": password
	"ctl00$contentParent$ValidateCode": "2222"
}

# 全局session，重复利用
session = requests.session()

def get_cookies():
	'''
	先得到cookies(主要为里得到SessionId)，
	然后再以这个cookies(内置SessionId) 以post方式将三个参数(用户名，密码，验证码)
	发送到 ReLogin.aspx
	'''
	url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx"
	headers = {
		"Host": "gs.cqupt.edu.cn:8080",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate",
		"Connection": "keep-alive"
	}
	if session != null:
		r = session.get(url_relogin, headers= headers)
		cookies = r.cookies
		print cookies

		return cookies

def save_img_from_url(imageUrl, filename):
	'''
	get the captcha by the url_captcha and save the image as 'captcha.png'
	'''
	u = urllib2.urlopen(imageUrl)
	data = u.read()
	#with open(filename, 'w') as fp:
		#shutil.copyfileobj(data, fp)
	f = open(filename, 'wb')
	f.write(data)
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






save_img_from_url(url_captcha, file_captcha)

if is_file_empty(file_captcha)== False:
	result_captcha = pytesseract.image_to_string(Image.open(file_captcha))
	print result_captcha
else:
	print "File size zero!"


