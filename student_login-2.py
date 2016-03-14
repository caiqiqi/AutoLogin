# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'
import requests
# import urllib2

def get_cookies():
	url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx"
	headers = {
		"Host": "gs.cqupt.edu.cn:8080",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate",
		"Connection": "keep-alive"

	}
	r = requests.get(url_relogin, headers= headers)
	cookies = r.cookies
	print cookies

	return cookies

url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx"
headers = {
	"Host": "gs.cqupt.edu.cn:8080",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate",
	"Connection": "keep-alive"
}

# 全局session，重复利用
session = requests.session()
if session != None:
	r = session.get(url_relogin, headers= headers)
	print u'Cookie为：'
	print type(r.cookies)
	print r.cookies
	print u'html内容为：'
	#print r.text