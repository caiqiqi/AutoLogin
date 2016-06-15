from lxml import etree
import requests


index_url = "http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php"

resp1 = requests.get(index_url)

# get the html text(str)
html = resp1.content
print html

# get the root node
root = etree.fromstring(html)

# get the line to be calculated
line = root.xpath('//form/text()').extract()

print line
