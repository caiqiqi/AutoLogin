import urllib2

url_loging = "http://gs.cqupt.edu.cn:8080/gstudent/loging.aspx?undefined"

req = urllib2.Request(url_loging)
try:
	response = urllib2.urlopen(req)
	print response.read()
except urllib2.HTTPError, e:
	print e.code
	print e.reason
	print e