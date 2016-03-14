# -*- coding: utf-8 -*-
'''
模拟学生登录研究生管理系统
'''
import requests
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser
from IPython.display import Image

config_file = 'config.ini'
config_item_cookie = 'cookies'
config_item_info = 'info'

def create_session():
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    cookies = cf.items(config_item_cookie)
    cookies = dict(cookies)
    from pprint import pprint
    pprint(cookies)


    username = cf.get(config_item_info, 'username')
    password = cf.get(config_item_info, 'password')
    # 验证码
    validateCode = ''

    session = requests.session()
    login_data = {
        '__EVENTTARGET': 'ctl00$contentParent$btLogin',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MTgxMzM3MTUwMWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U=',
        '__EVENTVALIDATION': '/wEdAAYLvU43cCGYojBoRpTPnhlWcybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=',
        'ctl00$contentParent$UserName': username,
        'ctl00$contentParent$PassWord': password,
        'ct100$contentParent$ValidateCode': validateCode
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
        'Host': 'gs.cqupt.edu.cn:8080',
        'Referer': 'http://gs.cqupt.edu.cn:8080/gstudent/default.aspx'
    }
    r = session.post('http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx', data=login_data, headers=header,)

    #r = session.get('http://gs.cqupt.edu.cn:8080/gstudent/default.aspx', cookies=cookies) # 实现验证码登陆

    with open('login.html', 'w') as fp:
        fp.write(r.content)

    return session, cookies


if __name__ == '__main__':
    requests_session, requests_cookies = create_session()

    url = 'http://gs.cqupt.edu.cn:8080/gstudent/default.aspx'
    # content = requests_session.get(url).content # 未登陆
    # content = requests.get(url, cookies=requests_cookies).content # 已登陆
    content = requests_session.get(url, cookies=requests_cookies).content # 已登陆
    with open('default.aspx', 'w') as fp:
        fp.write(content)