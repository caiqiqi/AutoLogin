#! /usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'caiqiqi'

import os
import random

import requests
# ConfigParser 用于从.ini文件中读取信息的
import ConfigParser

import pytesseract
from PIL import Image

CONFIG_FILE = 'config.ini'
CONFIG_ITEM_INFO = 'info'

def gen_random_int():
    int_random = random.randint(100000000, 999999999)
    print "生成的随机数为:"
    print int_random
    return int_random

def get_items_from_ini():
    '''
    从.ini文件中载入账户密码信息
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)
    dict_user = {}
    dict_user['username'] = cf.get(CONFIG_ITEM_INFO, 'username')
    dict_user['password'] = cf.get(CONFIG_ITEM_INFO, 'password')
    print "账号信息:"
    print dict_user
    return dict_user

def _is_file_empty(filepath):
    '''
    判断文件内容是否为空
    '''
    file_size = os.stat(filepath).st_size
    if 0 == file_size:
        return True
    else:
        return False

def parse_img_to_txt(image_file):
    if not _is_file_empty(image_file):
        result = pytesseract.image_to_string(Image.open(image_file))
        print "解析结果:"
        print result
        return result
    else:
        print "File size zero!"
        return ""


def save_img_from_url(imageUrl, heads, filename):
    '''
    get the captcha by the url_captcha and save the image as 'captcha.png'
    '''
    r = requests.get(imageUrl,headers= heads)
    # with open(filename, 'w') as fp:
    # shutil.copyfileobj(data, fp)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()