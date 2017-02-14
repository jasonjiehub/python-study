import urllib
import sys

for url in sys.stdin:
    a=urllib.unquote(url)
    print a
