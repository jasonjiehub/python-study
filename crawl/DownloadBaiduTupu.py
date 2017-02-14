import requests
import simplejson
import codecs
import queue
from random import randrange
import os

# 以章子怡作为入口
url = 'http://tupu.baidu.com/tupu/api/graph/v2?id='

def downloadtupudata(lemmaId):
    proxies = {
        'http': 'www.test01.com:8080'
    }
    global url
    for i in range(5):
        try:
            randData = randrange(32) + 1
            host = 'www.test' + ('%02d' % randData) + '.com'
            if randData <= 16:
                proxies['http'] = host + ":8080"
            else:
                proxies['http'] = host + ":9090"

            page = requests.get(url + str(lemmaId), proxies=proxies, timeout=10)
            return page.text

        except:
            pass

    return None

lemmaIdQueue = queue.Queue(maxsize=0)
lemmaIdQueue.put(131804)
lemmaIdQueue.put(114923)
lemmaIdQueue.put(633129)
lemmaIdQueue.put(80102)
lemmaIdQueue.put(424349)
lemmaIdQueue.put(6804)
lemmaIdQueue.put(77734)
lemmaIdQueue.put(702991)
lemmaIdQueue.put(1826141)
lemmaIdQueue.put(71648)
lemmaIdQueue.put(240200)
lemmaIdQueue.put(57581)
lemmaIdQueue.put(5681)
lemmaIdQueue.put(236869)
lemmaIdQueue.put(5681)
lemmaIdQueue.put(17753)
lemmaIdQueue.put(131821)
lemmaIdQueue.put(828151)

lemmaIdList = [131804, 114923, 633129, 80102, 424349, 6804, 702991, 1826141, 71648, 240200, 57581, 5681,
               236869, 17753, 131821, 828151]
index = 0
notFoundFile = codecs.open('notFoundFile.o', 'w', 'utf-8')
notConnectFile = codecs.open('notConnectFile.o', 'w', 'utf-8')
while not lemmaIdQueue.empty():
    lemmaId = lemmaIdQueue.get()
    print(lemmaId)
    print('start get')
    pageText = downloadtupudata(lemmaId)
    print(pageText)
    print('end get')
    if pageText:
        if not pageText.startswith('{"interests'):
            notConnectFile.write(str(lemmaId) + "\n")

        else:
            pageJson = simplejson.loads(pageText)
            entities = pageJson.get('entities')

            if entities:
                index += 1
                path = './tupuFile/' + str(index // 1000)
                if not os.path.exists(path):
                    os.mkdir(path)

                f = codecs.open(path + "/" + str(lemmaId) + '.json', 'w', 'utf-8')
                f.write(pageText)

                for entry in entities:
                    tempId = entry.get('newlemmaID')
                    if tempId and (not (tempId in lemmaIdList)):
                        lemmaIdList.append(tempId)
                        lemmaIdQueue.put(tempId)
            else:
                notFoundFile.write(str(lemmaId) + "\n")

    else:
        notConnectFile.write(str(lemmaId) + "\n")

print('done')
