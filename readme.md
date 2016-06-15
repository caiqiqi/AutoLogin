# 主要是用于学校研究生管理系统的自动登录
YouTube地址：https://www.youtube.com/watch?v=6u05g--r_78 </br>
秒拍视频：http://weibo.com/p/230444427857313e89770690bec69367024c29

## student-login-final.py
<p>通过Chrome/Firefox的开发者工具以及Burp Suite分析登录过程的HTTP通信细节，然后用python实现对目标网站在给定学号密码情况下的自动登录。</br> </p>
- ConfigParser:  用于从.ini文件中读取用户名和密码
- requests: 关键库。用于进行HTTP请求(GET/POST)。可带headers(HTTP请求头)，data(POST时带的表单信息)。
- pytesseract: 开源图像识别库。它的image_to_string()可以将一个PIL.Image包装的图片文件识别出其中的文字信息，并返回该字符串。
- bs4.BeautifulSoup: 解析xml/html的库。这里用于查找hidden的'__VIEWSTATE' 和 'EVENTVALIDATION'。也可用lxml或者正则re。

