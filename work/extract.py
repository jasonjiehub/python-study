
#!/usr/bin/python
# coding : unicode 

import os,sys
import time,pdb
import re

charset_reg =  re.compile(r'<meta\s+http-equiv=\"Content-Type\".*?charset=(.*?)\"', re.X|re.DOTALL|re.IGNORECASE)
bread1_reg =  re.compile(r'blkChannel_path.*?>(.*?)<\/div>', re.X|re.DOTALL|re.IGNORECASE)
bread2_reg =  re.compile(r'blkBreadcrumbNav.*?>(.*?)<\/div>', re.X|re.DOTALL|re.IGNORECASE)
title_reg = re.compile(r'<title>(.*?)<\/title>', re.X|re.DOTALL|re.IGNORECASE)
kw_reg = re.compile(r'art_keywords\">(.*?)<\/p>', re.X|re.DOTALL|re.IGNORECASE)
content_reg = re.compile(r'id=\"artibody\">(.*?)end\s*-->', re.X|re.DOTALL|re.IGNORECASE)

def extract(filename):
    ff = open(filename)
    htm = ff.read()
    ff.close()

    title = ""
    charset = ""
    content = ""

    bread = ""
    keyword = ""

    try:
        htm = htm.replace("\r"," ").replace("\n"," ").replace("\t", " ")
    
        #charset
        reres = charset_reg.search(htm)    
        if reres:        
            charset = reres.group(1)
        else:
            print(filename)
            return

        #bread
        reres = bread1_reg.search(htm)    
        if reres:        
            bread = reres.group(1)
        else:
            reres = bread2_reg.search(htm)    
            if reres:        
                bread = reres.group(1)
            else:
                print(filename + "\t" + charset)
                return

        #title
        reres = title_reg.search(htm)
        if reres:        
            title = reres.group(1)
        else:
                print("%s\t%s\t%s" % (filename, charset, bread))
                return

        #content
        reres = content_reg.search(htm)
        if reres:        
            content = reres.group(1)

        #keyword
        reres = kw_reg.search(htm)
        if reres:        
            keyword = reres.group(1)

        print("%s\t%s\t%s\t%s\t%s\t%s" % (filename, charset, title, bread, keyword, content))

    except:
        pass 

if __name__=="__main__":
    extract(sys.argv[1])
