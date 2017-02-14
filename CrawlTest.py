import urllib.request

res = urllib.request.urlopen("http://www.baidu.com")
print(res.getcode())
print(res.read())
