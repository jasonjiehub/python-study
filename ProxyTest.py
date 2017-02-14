import requests
import simplejson
import codecs
import queue
from random import randrange

proxies = {
    'http': 'adslspider01.web.zw.vm.ted:8080'
}

url = 'http://tupu.baidu.com/tupu/api/graph/v2?id='
randData = randrange(32) + 1
host = 'adslspider' + ('%02d' % randData) + '.web.zw.vm.ted'
if randData <= 16:
    proxies['http'] = host + ":8080"
else:
    proxies['http'] = host + ":9090"

print(proxies)

page = requests.get(url + '104887', proxies=proxies)
pageText = page.text
pageJson = simplejson.loads(pageText)
if pageJson.get('entities'):
    for entry in pageJson.get('entities'):
        print(entry.get('newlemmaID'))
        print(type(entry.get('newlemmaID')))
else:
    print('not find')
    print(type(pageJson))
    print(pageJson)
