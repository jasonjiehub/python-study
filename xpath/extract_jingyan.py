#!/bin/env python
#coding=UTF-8

import re
import sys
sys.path.append("./")
import ordered_dict

import zlib
from lxml import etree
import lxml.html

sys.path.append("../../webdata/parser")

import pdb

#抽取正文内容，包括图片。其中图片会转义，只保留 sign部分，即这种：4a36acaf2edda3ccdbb8433c02e93901213f924a.jpg
#现在是基本上去掉无意义的TAG。留下有意义的TAG
def extract_content(root, images):
    text_avail_tags =set(['h2', 'p', 'h3', 'h1', 'strong', 'br']) 
    all_avail_tags = set(text_avail_tags)
    all_avail_tags.add('img')

    un_tags = set()
    
    all_queue = []
    all_queue.append(root) 
    while len(all_queue) > 0:
        node = all_queue.pop()
        tag_name = node.tag

        if tag_name not in all_avail_tags:
            un_tags.add(tag_name)
        elif tag_name == 'img':  #改变img
            img_url = node.attrib.get('data-src')
            if img_url == None:
                img_url = node.attrib.get('src')
            if img_url != None:
                sp=img_url.split('/')
                newurl = 'pics/%s' % sp[-1]
                images.add(img_url)
                node.attrib.clear()
                node.set('src', newurl)

        if node.text == u'步骤阅读':
            node.clear()

        childs = node.getchildren()
        all_queue.extend(childs)

    for tagname in un_tags:
        path = ".//%s" % tagname
        while True:
            subnode = root.find(path)
            if subnode != None:
                subnode.drop_tag()
            else:
                break

    root.attrib.clear()
    txt_body = lxml.html.tostring(root, encoding='utf8')

    return txt_body
        
def extract_jingyan(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    #result = ordered_dict()
    result = {}
    import extract
    # 问题 问题分类 浏览量 更新时间 问题描述
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度经验"))
    result["update_time"] = extract.extract_text(root, '//ul[@class="exp-info"]//time', None) 
    result["view_num"] = extract.extract_text(root, '//ul[@class="exp-info"]//span[@class="views"]', None) 
    result["tag"] = extract.extract_text(root, '//ul[@class="exp-info"]//span[@class="exp-tag-top"]', None) 
    result["nav"] = extract.extract_text(root, '//div[@id="bread-wrap"]', None)

    # 正文 
    '''
  exp-content-block
     exp-content-listblock
        content-listblock-text

  exp-content-block
      exp-content-head  <h2>
      exp-content-body
           exp-content-unorderlist 
             exp-content-list list-item-1
                class="content-list-text"
                class="content-list-media"
                     <img src
                     <img data-src
           or 
             exp-conent-orderlist
                  exp-content-list list-item-1           

    '''
    article_nodes = root.xpath('//*[@alog-group="exp-content"]/div[@class="exp-content-block"]')
    i = 0 
    articles = [] 
    images = set() 
    for node in article_nodes:
        subblocks = []
        head_node = node.xpath('.//div[@class="exp-content-head"]')
        content_header = ""
        if len(head_node) > 0:
            content_header = node.text_content()

        #print "paragraph", etree.tostring(node)
        list_text_nodes = node.xpath('.//div[@class="content-listblock-text"]')
        list_text_nodes = node.xpath('.//div[@class="exp-content-listblock"]')
        for tnode in list_text_nodes:
            txt_body = extract_content(tnode, images)
            subblocks.append((1, txt_body, []))  #内容， 图片

        #h2标题
        h2_text_nodes = node.xpath('.//h2[@class="exp-content-head"]')
        for tnode in h2_text_nodes:
            txt_body = extract_content(tnode, images)
            subblocks.append((1, txt_body, []))  #内容， 图片

        #pdb.set_trace()
        #order_text_nodes = node.xpath('.//ol[@class="exp-content-orderlist"]')
        order_text_nodes = node.xpath('.//div/ol[starts-with(@class,"exp-conent-orderlist")]')
        if len(order_text_nodes) > 0:
            type = 2
        else:
            #order_text_nodes = node.xpath('.//ul[@class="exp-content-unorderlist"]')
            order_text_nodes = node.xpath('.//div/ul[starts-with(@class,"exp-content-unorderlist")]')
            if len(order_text_nodes) > 0:
                type = 4 

        for subnode in order_text_nodes:
            '''
             exp-content-list list-item-1
                class="content-list-text"
                class="content-list-media"
                     <img src
                     <img data-src
            '''
            #ssnodes = subnode.xpath('./div[@class="exp-content-list"]')
            ssnodes = subnode.xpath('.//li[starts-with(@class, "exp-content-list")]')
            for ssnode in ssnodes:
                txt_body = extract_content(ssnode, images)
                subblocks.append((1, txt_body, []))  #内容， 图片

        if len(subblocks) > 0:
            articles.append([content_header, subblocks])  #头，子列表

    result['articles'] = articles

    # 投票数 有得 疑问 TODO：用户评论数 
    comments = root.xpath('//*[@class="wgt-comments"]')
    if comments:
        result["vote_num"] = extract.extract_text(comments[0], './/div[@class="vote-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
        result["hads_num"] = extract.extract_text(comments[0], './/div[@class="hads-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
        result["ques_num"] = extract.extract_text(comments[0], './/div[@class="ques-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
    else:
        result["vote_num"] = extract.extract_text(root, '//*[@class="useful-button-wp"]//span[@class="a-h"]', re.compile(u"(\d+)"))
        result["collect_num"] = extract.extract_text(root, '//*[@class="collect-button-wp"]//span[@class="a-h"]', re.compile(u"(\d+)"))

    # 用户名 主页
    user = root.xpath('//*[@class="author-info left"]/h2/a')
    if user:
        #print "user", etree.tostring(user[0])
        result["user_name"] = user[0].text_content()
        #result["user_homepage"] = "http://jingyan.baidu.com/" + user[0].attrib.get("href")
        result["user_homepage"] = user[0].attrib.get("href")
    
    result['images'] = images
    return result 

def parse_from_string(data, code):
    try:
        root = lxml.html.fromstring(data.decode(code, "ignore"))
    except Exception, e:
        #print e
        return None
    return root

def to_html(filename, result):
    title = rst['title'].encode('utf8', 'ignore') 
    aaa=filename.split('/')
    jingyan_url='http://jingyan.baidu.com/article/%s' % (aaa[-1])

    sinfo = "<h2>%s</h2>\n" % (title)
    sinfo += '<p><a target="_blank" href="%s">经验URL</a></p>\n' % (jingyan_url)
    sinfo += "<p>更新时间: %s </p>\n" % (rst['update_time'])
    sinfo += "<p>浏览数: %s</p>\n" % (rst['view_num']) 

    ss = ""
    if rst['tag'] != None:
        ss = rst['tag'].encode('utf8', 'ignore')
    sinfo += "<p>tag: %s</p>\n" % (ss)
    
    ss = ""
    if rst['nav'] != None:
        ss = rst['nav'].encode('utf8', 'ignore')
    sinfo += "<p>nav: %s</p>\n" % (ss)

    astr = ""
    for article in rst['articles']:
        content_header = article[0]
        subblocks = article[1]

        astr += content_header
        
        id = 0 
        for sub in subblocks:
            type = sub[0]
            body_txt = sub[1]
            id += 1
            if type == 4:
                astr += '<h2>%s<h2>%s\n' % (id, body_txt)
            else:
                astr += body_txt

    html = '<meta charset="utf-8">\n'
    html += '<html><body>%s<p><p>%s</body</html>' % (sinfo, astr)

    return html 


#pdb.set_trace()
filename=sys.argv[1]
outfname = sys.argv[2]
with open(filename) as fp:
    data = fp.read()
    root = parse_from_string(data, "UTF8")
    if root != None:
        rst = extract_jingyan("", root, data)

        if 'title' in rst:
            images = rst['images']
            imgstr = ';'.join(images)
            fs = filename.split('/')
            ss = "%s\t%s\t%s\t%s\t%s"%(fs[-1], rst['title'], rst['nav'], rst['tag'], imgstr)
            ss = ss.encode('utf8', 'ignore')
            print  ss

        html_str = to_html(filename, rst)
        if len(sys.argv) > 3:
            print html_str

        outfile = open(outfname, 'w')
        outfile.write(html_str)
        outfile.close()

        sys.exit() 

        print "update_time\t", rst['update_time']
        print 'view_num\t', rst['view_num']
        print 'tag\t', rst['tag']
        print 'nav\t', rst['nav']

        print 'articles\t', rst['articles']
        print 'images\t', rst['images']
