# 主要是用于学校研究生管理系统的自动登录
YouTube地址：https://www.youtube.com/watch?v=K4LTgzm9G3w </br>
秒拍视频：http://weibo.com/p/230444427857313e89770690bec69367024c29 </br>

## 用法
### 配置登录帐号密码
在登录脚本所在目录配置`config.ini`  格式为: </br>
```
[info]
username = XXXXX
password = XXXXX
```
### 参数
```
--course-selected || -c       Show courses you have already selected in this semester.
--course-score || -s          Show the scores of all your courses.
--course-exam-info || -i      Show your exam info of this semester, if any.
--help || -h                  Print this help message.
```

## student-login-final.py
通过Chrome/Firefox的开发者工具以及Burp Suite分析登录过程的HTTP通信细节，然后用python实现对目标网站在给定学号密码情况下的自动登录。</br>
## 思路
分析整个HTTP通信过程。实际用浏览器登录时由于有各种css/js/png文件，还有像WebResource.axd，ScriptResource.axd这种让你迷惑不知重不重要的文件。通过分析和实验，发现主要有三个HTTP请求。</br>
1. 先请求登录页面 `http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined` </br>如果已登录未退出这个session还是已登录的状态，或者登录过期这个session虽然已失效但是sessionId还在，这种情况下不会新建session，而是沿用之前的session，服务器端返回的请求中不会『Set-cookie』。如果不是以上情况，则会在这第一次请求之后服务器在返回的响应中通过『Set-cookie』发给客户端一个cookie，这个cookie的内容就是这次session的sessionId。如果直接用requests库的get/post方法，则会在headers(HTTP的请求头)中将connection字段设置为closed，这样不利用之后的请求沿用之前的cookie以保持同一次session，导致服务器在登录认证的过程中不能将之后的请求与之前的请求联系起来，最终返回302重定向到这个页面 `http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined` </br> 让用户重新登录从而登录失败。</br>
在第一次发出的get请求后还要从返回的html页面中找出三个重要参数供后续的请求中用到。这三个参数是：登录的最后一步提交post请求时的表单里的数据*__VIEWSTATE*和*EVENTVALIDATION*字段；以及第二次get请求图片验证码时用到的`?image=124685645`类似这样的参数。</br>
2. 然后请求验证码页面，即访问一个.aspx页面并带一个随机参数(这个参数并不是像有些网站一样通过前端的js文件中的Math.random()随机产生)。由于我并不知道服务器端生成这个随机参数的逻辑，于是我只能通过分析返回的html页面中找出下一步要请求的验证码页面。然后通过requests.Session.get()发出请求，将得到的图片存入本地文件，然后打开这个文件用`pytesseract`这个库来将图片内容解析成文字。
3. 登录的最后一步就是将之前搜集的几个重要参数加上用户名，密码，验证码post到指定的url `http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx?ReturnUrl=/gstudent/loging.aspx?undefined` </br>注意这里不是提交到这里`http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined` </br>(这里碰到过坑所以提一下)
然后通过打印出当前页面的url可以看出是否已经登录了。然后就可以做任意已登录的操作了。

- **ConfigParser**:  用于从.ini文件中读取用户名和密码
- **requests**: 关键库。用于进行HTTP请求(GET/POST)。可带headers(HTTP请求头)，data(POST时带的表单信息)。
- **pytesseract**: 开源图像识别库。它的image_to_string()可以将一个PIL.Image包装的图片文件识别出其中的文字信息，并返回该字符串。
- **bs4.BeautifulSoup**: 解析xml/html的库。这里用于查找hidden的*__VIEWSTATE* 和 *EVENTVALIDATION*。也可用lxml或者正则re。

