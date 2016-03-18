#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import requests
import re

from parser import parse_courses_selected

_url_relogin = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx"


# “开课目录信息查询”
_url_courses_2B_selected = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseOpenDirQuery.aspx?EID=CdRhNRK-zJr3CJv3WDbQaBWEe!jqkgb!AtazZugP2TECqzDZi1FUqQ=="
# “课程网上选课管理”
_url_courses_planed =  "http://gs.cqupt.edu.cn:8080/gstudent/Course/PlanCourseOnlineSel.aspx?EID=f2IawWQYWiguoSkeu5rGyGlX-!Ikp-Iy0PjyBHOHcifgpbJ!LYPpDw=="
# “选课结果信息信息查询”
_url_courses_selected = "http://gs.cqupt.edu.cn:8080/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="

_sessionId_1 = 'k3cjuzqhfaojrlf23mjs2qhx'
_sessionId_2 = 'nembjmva4ig4uw43l0rna5ae'
_list_sessionId = [_sessionId_1, _sessionId_2]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'ASP.NET_SessionId=' + _list_sessionId[1],
    'Host': 'gs.cqupt.edu.cn:8080',
    'Referer': 'http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ==',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
}

# print _list_sessionId[1]
_r = requests.get(_url_courses_selected, headers= headers)
print _r.url

# 将unicode 转化为 str
_r_str = str(_r.url)
# 通过正则表达式判断Response中的url是否为
if re.match(_url_relogin, _r_str) == None:
    # 表示匹配不成功,即返回的页面不是 _url_relogin,则说明已经成功得到想要的页面了,没有被强制跳转
    #print _r.text
    #TODO 解析
    parse_courses_selected(_r.content)
