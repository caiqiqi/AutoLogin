#coding=utf-8
'''
url_course_selected:  选课结果信息查询
url_course_score:     课程成绩信息查询
url_course_exam_info: 学期考试信息查询
url_history         : 登录历史
'''

url_base     = "http://gs.cqupt.edu.cn"

url_captcha  = url_base + "/Public/ValidateCode.aspx"
url_login_post = url_base+ "/"
#url_loging   = url_base + "/gstudent/loging.aspx?undefined"
#url_relogin  = url_base + "/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"

url_exit = url_base+ "/UserLogin.aspx?exit=1"

url_course_selected  = url_base + "/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="
url_course_score     = url_base + "/gstudent/Course/StudentScoreQuery.aspx?EID=OYCzqNQgp9KLbeePzWGaybPEvIYjIwL3qIu7s7NFViZvF2I21gvMWg=="
url_course_exam_info = url_base + "/gstudent/Course/CourseTestInfo.aspx?EID=wlt4FUXSIZqP8ASNy5fY7O3mF9B6EclOO8VWx82rzmj1PxzhUTNKUg=="
# 个人基本信息管理
url_self_info_mgm = url_base + "/Gstudent/Individual/Student_Info.aspx?EID=IhQSXbQR6iQ2d3FALhnQtp7i6wtSsYlo-P77fS9kan-HRr3Mw0W0ww=="
# 登录密码信息修改
url_login_passwd_modi = url_base +      "/Gstudent/Individual/StuPwd_Edit.aspx?EID=cs3!AlV6-ppx7YZD3gdxMqpSpZrnm01uf8vmBH5b5F9Gdqx2Pe0Vag=="
# 通过email获取某帐号的登录密码
url_email_get_passwd = url_base + "/Public/EmailGetPasswd.aspx?EID=07NAyBe51SA="

# 论文开题报告管理
url_paper_open_mgm = url_base + "/Gstudent/Topic/Topic_Manage.aspx?EID=lmtSFlI-bjmfMQRDeoE6Xuuzz4O16owg8OcRzDqDYSg="
# 论文中期报告管理
url_paper_mid_mgm = url_base + "/Gstudent/LwMid/Lwzq_Manage.aspx?EID=1!Q97mzyi41Gk79Lo3Py3zOsxUQdafm8I0AVohyamXw="
# 学位论文评审报名
url_paper_evaluat_sign = url_base + "/Gstudent/Audit/Audit_Bm.aspx?EID=ZkOadKjhKS0h7JwvUSS3mO9l6D48TqNX9RLRz4Xf5!Y="
# 学位论文答辩管理
url_paper_reply_mgm = url_base + "/Gstudent/Reply/Reply_Manage.aspx?EID=sC8G-4gl-8DFdHAf7AatzSH9pzlbtZ53g-WWE5UDMoY="
# 优秀论文申请管理
url_excel_paper_sign_mgm = url_base + "/Gstudent/ExcelLw/ExcelLw_Manage.aspx?EID=KC8vQm4a4p24RWVSGbRN1nlWluF6PrDXn68Wto9zGKYtd4y3nsGtAQ=="
# 存档论文文档上传
url_paper_doc_upload = url_base + "/Gstudent/ElseManage/Article_InArch.aspx?EID=OnTa7D5rEQEiTa3cNp3kw7saFwGS0TJDnnDtc0mAomSyC!NV-KvnCA=="
# 学位申请信息管理
url_degree_sign_mgm = url_base + "/Gstudent/Degree/Degree_Manage.aspx?EID=S2R0owfPH!h902SZs-9DCwd3qPevPjGhzkz4!IpYnrREd9fsBrRliA=="
# 电子注册信息核对
url_signup_info_check = url_base + "/Gstudent/Degree/GradCheck_xlss.aspx?EID=o6pvZK!UAQoOgIEJPTpJximEGwBQUa20nA!DAJTEoQXBa5h63YGQ4g=="



url_history = url_base + "/gstudent/Message/Login_Log.aspx?EID=v4Uk3409ri6XufRM3!utuB3tABwxUpGaytJfxWL3xeY="


'''
headers_get:    GET到登录页面用到的
headers_image:  获取验证码图片用到的
headers_post:   模拟登录时要POST给登录页面的
headers_query:  查询用的
'''

headers_get = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn",
    "Upgrade-Insecure-Requests": "1",
}

headers_image = {
    "Host": "gs.cqupt.edu.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "*/*",
    "Referer": url_login_post,
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4"
} 

headers_post = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn",
    "Origin": "http://gs.cqupt.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "Referer": url_exit
}

headers_edit_passwd_post = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn",
    "Origin": "http://gs.cqupt.edu.cn",
    "X-Requested-With": "XMLHttpRequest",
    "X-MicrosoftAjax": "Delta=true",
    "Referer": "http://gs.cqupt.edu.cn/Gstudent/Individual/StuPwd_Edit.aspx?EID=cs3!AlV6-ppx7YZD3gdxMqpSpZrnm01uf8vmBH5b5F9Gdqx2Pe0Vag=="
}

headers_query = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "gs.cqupt.edu.cn",
    "Origin": "http://gs.cqupt.edu.cn"
}