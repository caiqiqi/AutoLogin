#coding=utf-8
# this tool is used for quering teachers in CQUPT, whose data is from
# its official website  http://www.cqupt.edu.cn
# lxml说明文档 http://lxml.de/3.1/api/private/lxml.html.HtmlElement-class.html
import sys
import requests
import lxml.html


########## url ##########
main_url            = "http://www.cqupt.edu.cn/cqupt/index.shtml"

#通信与信息工程学院
tongxin_url = [ "http://scie.cqupt.edu.cn:8080/index/index/page/"+str(i) for i in range(1,13) ]   #生成12页

#计算机科学与技术学院
jisuanji_url_0 = "http://cs.cqupt.edu.cn/ReadNews.asp?NewsID=7867"
jisuanji_url_1 = "http://cs.cqupt.edu.cn/ReadNews.asp?NewsID=7866"
#自动化学院
zidonghua_url     = "http://ac.cqupt.edu.cn/teacher_rank.php?cat_id=39"
#先进制造工程学院
xianjinzhizao_url = "http://same.cqupt.edu.cn/newsList.html?id=10&%E5%AD%A6%E9%99%A2%E6%A6%82%E5%86%B5"
#光电工程学院
guangdian_url     = "http://ee.cqupt.edu.cn/listsmall.php?bid=2&sid=6"
#软件工程学院
ruanjian_url      = "http://202.202.43.26/software/test.aspx?pro=27&doc=1"
#理学院
lixueyuan_url     = "http://slxy.cqupt.edu.cn/teacherList.php"
#经济管理学院
jingguan_url = [ "http://jgxy.cqupt.edu.cn/list.php?sid=46&bid=12&page="+str(i) for i in range(1,5)]
#传媒艺术学院
chuanmei_url = 
["http://cmys.cqupt.edu.cn/teachers/yingshibiandaoyuchuanboxi/", 
"http://cmys.cqupt.edu.cn/teachers/shuzimeitiyudonghuaxi/", 
"http://cmys.cqupt.edu.cn/teachers/yishushejixi/", 
"http://cmys.cqupt.edu.cn/teachers/shiyanzhongxin/", 
"http://cmys.cqupt.edu.cn/teachers/TVcreationcenter/"]
#外国语学院
waiguoyu_url      = "http://cfl.cqupt.edu.cn/szdw.htm"
#法学院
faxueyuan_url     = "http://law.cqupt.edu.cn/index.php/t_team/tlist"
#马克思主义学院
makesi_url = 
["http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E8%AE%B2%E5%B8%88", 
"http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E5%89%AF%E6%95%99%E6%8E%88", 
"http://marx.cqupt.edu.cn/home?method=childPhotoShow&category=%E6%95%99%E6%8E%88"]



########## xpath ##########
main_xpath  = '//div[@class="_s1 select"]/ul/li/a'
ruanjian_xpath = '//div[@id="ctl00_ContentPlaceHolder1_UpdatePanel1"]/ul/li/span[@class="text"]/a'
waiguoyu_xpath = '//li/a[@target="_blank"]'
lixueyuan_xpath = '//font[@style="font-size:12px;line-height:30px;"]/a[@target="_blank"]'
jingguan_xpath = '//td[@align="left" and @class="bottom1"]/a'
zidonghua_xpath = '//span[@class="STYLE13"]/a'
jisuanji_xpath_0 = '//td[@valign="top"]/div[@class="articleContent"]/table/tr[2]/td/p[2]/a'
jisuanji_xpath_1 = '/html/body/div/table[4]/tr/td[2]/div[@class="articleContent"]/table/tr[2]/td/div//a'
#Note:用xpath时，在html元素中碰到tbody不用查找tbody，直接忽略，往下一级查找，如不要`table/tbody/tr`
#而直接 `table/tr` 即可
#Note:找到某路径下所有a元素或者子元素中包含的a元素 `XXX//a`
tongxin_xpath = '//div[@class="teacher-name"]/parent::*'



def get_teacher_name(college_url, xpath_expression, tp, is_list=False):
    resp = requests.get(college_url)
    doc = lxml.html.document_fromstring(resp.content)
    print "-----" + tp + "-----"

    html_uls = doc.xpath(xpath_expression)     # list类型
    print "得到的list长度为：", str(len(html_uls))
    if tp=='通信学院':
    	print html_ul.find('div').text
        #获得某html元素的某属性
        print html_ul.attrib['href']
    
    for html_ul in html_uls:
        print html_ul.text
        #获得某html元素的某属性
        print html_ul.attrib['href']



#主页
#get_teacher_name(main_url, main_xpath, 'main')
'''
#软件学院 //TODO: 对js进行跳转到下一页的情况进行处理
get_teacher_name(ruanjian_url_0, ruanjian_xpath, '软件学院')
#外国语学院
get_teacher_name(waiguoyu_url_0, waiguoyu_xpath, '外国语学院')
#理学院
get_teacher_name(lixueyuan_url_0, lixueyuan_xpath , '理学院')
#经管学院
for i in range(0,4):
	get_teacher_name(jingguan_url[i], jingguan_xpath, '经管学院')

#自动化学院 //TODO: ##bug 魏F--> 魏旻
get_teacher_name(zidonghua_url_0, zidonghua_xpath, '自动化学院')
'''
#计算机学院
#get_teacher_name(jisuanji_url_0, jisuanji_xpath_0, '计算机学院')
#get_teacher_name(jisuanji_url_1, jisuanji_xpath_1, '计算机学院')
#通信学院
get_teacher_name(tongxin_url_0, tongxin_xpath, '通信学院')

