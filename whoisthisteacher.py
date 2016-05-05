#coding=utf-8
# this tool is used for quering teachers in CQUPT, whose data is from
# its official website  http://www.cqupt.edu.cn

import requests
import lxml.html

main_url            = "http://www.cqupt.edu.cn/cqupt/index.shtml"

#通信与信息工程学院
tongxin_url_0       = "http://scie.cqupt.edu.cn:8080/"
#计算机科学与技术学院
jisuanji_url_0      = "http://cs.cqupt.edu.cn/ReadNews.asp?NewsID=7867"
jisuanji_url_1      = "http://cs.cqupt.edu.cn/ReadNews.asp?NewsID=7866"
#自动化学院
zidonghua_url_0     = "http://ac.cqupt.edu.cn/teacher_rank.php?cat_id=39"
#先进制造工程学院
xianjinzhizao_url_0 = "http://same.cqupt.edu.cn/newsList.html?id=10&%E5%AD%A6%E9%99%A2%E6%A6%82%E5%86%B5"
#光电工程学院
guangdian_url_0     = "http://ee.cqupt.edu.cn/listsmall.php?bid=2&sid=6"
#软件工程学院
ruanjian_url_0      = "http://202.202.43.26/software/test.aspx?pro=27&doc=1"
#理学院
lixueyuan_url_0     = "http://slxy.cqupt.edu.cn/teacherList.php"
#经济管理学院
jingguan_url_1      = "http://jgxy.cqupt.edu.cn/list.php?sid=46&bid=12&page=1"
jingguan_url_2      = "http://jgxy.cqupt.edu.cn/list.php?sid=46&bid=12&page=2"
jingguan_url_3      = "http://jgxy.cqupt.edu.cn/list.php?sid=46&bid=12&page=3"
jingguan_url_4      = "http://jgxy.cqupt.edu.cn/list.php?sid=46&bid=12&page=4"
#传媒艺术学院
chuanmei_url_0      = "http://cmys.cqupt.edu.cn/teachers/yingshibiandaoyuchuanboxi/"
chuanmei_url_1      = "http://cmys.cqupt.edu.cn/teachers/shuzimeitiyudonghuaxi/"
chuanmei_url_2      = "http://cmys.cqupt.edu.cn/teachers/yishushejixi/"
chuanmei_url_3      = "http://cmys.cqupt.edu.cn/teachers/shiyanzhongxin/"
chuanmei_url_4      = "http://cmys.cqupt.edu.cn/teachers/TVcreationcenter/"
#外国语学院
waiguoyu_url_0      = "http://cfl.cqupt.edu.cn/szdw.htm"
#法学院
faxueyuan_url_0     = "http://law.cqupt.edu.cn/index.php/t_team/tlist"
#马克思主义学院
makesi_url_0        = "http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E8%AE%B2%E5%B8%88"
makesi_url_1        = "http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E5%89%AF%E6%95%99%E6%8E%88"
makesi_url_2        = "http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E6%95%99%E6%8E%88"


ruanjian_xpath = '//body/form[@id="aspnetForm"]/div[@id="main"]/div[@class="content"]/div[@class="list_right mt20"]/div[@class="news_list mt15"]/div/div/div[@id="ctl00_ContentPlaceHolder1_UpdatePanel1"]/ul/li/span[@class="text"]/a'
waiguoyu_xpath = '//body[@class="channle"]/table/tbody/tr/td[@class="news_list"]/table[@class="box"]/tbody/tr/td/li/a'



def get_teacher_name(college_url, xpath_expression):
    resp = requests.get(college_url)
    doc = lxml.html.document_fromstring(resp.content)
    html_uls = doc.xpath(xpath_expression)
    for html_ul in html_uls:
        print html_ul.text

#软件学院 //TODO: 对js进行跳转到下一页的情况进行处理
get_teacher_name(ruanjian_url_0, ruanjian_xpath)
#外国语学院
#get_teacher_name(waiguoyu_url_0, waiguoyu_xpath)

