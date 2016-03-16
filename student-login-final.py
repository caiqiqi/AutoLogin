# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'
import requests
import urllib2
import json
# import shutil
import os
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser

import pytesseract
from PIL import Image


# 再用GET去到validateCode.aspx
# 解析验证码之后，将结果告诉url_payload
# 带着这个header，用POST提交到Relogin.aspx(这时解析ini文件中的信息)
# 测试是否登录成功


config_file = 'config.ini'
config_item_info = 'info'

username = ''
password = ''
result_captcha = ''

url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
file_captcha = "captcha.png"

# 全局session，重复利用
# session = requests.session()

def get_item_from_ini():
	'''
	从.ini文件中载入账户密码信息
	'''
	cf = ConfigParser.ConfigParser()
	cf.read(config_file)
	username = cf.get(config_item_info, 'username')
	password = cf.get(config_item_info, 'password')
    # 不要将四个空格喝TAB键混用了
	print "从.ini文件中读取账户密码信息..."
	print(username)
	print(password)

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

def parse_img_to_txt():
	if is_file_empty(file_captcha)== False:
		result = pytesseract.image_to_string(Image.open(file_captcha))
		return result
		# 下面这句print并不会执行
		# print result
	else:
		print "File size zero!"


get_item_from_ini()
save_img_from_url(url_captcha, file_captcha)
result_captcha = parse_img_to_txt()
print result_captcha

# 将解析到的结果告诉url_payload
url_payload = {
	"__VIEWSTATE": "/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUqfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9NDQzMTExNjY4ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFIWN0bDAwJGNvbnRlbnRQYXJlbnQkVmFsaWRhdGVJbWFnZQ==",
	"__EVENTVALIDATION": "/wEdAAbMtF0d3Y2cTjUXfEcqyS4TcybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=",
	"ctl00$contentParent$UserName": username,
	"ctl00$contentParent$PassWord": password,
	"ctl00$contentParent$ValidateCode": result_captcha
}


#"__VIEWSTATE:/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MjEyNTM0ODg0MWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U=
#__EVENTVALIDATION:/wEdAAZH+6jAUgvVRayvuTw9Z0CkcybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls="

# url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=%2fgstudent%2floging.aspx%3fundefined"
url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
### 注意：即便你已经登录了，你再开一个浏览器标签页，然后发出一个这样的请求之后，那你之前已经登录的那个标签页再刷新的时候也失去了登录状态，返回一个重新登录的页面让你重新登录。
headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "ASP.NET_SessionId=k3cjuzqhfaojrlf23mjs2qhx; LoginType=LoginType=1; DropDownListXqu=DropDownListXqu=1; DropDownListYx_xsbh=DropDownListYx_xsbh=",
	"Host": "gs.cqupt.edu.cn:8080",
	"Origin": "http://gs.cqupt.edu.cn:8080",
	"Upgrade-Insecure-Requests": "1",
	"Content-Type": "application/x-www-form-urlencoded",
	"Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
}


# 全局session，重复利用
session = requests.session()
#if session != None:
	#r = session.post(url_relogin, headers= headers)
	#print r.cookies
	# print r.text

r = session.post(url_relogin, data=json.dumps(url_payload), headers = headers)
print r.content

# 进入登录成功页面
headers1 = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "ASP.NET_SessionId=k3cjuzqhfaojrlf23mjs2qhx; LoginType=LoginType=1; DropDownListXqu=DropDownListXqu=1; DropDownListYx_xsbh=DropDownListYx_xsbh=",
	"Host": "gs.cqupt.edu.cn:8080",
	"Upgrade-Insecure-Requests": "1",
	"Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
}

url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
#r1 = session.get(url_loging, headers= headers1)
#print r1.content

# 如何判断是非已经登陆成功

url_course_query = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="

headers2 = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate",
	"Upgrade-Insecure-Requests": "1",
	"Cache-Control": "max-age=0" ,
	"Connection": "keep-alive",
	"Host": "gs.cqupt.edu.cn:8080",
	"Origin": "http://gs.cqupt.edu.cn:8080"
}
r2 = session.get(url_course_query, headers = headers2)
print r2.text

