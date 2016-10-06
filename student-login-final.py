#! /usr/bin/env python
#coding=utf-8
__author__ = 'caiqiqi'

import sys
import os
import ConfigParser

import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup

from url import *
from headers import *


version          = '2.0'

CONFIG_FILE      = 'config.ini'
CONFIG_ITEM_INFO = 'info'

_username        = ''
_password        = ''
_result_captcha  = ''

file_captcha     = 'captcha.png'

# for requests
TIME_OUT         = 5

# 开始就用一个session来维持整个回话，这样在之后请求中可以沿用之前的headers，
# 而且可以往headers里添加已有的字段以覆盖之前的字段，这样connection才是 *keep-alive*，而不是*close*
s = requests.Session()


def print_help(version):
    print "-------------------------------------"
    print "[*] student-login v{} by CaiQiqi :)".format(version)
    print
    print " --course-selected || -c       Show courses you have already selected in this semester."
    print " --course-score || -s          Show the scores of all your courses."
    print " --course-exam-info || -i      Show your exam info of this semester, if any."
    print " --help || -h                  Print this help message."


def print_options():
    print
    print "  #1  选课结果"
    print "  #2  课程成绩"
    print "  #3  学期考试"
    print
    print
    print "[*] 请输入对应的序号, 以进行相应的查询! 查询完成后按 [Q/q] 退出 \n"
    

def get_input():
    # print后面加逗号可以不换行
    print ">" ,
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
        elif cmd == "q" or cmd == "Q":
            exit(0)
    except Exception as e:
        print "[!] Exception caught: {}".format(e)
        #print "[!] 请输入可选的选项!"




def parse_cmd():
    try:
        if sys.argv[1] == "--course-selected" or sys.argv[1] == "-c":
            show_course_selected()
        elif sys.argv[1] == "--course-score" or sys.argv[1] == "-s":
            show_course_score()
        elif sys.argv[1] == "--course-exam-info" or sys.argv[1] == "-i":
            show_course_exam_info()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print_help(version)
    
    except IndexError:
        print "[!] 请检查参数个数, 输入 --help 或者 -h查看帮助信息"
        exit(1)



def _get_item_from_ini():
    '''
    从.ini文件中载入账户密码信息
    '''
    global _username
    global _password

    cf = ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)
    _username = cf.get(CONFIG_ITEM_INFO, 'username')
    _password = cf.get(CONFIG_ITEM_INFO, 'password')


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
        print "[!] 解析验证码错误！\n"
        exit(1)



# 解析各种html页面
def parse_html(html_str, p_url):

    soup = BeautifulSoup(html_str, "lxml")  # soup 就是BeautifulSoup处理格式化后的字符串
    # 解析`loging`页面, 从中获取 1# VIEWSTATE, 2# EVENTVALIDATION, 3# 验证码带随机数字的url
    if url_loging == p_url:
        __VIEWSTATE         = soup.find(id = "__VIEWSTATE")['value']
        __EVENTVALIDATION   = soup.find(id = "__EVENTVALIDATION")['value']
        _validatecode_url   = soup.find(id = "ctl00_contentParent_ValidateImage")['src']

        return __VIEWSTATE, __EVENTVALIDATION, _validatecode_url
    # 解析`已选课程`页面, 从中获取已选课程的内容
    elif url_course_selected == p_url:
        return soup.find(id = "ctl00_contentParent_dgData")
    # 解析`课程成绩`页面, 从中获取各科成绩
    elif url_course_score == p_url:
        return soup.find(id = "ctl00_contentParent_dgData")
    # 解析`考试信息`页面, 从中获取考试信息
    elif url_course_exam_info == p_url:
        return soup.find(id = "ctl00_contentParent_dgData")


# 已选课程查询
def show_course_selected(session):
    response = session.get(url_course_selected, headers = headers_query, timeout = TIME_OUT)
    print "[*] 已选课程"
    print parse_html(response.content, url_course_selected)

# 课程成绩查询
def show_course_score(session):
    response = session.get(url_course_score, headers = headers_query, timeout = TIME_OUT)
    print "[*] 课程成绩"
    print parse_html(response.content, url_course_score)

# 学期考试信息查询
def show_course_exam_info(session):
    response = session.get(url_course_exam_info, headers = headers_query, timeout = TIME_OUT)
    print "[*] 考试信息"
    print parse_html(response.content, url_course_exam_info)



def main():
    global url_captcha
    global _result_captcha

    _get_item_from_ini()  # 从ini文件中解析出账号密码信息
    print(_username)


    # 先GET到`登录页面`
    r0 = s.get(url_loging, headers = headers_get, timeout = TIME_OUT)
    VIEWSTATE, EVENTVALIDATION, url_captcha_tmp = parse_html(r0.content, url_loging)
    # 分割出从页面中得到的参数并将其连接到验证码的url上去
    url_captcha = url_captcha + "?" + url_captcha_tmp.split('?')[1]

    # 从向这个url发出请求,然后将得到的图片保存到本地，最后解析图片成文字
    _result_captcha = save_img_to_file_and_get_result(url_captcha, file_captcha)
    if not _result_captcha:
        print "[!] 验证码获取或解析失败 !"
        exit(1)
    print "[*] 验证码: %s\n" % _result_captcha



    # 将解析到的结果告诉url_payload
    payload = '__EVENTTARGET=ctl00$contentParent$btLogin&__EVENTARGUMENT=&__VIEWSTATE='+ VIEWSTATE+ '&' +'__EVENTVALIDATION='+ EVENTVALIDATION + '&' +'ctl00$contentParent$UserName='+ _username + '&' +'ctl00$contentParent$PassWord='+ _password + '&' +'ctl00$contentParent$ValidateCode='+ _result_captcha

    # 登录
    r1 = s.post(url_relogin, data = payload, headers = headers_post, timeout = TIME_OUT)
    if r1.status_code == 200:
        # 只有返回页面的url跟 `url_loging` 一样, 才是登录成功
        if str(r1.url) == url_loging:
            print "[*] 登录成功 !\n"
        else:
            print "[!] 登录失败 ! 状态码: %d\n" % r1.status_code
            print "[!] 当前url为: %s\n" % str(r1.url)
            exit(1)
    else:
        print "[!] 登录失败 ! 状态码: %d\n" % r1.status_code
        print "[!] 当前url为: %s\n" % str(r1.url)
        exit(1)

    # 解析命名行参数
    #parse_cmd()

    # 打印可用选项
    print_options()
    # 解析用户输入
    get_input()


if __name__ == "__main__":
    main()
