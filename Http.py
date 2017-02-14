
# from urllib import request
# page = request.urlopen('http://www.cnblogs.com/congbo/archive/2012/08/23/2652490.html')
# text = page.readlines()
# print(text)
from lxml import html
import requests
# page = "<div title=\"buyer-name\">Carson Busses</div>"
page = requests.get("http://www.sogou.com/kmap?query=%E9%99%88%E5%A5%95%E8%BF%85&from=relation&id=")
# tree = html.fromstring(page.text)
# buyers = tree.xpath('//div[@title="buyer-name"]/text()')
# print(buyers)
print(page.text)
