# 学校研究生管理系统的自动登录
YouTube地址：https://www.youtube.com/watch?v=K4LTgzm9G3w </br>
秒拍视频：http://weibo.com/p/230444427857313e89770690bec69367024c29 </br>

## Demo
![](img/dev-v2.5-demo.png)

## 用法
### 配置登录帐号密码
在登录脚本所在目录配置`config.ini`  格式为: </br>
```
[info]
username = XXXXX
password = XXXXX
```

- `pytesseract` 用于识别验证码
- `requests` 用于HTTP请求并维持session
- `bs4.BeautifulSoup` 用于解析html
----------
5月27日临晨更新
----------
## 关于headers
发现登录成功之后的响应headers中会有这样几个字段。
```
#这时表示不过期吗?
Expires: -1
#登录成功只是在之前的cookie基础(ASPSessionId)上加了一句LoginType=LoginType=1来标识该sessionid登录了
#然后过期时间是一周以后?
Set-Cookie: LoginType=LoginType=1; expires=Fri, 02-Jun-2017
```
## 关于一个奇怪的响应
参考：
https://stackoverflow.com/questions/25308551/how-is-a-redirect-response-handled-by-the-client-using-aspx-forms
### 第一次
```
...
Content-Length: 79

1|#||4|54|pageRedirect||http%3a%2f%2fgs.cqupt.edu.cn%2fGstudent%2fDefault.aspx|
```
### 第二次
```
...
Content-Length: 1531

1|#||4|290|updatePanel|UpdatePanel2|
                                        <a id="btLogin" tabindex="4" title="ç»å½ç³»ç»" href="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;btLogin&quot;, &quot;&quot;, true, &quot;&quot;, &quot;&quot;, false, true))">ç»å½</a>
					 
					                                     |0|hiddenField|__EVENTTARGET||0|hiddenField|__EVENTARGUMENT||0|hiddenField|__LASTFOCUS||364|hiddenField|__VIEWSTATE|/wEPDwULLTEyODk3MDA4NTUPZBYCAgMPZBYGAg0PZBYCZg9kFgICAQ8PFgIeCEltYWdlVXJsBSt+L1B1YmxpYy9WYWxpZGF0ZUNvZGUuYXNweD9pbWFnZT0xNzQ2NjYyMjUxZGQCEQ9kFgJmD2QWAgIBDxBkZBYBZmQCFQ9kFgJmD2QWAgIBDw8WAh4LTmF2aWdhdGVVcmwFLX4vUHVibGljL0VtYWlsR2V0UGFzc3dkLmFzcHg/RUlEPTA3TkF5QmU1MVNBPWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ1WYWxpZGF0ZUltYWdl7QBC+8lMZBwAII4oW0QYB9JCV0Y=|8|hiddenField|__VIEWSTATEGENERATOR|7A1355CA|248|hiddenField|__EVENTVALIDATION|/wEdAAp8qhZyYKwH4YbGWObE+0k/tBkakX23YAyFtnbSLK+q20dSwSl9T9cYdvdEUMk3rEUGvkTgTBH+3oFe+9r/kbESVLz6L5LCYFLkJ6flg//uC0CspgRGmYFcPa3w4gGjNaKVioSYXqFJqLjqkAs5cE0jVpUE8Nw3L5jC2NzwKhaAPrhUk8uaMwhBuFwcS/2JHqdHIAvyK8Ja/XfFTm2/DJ2D8KUpwz0gDkTGG6MTaAwiR6BXBkE=|0|asyncPostBackControlIDs|||0|postBackControlIDs|||59|updatePanelIDs||tUpdatePanel1,,tUpdatePanel3,,tUpdatePanel2,,tUpdatePanel4,|0|childUpdatePanelIDs|||13|panelsToRefreshIDs||UpdatePanel2,|2|asyncPostBackTimeout||90|23|formAction||./UserLogin.aspx?exit=1|59|scriptStartupBlock|ScriptContentNoTags|$.dialog.tips('',0.01,'');$.dialog.alert('éªè¯ç è¾å¥éè¯¯ï¼è¯·éæ°è¾å¥!');|
```
## 关于__VIEWSTATE
> asp.net巧妙的改变了这一点. 当我们在写一个asp.net表单时, 一旦标明了 form runat=server ,那么,asp.net就会自动在输出时给页面添加一个隐藏域
> ```<input type="hidden" name="__VIEWSTATE" value="">```
> 那么,有了这个隐藏域,页面里其他所有的控件的状态,包括页面本身的一些状态都会保存到这个控件值里面. 每次页面提交时一起提交到后台,asp.net对其中的值进行解码,然后输出时再根据这个值来恢复各个控件的状态. 我们再看这个控件的value值,它可能类似如下的形式:Oz4+O2w8aTwxPjs+O2w8.... 
> 很多人会认为这是加密的信息,其实不是, ms仅仅是给各个控件和页面的状态存入适当的对象里面,然后把该对象序列化, 最后再做一次base64编码,直接赋值给viewstate控件.


参考：
http://www.cnblogs.com/yzxchoice/archive/2006/09/08/498499.html

## 与ASPX相关的
碰到这个
```
25|pageRedirect||/path/to/somepage.aspx| 
```
参考：https://stackoverflow.com/questions/25308551/how-is-a-redirect-response-handled-by-the-client-using-aspx-forms
## TODO
用lxml或者正则加速解析
