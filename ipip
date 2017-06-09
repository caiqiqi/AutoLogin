#! /usr/bin/env python
#coding=utf-8
__author__ = 'caiqiqi'


import sys

from pyquery import PyQuery as pq

from bs4 import BeautifulSoup
import requests
import lxml.html

url = 'http://www.ipip.net/ip.html'

header = {
'Host':"www.ipip.net",
'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0",
'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
'Accept-Encoding':"gzip, deflate",
'Referer':"http://www.ipip.net/",
'Connection':"keep-alive",
'Upgrade-Insecure-Requests':"1",
'Content-Type':"application/x-www-form-urlencoded"
}

def parse_html_by_bs(html_str):
    soup = BeautifulSoup(html_str, "lxml")
    return soup.find(id='myself').get_text()

def parse_html_by_pq(html_str):
    doc = pq(html_str)
    return doc('#myself').text()

s = requests.Session()
payload = ''

try:
    payload = 'ip=' + sys.argv[1]
except IndexError as e:
    print "[!] 未输入查询IP, 直接返回当前IP"

r = s.post(url, data=payload, headers=header)
#print parse_html_by_bs(r.content)
print parse_html_by_pq(r.content)
s.close()
