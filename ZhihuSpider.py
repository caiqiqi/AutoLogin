# -*- coding: utf-8 -*-
'''
网络爬虫之用户名密码及验证码登陆：爬取知乎网站
'''
import requests
import ConfigParser

def create_session():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    cookies = cf.items('cookies')
    cookies = dict(cookies)
    from pprint import pprint
    pprint(cookies)


    username = cf.get('info', 'username')
    password = cf.get('info', 'password')
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
    r = session.post('http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx', data=login_data, headers=header)
    if r.json()['r'] == 1:
        print 'Login Failed, reason is:',
        for m in r.json()['data']:
            print r.json()['data'][m]
        print 'So we use cookies to login in...'
        has_cookies = False
        for key in cookies:
            if key != '__name__' and cookies[key] != '':
                has_cookies = True
                break
        if has_cookies is False:
            raise ValueError('请填写config.ini文件中的cookies项.')
        else:
            # r = requests.get('http://www.zhihu.com/login/email', cookies=cookies) # 实现验证码登陆
            r = session.get('http://gs.cqupt.edu.cn:8080/gstudent/default.aspx', cookies=cookies) # 实现验证码登陆

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