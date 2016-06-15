#encoding=utf-8
import cookielib
import urllib2


def save_cookies_to_file():

	'''
	保存cookies到文件
	'''
	url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
	# 设置保存cookie的文件为同级目录下的cookie.txt
	filename = 'cookie.txt'
	# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	# 通过handler来构建opener
	opener = urllib2.build_opener(handler)
	# 创建一个请求，原理同urllib2的urlopen
	response = opener.open(url_loging)
	# 保存cookie到文件
	cookie.save(ignore_discard=True, ignore_expires=True)
	# ignore_discard的意思是，即使cookies将被丢弃也将它保存下来，
	# ignore_expires的意思是，如果在该文件中cookies已经存在，则覆盖原文件写入。
	# 这里我们将这两个全部设置为True。运行之后，cookies将保存到cookie.txt文件中。


def read_cookies_from_file():

	'''
	从文件中获取cookies并带着它访问
	'''
	filename = 'cookie.txt'
	url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"
	# 创建MozillaCookieJar实例对象
	cookie = cookielib.MozillaCookieJar()
	# 从文件中读取cookie到变量
	cookie.load(filename, ignore_discard=True, ignore_expires=True)
	# 创建请求的request
	req = urllib2.Request(url_loging)
	# 利用urllib2的build_opener方法创建一个opener
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open(req)
	print response.read()


if __name__ == "__main__":
	#save_cookies_to_file()
	read_cookies_from_file()
