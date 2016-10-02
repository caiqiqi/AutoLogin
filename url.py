#coding=utf-8
'''
url_course_selected:  选课结果信息查询
url_course_score:     课程成绩信息查询
url_course_exam_info: 学期考试信息查询
'''

url_base     = "http://gs.cqupt.edu.cn:8080"

url_captcha  = url_base + "/Public/ValidateCode.aspx"
url_loging   = url_base + "/gstudent/loging.aspx?undefined"
url_relogin  = url_base + "/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined"

url_course_selected  = url_base + "/gstudent/Course/CourseSelQuery.aspx?EID=Ng!0IdeEcMBa4v7gTkZteOPL5Mjmu7TIBdO8k2iXxW479MCMokufJQ=="
url_course_score     = url_base + "/gstudent/Course/StudentScoreQuery.aspx?EID=OYCzqNQgp9KLbeePzWGaybPEvIYjIwL3qIu7s7NFViZvF2I21gvMWg=="
url_course_exam_info = url_base + "/gstudent/Course/CourseTestInfo.aspx?EID=wlt4FUXSIZqP8ASNy5fY7O3mF9B6EclOO8VWx82rzmj1PxzhUTNKUg=="