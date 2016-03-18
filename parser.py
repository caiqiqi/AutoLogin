#! /usr/local/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
# 用于显示表格的
from prettytable import PrettyTable

TAG_INPUT = 'input'
ID_VIEWSTATE = "__VIEWSTATE"
ID_EVENTVALIDATION = "__EVENTVALIDATION"


def parse_post_params(html_doc):
    '''
    从 html_doc中解析出两个参数
    :param html_doc: 待解析的html页面
    :return: 包含两个已解析的参数的字典
    '''
    '''
    :param html_doc:
    :return:
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

    return dict_values

def parse_courses_selected(html_doc):

    soup = BeautifulSoup(html_doc, "lxml")
    # 选了几门课
    num_courses_selected = _parse_num_courses_selected(soup)
    # 选了哪些课
    courses_selected = _parse_courses_selected(soup)
    print u'选了几门课呢?'
    print num_courses_selected
    print u'选了哪些课呢?'
    # print courses_selected
    # return num_courses_selected


def _parse_num_courses_selected(obj_soup):
    # 通过标签来找
    id_num_courses = "ctl00_contentParent_lblNum"
    # <span id="ctl00_contentParent_lblNum" style="font-weight:bold;">所选课程 共：7 门</span>
    return obj_soup.find(id= id_num_courses).text


def _parse_courses_selected(obj_soup):
    id_couses_list = "ctl00_contentParent_dgData"
    table_courses_list = obj_soup.find(id= id_couses_list)
    # 得到table中的所有 <tr>标签
    list_tr = table_courses_list.find_all('tr')

    list_tr0_th = list_tr[0].find_all('th')
    for i in list_tr0_th:
        print i.text

    # print list_tr0_th[0].text