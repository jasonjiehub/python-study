#!/usr/bin/python

from time import sleep
import urllib2
import random
import os

total = -1
downerr = open("/search/ffy/downerr","a+")
path = ""

def writeErr(url):
    global downerr
    try:
        downerr.write(url+"\n")
    except:
        print "down error "+url

def writeFile(name,data):
    try:
        f = open(name,"w+")
        f.write(data)
        f.close()
    except:
        writeErr("write file error "+name)

Headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'_za=5b9b59ad-6b9b-47e6-a4ca-a378b0a3fd8e; _ga=GA1.2.2126042714.1437378236; q_c1=441c1350dac9470aaa22b91c2a41c1b0|1440036410000|1437378235000; _xsrf=75169d80827fbabaf39d4053622a5b9e; tc=AQAAALaqqTVTWgkA3TN+exFwj1mnFOHb; cap_id="ODNmNDFmZjkzZWU0NGI5YjlhY2Y5NjdkYjVmZjY0ZmY=|1441158705|b97cfdf33304b7d289b871aee80f49e6d18e6d94"; z_c0="QUJCTTZONERvd2dYQUFBQVlRSlZUVG5qRFZZbTBmdjc1MDJhWXR2aEhCSG1FenJJdG1KLUl3PT0=|1441158713|307a22607e7cd9e752f9ed1cca64a83cb2fd141c"; __utmt=1; __utma=51854390.1930374697.1441677292.1441677292.1441677292.1; __utmb=51854390.11.9.1441677328083; __utmc=51854390; __utmz=51854390.1441676533.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-2|2=registration_date=20150902=1^3=entry_date=20150720=1',
        'Host':'www.zhihu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        }
for page in range(1,126579):
	global path
        if(page % 10 == 0):
            time = random.uniform(2,10)
            sleep(time)
        url='http://www.zhihu.com/topic/19776749/questions?page='+str(page)

        Referers='http://www.zhihu.com/topic/19776749/questions?page='+str(int(page-1))
        Headers['Referer']=Referers
        try:
            req=urllib2.Request(url,headers=Headers)
            response=urllib2.urlopen(req,timeout=20)
            data_page=response.read()
        except:
            writeErr(url)
            continue
        ismk = 0
        total += 1
        if(total%10000 == 0):
            try:
                tmp_path = "/search/ffy/zhihu-topic-all/"+str(total/10000)
                os.mkdir(tmp_path)
            except:
                print "mkdir error "+str(total/10000)
            else:
                ismk = 1
        if(ismk == 1):
                path = tmp_path
       
        file_name=path+"/"+str(page)+".gz"
        writeFile(file_name,data_page)           

downerr.close()
