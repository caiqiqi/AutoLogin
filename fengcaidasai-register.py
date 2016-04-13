#coding=utf-8
__author__ = 'caiqiqi'

import sys
import requests


register_url =        "http://m.hy323220.icoc.in/col.jsp?id=106"
register_post_url =   "http://m.hy323220.icoc.in/ajax/mobiForm_h.jsp"

get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Cache-Control":"max-age=0",
    "Connection": "keep-alive",
    "Host": "m.hy323220.icoc.in",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
}

resp_get = requests.get(register_url, headers=get_headers)
# 先得到CookieJar
cookiejar = resp_get.cookies
cookies_get_dict = {'__cfduid': cookiejar['__cfduid'], '_cliid': cookiejar['_cliid']}

post_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": cookies_get_dict,
    "Host": "m.hy323220.icoc.in",
    "Origin": "http://m.hy323220.icoc.in",
    "Referer": "http://m.hy323220.icoc.in/col.jsp?id=106",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

#接收命令行参数
_name    = sys.argv[0]
_sex     = sys.argv[1]
_colloge = sys.argv[2]
_stuNum  = sys.argv[3]
_phoneNum= sys.argv[4]
_mail    = sys.argv[5]


post_payload = {
    "cmd": "addSubmit",
    "formId": "2",
    "submitContentList": [{"id":0,"val":_name},{"id":1,"val":_sex},{"id":2,"val":_colloge},{"id":3,"val":_stuNum},{"id":4,"val":_phoneNum},{"id":5,"val":_mail}],
    "vCodeId": "3162",
    "validateCode": "undefined",
    "tmpFileList": "[]",
    "_TOKEN": "undefined"
}
resp_post= requests.post(register_post_url, data=post_payload, headers=post_headers)

print "#1: title"
print resp_post.url
print "#2: cookie"
print resp_post.cookies
print "#3: content"
print resp_post.text
