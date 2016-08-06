#encoding=utf-8

__author__ = 'caiqiqi'

import os
import re

import ConfigParser # ConfigParser 用于从.ini文件中读取信息的

import pytesseract
from PIL import Image # 用来解析验证码

from bs4 import BeautifulSoup

import requests
import urllib
import urllib2
import cookielib

CONFIG_FILE = 'config.ini'
CONFIG_ITEM_INFO = 'info'

_username = ''
_password = ''
_result_captcha = ''
_file_captcha = 'captcha.png'

VIEWSTATE = ''
EVENTVALIDATION = ''

url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
url_loging  = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"


def get_item_from_ini():
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


def save_img_to_file_and_get_result(imageUrl, filename):
    r = requests.get(imageUrl)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()

    # 判断文件内容是否为空
    file_size = os.stat(filename).st_size
    if 0 != file_size:
    	# 将读到的图片转换成文本
    	result = pytesseract.image_to_string(Image.open(filename))
    	print result
    	return result
    else:
    	print "解析验证码错误！"


def parse_to_post_params1(html_str):
    '''
    从 html_doc中解析出两个参数
    :param html_doc: 待解析的html页面
    :return: 包含两个已解析的参数的字典
    '''

    TAG_INPUT = 'input'
    ID_VIEWSTATE = "__VIEWSTATE"
    ID_EVENTVALIDATION = "__EVENTVALIDATION"

    # soup 就是BeautifulSoup处理格式化后的字符串
    soup = BeautifulSoup(html_str, "lxml")
    # 找到所有`input`标签,find_all 函数返回的是一个序列
    soup.find_all(TAG_INPUT)
    # 得到VIEWSTATE的值
    value_VIEWSTATE = soup.find(id= ID_VIEWSTATE)['value']
    # 得到EVENTVALIDATION的值
    value_EVENTVALIDATION= soup.find(id = ID_EVENTVALIDATION)['value']

    return value_VIEWSTATE, value_EVENTVALIDATION

def parse_to_post_params(html_str):
    VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', html_str,re.I)
    EVENTVALIDATION =re.findall(r'input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', html_str,re.I)
    return VIEWSTATE[0], EVENTVALIDATION[0]

def get_login_page(html_str):
	global VIEWSTATE
	global EVENTVALIDATION
	# 先GET到`登录页面`
	# r0 = requests.get(login_url, headers = headers0)
	# 解析GET到的页面中的两个关键元素
	# dict_post_params = parse_to_post_params(_r0.content)
	# print dict_post_params['__VIEWSTATE']
	# print dict_post_params['__EVENTVALIDATION']
	VIEWSTATE, EVENTVALIDATION = parse_to_post_params(html_str)
	print VIEWSTATE
	print EVENTVALIDATION


def do_request(relogin_url, post_url, img_result):
    
    global VIEWSTATE
    global EVENTVALIDATION

    cookie = cookielib.CookieJar()  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
 

    headers0 = {
	    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	    "Accept-Encoding": "gzip, deflate",
	    "Connection": "keep-alive",
	    "Host": "gs.cqupt.edu.cn:8080",
	    "Upgrade-Insecure-Requests": "1"
	}
	# 先访问登录页面，为了得到`VIEWSTATE`和 `EVENTVALIDATION`
    req1 = urllib2.Request(url= relogin_url)
    response1 = opener.open(req1)
    page_str = response1.read()
    print page_str

    VIEWSTATE, EVENTVALIDATION = parse_to_post_params(page_str)
    print VIEWSTATE
    print EVENTVALIDATION
	#需要POST的数据，
    postdata = urllib.urlencode({  
        '__EVENTTARGET': 'ctl00$contentParent$btLogin',
    	'__EVENTARGUMENT': '',
        '__VIEWSTATE': VIEWSTATE,
        '__EVENTVALIDATION': EVENTVALIDATION,
        'ctl00$contentParent$UserName': _username,
    	'ctl00$contentParent$PassWord': _password,
    	'ctl00$contentParent$ValidateCode': img_result
    })
    # 要POST给登录页面的
    # "Connection": "keep-alive",
    headers = {
	    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
	    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	    "Accept-Encoding": "gzip, deflate",
	    "Cache-Control": "max-age=0",
	    "Host": "gs.cqupt.edu.cn:8080",
	    "Origin": "http://gs.cqupt.edu.cn:8080",
	    "Upgrade-Insecure-Requests": "1",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
	}

    #自定义一个请求#
    req2 = urllib2.Request(url= post_url, data= postdata, headers= headers)
    #访问该链接#
    response2 = opener.open(req2)
    #打印返回的内容#
    print response2.geturl
    print response2.getcode
    a = response2.read()


if __name__ == '__main__':
	get_item_from_ini()
	# 得到解析后的验证码
	_result_captcha = save_img_to_file_and_get_result(url_captcha, _file_captcha)
	# 将要post的url和解析过后的验证码传入进去
	do_request(url_relogin, url_loging, _result_captcha)