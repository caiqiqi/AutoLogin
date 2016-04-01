#! /usr/local/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import re
# 用于显示表格的
# from prettytable import PrettyTable

TAG_INPUT = 'input'
ID_VIEWSTATE = "__VIEWSTATE"
ID_EVENTVALIDATION = "__EVENTVALIDATION"

# 用于找到sessionId的
_pattern_1 = "Set-Cookie"
_pattern_2 = ";"


def parse_to_post_params(html_doc):
    '''
    从 html_doc中解析出两个参数
    :param html_doc: 待解析的html页面
    :return: 包含两个已解析的参数的字典
    '''
    # soup 就是BeautifulSoup处理格式化后的字符串
    soup = BeautifulSoup(html_doc, "lxml")
    # 找到所有`input`标签,find_all 函数返回的是一个序列
    soup.find_all(TAG_INPUT)
    # 得到VIEWSTATE的值
    value_VIEWSTATE = soup.find(id= ID_VIEWSTATE)['value']
    # 得到EVENTVALIDATION的值
    value_EVENTVALIDATION= soup.find(id = ID_EVENTVALIDATION)['value']
    dict_values = {}
    dict_values['__VIEWSTATE'] = value_VIEWSTATE
    dict_values['__EVENTVALIDATION'] = value_EVENTVALIDATION
    print dict_values['__VIEWSTATE']
    print dict_values['__EVENTVALIDATION']

    return dict_values

def parse_to_courses_selected(html_doc):
    '''
    选课结果查询
    '''
    soup = BeautifulSoup(html_doc, "lxml")
    # 选了几门课
    num_courses_selected = _parse_to_num_courses_selected(soup)
    # 选了哪些课
    courses_selected = _parse_to_courses_selected(soup)
    print u'选了几门课呢?'
    print num_courses_selected
    print u'选了哪些课呢?'
    print courses_selected
    # return num_courses_selected


def _parse_to_num_courses_selected(obj_soup):
    # 通过标签来找
    id_num_courses = "ctl00_contentParent_lblNum"
    # <span id="ctl00_contentParent_lblNum" style="font-weight:bold;">所选课程 共：7 门</span>
    return obj_soup.find(id= id_num_courses).text


def _parse_to_courses_selected(obj_soup):
    id_couses_list = "ctl00_contentParent_dgData"
    table_courses_list = obj_soup.find(id= id_couses_list)
    return table_courses_list.prettify()


def parse_to_sessionId(resp_headers):
    ''' 找到headers这个dict中键为 _pattern_1的值,将其按照_pattern_2 分割成两份, 然后取其第一部分[0] '''
    _sessionID = resp_headers[_pattern_1].split(_pattern_2)[0]
    print "SessinId:"
    print _sessionID
    return _sessionID

def check_if_captcha_wrong(html_doc):
    pattern_captcha_wrong = "$.dialog.alert"
    if re.search(pattern_captcha_wrong, html_doc):
        print pattern_captcha_wrong
        return True
    else:
        print "未提示验证码有错!"
        return False
