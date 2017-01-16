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

## TODO
用lxml或者正则加速解析
