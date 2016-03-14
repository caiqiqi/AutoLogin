# -*- coding: utf-8 -*-


import urllib2
import cookielib
import urllib
import Image
import cStringIO 
from pytesser import *
import re
import os
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser

import pytesseract
from PIL import Image

#避免 UnicodeEncodeError: 'ascii' codec can't encode character.  的报错
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )



#下面这段是关键了，将为urlib2.urlopen绑定cookies
#MozillaCookieJar(也可以是 LWPCookieJar ，这里模拟火狐，所以用这个了) 提供可读写操作的cookie文件,存储cookie对象
cookiejar = cookielib.MozillaCookieJar()
# 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)
#下面两行为了调试的
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的
opener = urllib2.build_opener(cookieSupport, httpsHandler)
#将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起，安装opener,此后调用urlopen()时都会使用安装过的opener对象，
urllib2.install_opener(opener)





#登陆页面
#loginpage = "http://gs.cqupt.edu.cn:8080/gstudent/default.aspx"



##打开登陆页面, 以此来获取cookies   。  但是因为  ##打开验证码页面就可以获取全部cookies了，所以可以直接跳过这一步。算是可有可无的
#LoginCookies = urllib2.urlopen(loginpage)
##打印cookies
#print  	cookiejar
##先打开页面获取的cookie与  后打开验证码页面的cookie不同。






##提取验证码text(手动输入验证码)
#vrifycodeUrl = "http://zhuzhou2013.feixuelixm.teacher.com.cn/GuoPeiAdmin/Login/ImageLog.aspx"
#file = urllib2.urlopen(vrifycodeUrl)
#pic= file.read()
#path = "c:\\code.jpg"
##img = cStringIO.StringIO(file) # constructs a StringIO holding the image  AttributeError: addinfourl instance has no attribute 'seek'
#localpic = open(path,"wb")
#localpic.write(pic)
#localpic.close()
#print "please  %s,open code.jpg"%path  
##text =raw_input("input code :")
#im = Image.open(path)
#text =image_to_string(im)
#print text


#要post的url
PostUrl   = "http://gs.cqupt.edu.cn:8080/gstudent/ReLogin.aspx" 

url_captcha = "http://gs.cqupt.edu.cn:8080/Public/ValidateCode.aspx"
file_captcha = "captcha.png"

def save_img_from_url(imageUrl, filename):
	'''
	get the captcha by the url_captcha and save the image as 'captcha.png'
	'''
	u = urllib2.urlopen(imageUrl)
	data = u.read()
	#with open(filename, 'w') as fp:
		#shutil.copyfileobj(data, fp)
	f = open(filename, 'wb')
	f.write(data)
	f.close()

def is_file_empty(filepath):
	'''
	判断文件内容是否为空
	'''
	file_size = os.stat(filepath).st_size
	if 0 == file_size:
		return True
	else:
		return False

def parse_img_to_txt(img_file):
	if is_file_empty(img_file)== False:
		result_captcha = pytesseract.image_to_string(Image.open(file_captcha))
		print result_captcha
		return result_captcha
	else:
		print "File size zero!"
		return ''

save_img_from_url(url_captcha, file_captcha)
text = parse_img_to_txt(file_captcha)






#设置cookie的值，因为post request head  需要 返回 cookie (不是cookies ，是将cookies的格式处理后的值)  
cookies = ''
#这里要从
for index, cookie in enumerate(cookiejar):
		#print '[',index, ']';
		#print cookie.name;
		#print cookie.value;
		#print "###########################"
		cookies = cookies+cookie.name+"="+cookie.value+";";
print "###########################"
cookie = cookies[:-1]
print "cookies:",cookie


#用户名，密码
#当然，我这里登顶要处理掉密码和用户名，可不能告诉你真密码账号了
#username = "7879954564555664"
#password = "12313164"

def get_item_from_ini():
	cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    username = cf.get(config_item_info, 'username')
    password = cf.get(config_item_info, 'password')


get_item_from_ini()

#请求数据包

postData = {
	"__EVENTTARGET": "ctl00$contentParent$btLogin"
	"__EVENTARGUMENT":
	"__VIEWSTATE": "/wEPDwUKMTA4ODc5NDc0OA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILD2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUrfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg/aW1hZ2U9MjAwODQ2NTQ5NWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSFjdGwwMCRjb250ZW50UGFyZW50JFZhbGlkYXRlSW1hZ2U="
	"__EVENTVALIDATION": "/wEdAAZ25z2YGnHhHaodt21WSyV/cybtMhw0mn0LtKqAHeD/6LR/VkzxozH4tyiImdrtlAcUWWYub4JHktVQEGONTxqoRZzhTcnfFsWcwOVyhy6aT8GiwGHwM4Wl4obxma9ASls=
	"ctl00$contentParent$UserName": username
	"ctl00$contentParent$PassWord": password
	"ctl00$contentParent$ValidateCode": text
}




#post请求头部
headers = {
   
	'Accept' :	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,en-us;q=0.8,zh;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    
    'Host':    'zhuzhou2013.feixuelixm.teacher.com.cn',
    'Cookie': cookies,
    'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0',  
    'Referer' : 'http://zhuzhou2013.feixuelixm.teacher.com.cn/GuoPeiAdmin/Login/Login.aspx',
	#'Content-Type':	'application/x-www-form-urlencoded',
	#'Content-Length' :474,
    'Connection' : 'Keep-Alive'
	
}


#合成post数据 
data = urllib.urlencode(postData)    
print "data:###############"
print  data
#创建request
#构造request请求
request = urllib2.Request(  PostUrl,data,headers  )
try:
	#访问页面
	response = urllib2.urlopen(request)
	#cur_url =  response.geturl()
	#print "cur_url:",cur_url
	status = response.getcode()
	print status
except  urllib2.HTTPError, e:
	 print e.code

#将响应的网页打印到文件中，方便自己排查错误
#必须对网页进行解码处理
f= response.read().decode("utf8")
outfile =open("rel_ip.txt","w")
print >> outfile , "%s"   % ( f)


#打印响应的信息
info = response.info()
print info




#测试登陆是否成功，因为在testurl只有登陆后才能访问
#还有一个原因是因为post返回得到的网页中含有iframe ，而要搜索的信息刚好在iframe ，所以要去iframe的原来的地址验证
'''
testurl = "http://zhuzhou2013.feixuelixm.teacher.com.cn/GuoPeiAdmin/Login/LoginedPage.aspx"

try:
	response = urllib2.urlopen(testurl)
except  urllib2.HTTPError, e:
	 print e.code

#因为后面要从网页查找字符来验证登陆成功与否，所以要保证查找的字符与网页编码相同，否则无非得到正确的结论。建议用英文查找,如css中的 id， name 之类的。
f= response.read().decode("utf8").encode("utf8")
outfile =open("out_ip.txt","w")
print >> outfile , "%s"   % ( f)

#在返回的网页中，查找“你好” 两个字符，因为只有登陆成功后才有两个字，找到了即表示登陆成功。建议用英文
tag = '你好'.encode("utf8")
if  re.search( tag,f):
	#登陆成功
	print 'Logged in successfully!'
else:
    #登陆失败
	print 'Logged in failed, check result.html file for details'

response.close()

#这个代码很随意，但是容易看，需要的活，可以写成函数。还有就是urlopen()在大量登陆及检验过程中，可能read(0因为网络阻塞而timeout(超时) ，需要设置urlopen() 的超时时间，或者多次发送请求
'''