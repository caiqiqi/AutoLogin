#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import os

# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup


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
_url_exam_info    = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseTestInfo.aspx?EID=wlt4FUXSIZqP8ASNy5fY7O3mF9B6EclOO8VWx82rzmj1PxzhUTNKUg=="


headers0 = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Upgrade-Insecure-Requests": "1",
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
headers_post = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn:8080",
    "Origin": "http://gs.cqupt.edu.cn:8080",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"
}

# 查询课程详情的
headers_query = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
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

def parse_to_post_params(html_str):
    '''
    从 html_str中解析出三个参数
    1. __VIEWSTATE,
    2. __EVENTVALIDATION,
    3. 验证码带随机数字的url
    '''

    ID_VIEWSTATE = "__VIEWSTATE"
    ID_EVENTVALIDATION = "__EVENTVALIDATION"
    ID_VALIDATECODE = "ctl00_contentParent_ValidateImage"

    # soup 就是BeautifulSoup处理格式化后的字符串
    soup = BeautifulSoup(html_str, "lxml")
    
    # 得到VIEWSTATE的值
    value_VIEWSTATE         = soup.find(id= ID_VIEWSTATE)['value']
    # 得到EVENTVALIDATION的值
    value_EVENTVALIDATION   = soup.find(id = ID_EVENTVALIDATION)['value']
    # 得到验证码带随机数字的url
    value_validatecode_url  = soup.find(id = ID_VALIDATECODE)['src']

    return value_VIEWSTATE, value_EVENTVALIDATION, value_validatecode_url


def main():
    global _url_captcha
    global _result_captcha
    # 从ini文件中解析出账号密码信息
    _get_item_from_ini()
    print(_username)


    # 先GET到`登录页面`
    _r0 = s.get(_url_loging, headers = headers0)
    VIEWSTATE, EVENTVALIDATION, url_captcha_tmp = parse_to_post_params(_r0.content)
    # 分割出从页面中得到的参数并将其连接到验证码的url上去
    _url_captcha = _url_captcha + "?" + url_captcha_tmp.split('?')[1]
    print VIEWSTATE
    print EVENTVALIDATION
    print "待访问的带随机数字的验证码的url："
    print _url_captcha

    # 从向这个url发出请求,然后将得到的图片保存到本地，最后解析图片成文字
    _result_captcha = save_img_to_file_and_get_result(_url_captcha, _file_captcha)

    print "验证码："
    print _result_captcha



    # 将解析到的结果告诉url_payload
    payload = '__EVENTTARGET=ctl00$contentParent$btLogin&__EVENTARGUMENT=&__VIEWSTATE='+ VIEWSTATE+ '&' +'__EVENTVALIDATION='+ EVENTVALIDATION + '&' +'ctl00$contentParent$UserName='+ _username + '&' +'ctl00$contentParent$PassWord='+ _password + '&' +'ctl00$contentParent$ValidateCode='+ _result_captcha

    # 登录
    r1 = s.post(_url_relogin, data= payload, headers=headers_post)
    print r1.url

    # 课程查询
    r2 = s.get(_url_course_query, headers=headers_query)
    print r2.url
    # 考试查询
    r3 = s.get(_url_exam_info, headers=headers_query)
    print r3.url
    print r3.content

    # TODO: 进行后续任意已登录的操作

if __name__ == "__main__":
    main()
