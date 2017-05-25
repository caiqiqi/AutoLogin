#! /usr/bin/env python
#coding=utf-8
__author__ = 'caiqiqi'

import sys
import os
import time
from base64 import b64encode as e
from base64 import b64decode as d
import ConfigParser

import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import lxml.html
import lxml.etree #用lxml来代替bs解析
## 参考：http://cangfengzhe.github.io/python/python-lxml.html

from url import *
from headers import *
from utils import color, banner
# 前面的logger是logger.py, 后面的logger是logger对象
from logger import logger

class Info():

    version              = '2.7'
    CONFIG_FILE          = 'config.ini'
    CONFIG_ITEM_INFO     = 'info'
    username            = ''
    password            = ''
    result_captcha      = ''

    file_captcha         = 'captcha.png'
    TIME_OUT             = 10      # for requests, 单位s
    is_login             = False   # 判断是否已登录


cf = ConfigParser.ConfigParser()

s = requests.Session()

def print_options():
    print
    print "  #0  登录日志"
    print "  #1  选课结果"
    print "  #2  课程成绩"
    print "  #3  学期考试"
    print
    print
    print "[*] 请输入对应的序号, 以进行相应的查询! 查询完成后按 [Q/q] 退出 \n"


def get_input():
    # print后面加逗号可以不换行
    print color("QAQ >", "red"),
    cmd = ""
    cmd = raw_input()
    try:
        
        if cmd == "1":
            # 选课结果信息查询
            show_course_selected(s)
            get_input()
        elif cmd == "2":
            # 课程成绩信息查询
            show_course_score(s)
            get_input()
        elif cmd == "3":
            # 学期考试信息查询
            show_course_exam_info(s)
            get_input()
        elif cmd == "0":
            # 登录历史
            show_history(s)
            get_input()
        elif cmd == "q" or cmd == "Q":
            exit(0)
    except Exception as e:
        logger.warning("[!] Exception caught: {}".format(e))


def is_internet_on():
    '''
    判断是否能访问互联网
    '''
    try:
        response = requests.get('http://www.baidu.com',timeout = 3) 
        return True
    except socket.error as e: 
        type, value, traceback = sys.exc_info()[:3] 
        if type == socket.timeout: 
            logger.error( u"[!] socket.timeout错误" )
        else: 
            logger.error( u"[!] 其他socket错误")
    return False

def is_intranet_on():
    '''
    判断能否访问内网
    '''
    try:
        response = requests.get('http://202.202.43.125',timeout = 3) 
        return True
    except socket.error as e: 
        type, value, traceback = sys.exc_info()[:3] 
        if type == socket.timeout: 
            logger.error( u"[!] socket.timeout错误" )
        else: 
            logger.error( u"[!] 其他socket错误")
    return False


def load_info_from_ini():
    '''
    从.ini文件中载入账户密码信息
    '''
    cf.read(Info.CONFIG_FILE)

    Info.username  = cf.get(Info.CONFIG_ITEM_INFO, 'username')
    Info._password  = d(d(d(cf.get(Info.CONFIG_ITEM_INFO, 'password'))))


def save_img_to_file_and_get_result(imageUrl, filename):
    r = s.get(imageUrl, headers=headers_image)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()

    # 判断文件内容是否为空
    file_size = os.stat(filename).st_size
    if 0 != file_size:
        # 将读到的图片转换成文本
        result = pytesseract.image_to_string(Image.open(filename))
        return result
    else:
        logger.error( "[!] 解析验证码错误！\n")
        exit(1)


# 用`BeautifulSoup`解析各种html页面
def parse_html_by_bs(html_str, p_url):

    soup = BeautifulSoup(html_str, "lxml")  # soup 就是BeautifulSoup处理格式化后的字符串
    # 解析`loging`页面, 从中获取 1# VIEWSTATE, 2# EVENTVALIDATION, 3# 验证码带随机数字的url
    if url_loging == p_url:
        __VIEWSTATE         = soup.find(id = "__VIEWSTATE")['value']
        __EVENTVALIDATION   = soup.find(id = "__EVENTVALIDATION")['value']
        __VIEWSTATEGENERATOR= soup.find(id = "__VIEWSTATEGENERATOR")['value']
        _validatecode_url   = soup.find(id = "ctl00_contentParent_ValidateImage")['src']

        return __VIEWSTATE, __EVENTVALIDATION, __VIEWSTATEGENERATOR, _validatecode_url
    # 解析`已选课程`页面, 从中获取已选课程的内容
    elif url_course_selected == p_url:
        print soup.find(id = "ctl00_contentParent_dgData").get_text(separator=u'  ')  # strip=True
    # 解析`课程成绩`页面, 从中获取各科成绩
    elif url_course_score == p_url:
        # unicode类型
        print soup.find(id = "ctl00_contentParent_dgData").get_text(separator=u'  ') # strip=True
    # 解析`考试信息`页面, 从中获取考试信息
    elif url_course_exam_info == p_url:
        print soup.find(id = "ctl00_contentParent_dgData").tr.td.get_text()
    # 解析`登录日志`页面，从中获取登录日志
    elif url_history == p_url:
        print soup.find(id = "ctl00_contentParent_UpdatePanel2").get_text(separator=u'  ') 

#TODO 用`xpath`解析各种html页面
def parse_html_by_xpath(html_str, p_xpath):
    html_xpathed = lxml.html.document_fromstring(html_str).xpath(p_xpath)
    print html_xpathed

def parse_html_by_lxml(html_str, p_xpath):
	root = lxml.html.fromstring(html_str)

# 已选课程查询
def show_course_selected(session):
    response = session.get(url_course_selected, headers = headers_query, timeout = Info.TIME_OUT)
    print "=============== 已选课程 ==============="
    parse_html_by_bs(response.content, url_course_selected)

# 课程成绩查询
def show_course_score(session):
    response = session.get(url_course_score, headers = headers_query, timeout = Info.TIME_OUT)
    print "=============== 课程成绩 ==============="
    parse_html_by_bs(response.content, url_course_score)

# 学期考试信息查询
def show_course_exam_info(session):
    response = session.get(url_course_exam_info, headers = headers_query, timeout = Info.TIME_OUT)
    print "=============== 考试信息 ==============="
    parse_html_by_bs(response.content, url_course_exam_info)

# 登录历史
def show_history(session):
    response = session.get(url_history, headers = headers_query, timeout = Info.TIME_OUT)
    print "=============== 登录日志 ==============="
    parse_html_by_bs(response.content, url_history)

def login(session):
    global url_captcha

    # 先GET到`登录页面`
    r0 = s.get(url_loging, headers = headers_get, timeout = Info.TIME_OUT)
    VIEWSTATE, EVENTVALIDATION, VIEWSTATEGENERATOR, url_captcha_tmp = parse_html_by_bs(r0.content, url_loging)
    # 分割出从页面中得到的参数并将其连接到验证码的url上去
    url_captcha = url_captcha + "?" + url_captcha_tmp.split('?')[1]

    # 从向这个url发出请求,然后将得到的图片保存到本地，最后解析图片成文字
    result_captcha = save_img_to_file_and_get_result(url_captcha, Info.file_captcha)
    if not result_captcha:
        logger.error( "[!] 验证码获取或解析失败 !")
        exit(1)
    logger.info( "[*] 验证码: %s" % result_captcha)

    # 将解析到的结果告诉url_payload
    payload = '__EVENTTARGET=ctl00$contentParent$btLogin&__EVENTARGUMENT=&__VIEWSTATE='+ VIEWSTATE+ '&' + '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR +'&' + '__EVENTVALIDATION='+ EVENTVALIDATION + '&' +'ctl00$contentParent$UserName='+ Info.username + '&' +'ctl00$contentParent$PassWord='+ Info.password + '&' +'ctl00$contentParent$ValidateCode='+ result_captcha
    # 登录
    r1 = s.post(url_relogin, data = payload, headers = headers_post, timeout = Info.TIME_OUT)
    if r1.status_code == 200:
        # 只有返回页面的url跟 `url_loging` 一样, 才是登录成功
        if str(r1.url) == url_loging:
            logger.info( "[*] 登录成功 !\n")
            return True
        else:  # 登录失败
            bad_login(r1)
            return False
    else:  # 登录失败
        bad_login(r1)
        return False

def bad_login(response):
    logger.info( "[!] 登录失败 ! 状态码: %d\n" % response.status_code)
    logger.info ("[!] 当前url为: %s\n" % str(response.url))
    #exit(1)


def main():
    load_info_from_ini()  # 从ini文件中解析出账号密码信息

    # 若未登录，则循环进行登录操作
    while not Info.is_login:
        time.sleep(3)
        logger.info( "[!] 未登录")
        logger.info ("[*] 正在登录...")
        Info.is_login = login(s)
        if Info.is_login:
            break

    logger.info( "[*] 已登录")
    print_options()   # 打印可用选项
    get_input()       # 解析用户输入


if __name__ == "__main__":
    logger.info( banner(Info.version))
    main()
