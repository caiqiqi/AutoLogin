# -*- coding: utf-8 -*-
'''
模拟学生登录研究生管理系统
'''
import requests

url_class_student = 'http://gs.cqupt.edu.cn:8080/Gstudent/Course/ClassStudent.aspx'

list_EID = [
'f2IawWQYWiguoSkeu5rGyGlX-!Ikp-Iy0PjyBHOHcifgpbJ!LYPpDw==', 
'nKxdsUV9wxeu4ldspzWbATTG3PntWJ7BM9HmnKygl-kH8Rxm4chslw==&UID='
]

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Host': 'gs.cqupt.edu.cn:8080',
    'Referer': 'http://gs.cqupt.edu.cn:8080/gstudent/default.aspx'
}

payload = {'EID': list_EID[1]}
print(list_EID[1])
resp = requests.get(url_class_student, params = payload, headers=header)

with open('student_class.html' ,'w') as fp:
    fp.write(resp.content)


