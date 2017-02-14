#!/bin/env python26
#coding=UTF-8

from urlparse import urljoin
import lxml.html
from lxml import etree

TITLE_PARAGRAPH_TAGS = set(["h1", "h2", "h3", "h4", "p", "div"])

def extract_text(node, xpath, pattern):
    if node == None:
        return None

    # 通过xpath查找对应的节点
    #print xpath
    nodes = node.xpath(xpath)
    if len(nodes) == 0:
        return None
    #print etree.tostring(nodes[0])
    text = nodes[0].text_content()
    #print text.encode("utf-8")
    
    # 通过正则表达式匹配，取第一个group
    if pattern != None:
        m = pattern.search(text)
        if m != None:
            text = m.group(1)
        else:
            return None

    return text.strip()

def extract_list(node, xpath, pattern):
    if node == None:
        return None

    # 通过xpath查找对应的节点
    nodes = node.xpath(xpath)
    if len(nodes) == 0:
        return None

    texts = []
    for node in nodes:
        text = node.text_content()
    
        if pattern != None:
            m = pattern.search(text)
            if m != None:
                text = m.group(1)

        text = text.replace("\t", "  ")
        texts.append(text.strip())

    return texts

def extract_int(node, xpath, pattern):
    text = extract_text(node, xpath, pattern)
    try:
        return int(text)
    except(ValueError):
        return None

def extract_float(node, xpath, pattern):
    text = extract_text(node, xpath, pattern)
    try:
        return float(text)
    except(ValueError):
        return None

def extract_attr(node, xpath, attr_name):
    '''
        抽取节点对应的属性。
    '''
    nodes = node.xpath(xpath)
    if len(nodes) <= 0:
        return None
    if attr_name not in nodes[0].attrib:
        return None
    return nodes[0].attrib[attr_name]

def is_new_link(link):
    if len(link) == 0:
        return False
    if link.startswith("#"):
        return False
    if link.startswith("javascript:void"):
        return False
    return True

def extract_link(node, xpath, pattern, url):
    '''
        抽取节点对应的链接，必须是a节点，必须包含href属性。
    '''
    link = extract_attr(node, xpath, "href")
    if link == None:
        return None
    if not is_new_link(link):
        return None

    link = urljoin(url, link)
    if link == url:
        return None
    return link


def extract_image_from_node(node, url):
    '''
        抽取节点对应的图片，必须是img节点，必须包含src属性。
        抽取后的图片，会调用upload_img模块来保存图片，最后
        返回保存后的地址。
    '''
    img_url = None
    if "src" in node.attrib:
        img_url = urljoin(url, node.attrib["src"])
    if "data-src" in node.attrib:
        img_url = urljoin(url, node.attrib["data-src"])
    if "data-bigimg" in node.attrib:
        img_url = urljoin(url, node.attrib["data-bigimg"])
    if "data-original" in node.attrib:
        img_url = urljoin(url, node.attrib["data-original"])
    if img_url == None:
        return None
    # 上传图片
    #print img_url
    new_img_url = upload(img_url.encode("utf-8"), url)
    #new_img_url = ""
    return new_img_url



def extract_image(node, xpath, pattern, url):
    '''
        抽取节点对应的图片，必须是img节点，必须包含src属性。
        抽取后的图片，会调用upload_img模块来保存图片，最后
        返回保存后的地址。
    '''
    nodes = node.xpath(xpath)
    if len(nodes) <= 0:
        return "" 

    return extract_image_from_node(nodes[0], url)



def extract_image_list(node, xpath, pattern, url):
    '''
        抽取节点对应的图片，必须是img节点，必须包含src属性。
        抽取后的图片，会调用upload_img模块来保存图片，最后
        返回保存后的地址。
    '''
    results = []
    nodes = node.xpath(xpath)
    if len(nodes) <= 0:
        return results

    for n in nodes:
        results.append(extract_image_from_node(n, url))

    return results


def extract_rich_text_from_node(element, url):
    strs = []
    for action, node in etree.iterwalk(element, events=("start", "end")):
        if not isinstance(node.tag, basestring):
            continue
        if action == "start":
            if node.tag == "br":    # new line
                strs.append("\n")
            elif node.tag == "img":  # image
                # 抽取图片
                new_img_url = extract_image_from_node(node, url)
                if new_img_url != None:
                    strs.append("\n")
                    strs.append('<img src="%s"/>' %new_img_url)
                    strs.append("\n")
            if node.tag != "script" and node.tag != "style" and node.text != None:
                strs.append(node.text)

        if action == "end":
            if node.tag in TITLE_PARAGRAPH_TAGS:    # a new paragraph
                strs.append("\n")
            if node.tag == "td":
                strs.append(" ")
            if node.tag == "tr":
                strs.append("\n")
       
            if node.tail != None and len(node.tail.strip()) > 0:
                strs.append(node.tail)

    return strs 


def extract_rich_text(root, xpath, pattern, url):
    # content
    nodes = root.xpath(xpath)
    #print etree.tostring(nodes[0])
    if nodes == None or len(nodes) == 0:
        return ""
    content_element = nodes[0]
    
    strs = extract_rich_text_from_node(content_element, url)
    content = "".join(strs).strip()
    
    if pattern != None:
        m = pattern.search(content)
        if m != None:
            content = m.group(1)

    return content

def extract_rich_text_list(root, xpath, pattern, url):
    # content
    nodes = root.xpath(xpath)
    if nodes == None or len(nodes) == 0:
        return ""

    strs = []
    for node in nodes:
        strs.extend(extract_rich_text_from_node(node, url))

    content = "".join(strs).strip()
    if pattern != None:
        m = pattern.search(content)
        if m != None:
            content = m.group(1)

    return content

def extract(url, node, xpath, pattern, type):
    '''
        抽取内容
    '''
    if type == "int":
        return extract_int(node, xpath, pattern)
    
    if type == "float":
        return extract_float(node, xpath, pattern)

    if type == "text":
        return extract_text(node, xpath, pattern)

    if type == "list":
        return extract_list(node, xpath, pattern)

    if type == "link":
        return extract_link(node, xpath, pattern, url)

    if type == "image":
        return extract_image(node, xpath, pattern, url)
    
    if type == "rich_text":
        return extract_rich_text(node, xpath, pattern, url)

    if type == "rich_text_list":
        return extract_rich_text_list(node, xpath, pattern, url)
    
    if type == "image_list":
        return extract_image_list(node, xpath, pattern, url)
    return None


if __name__ == "__main__":
    import sys
    import re
    if len(sys.argv) < 2:
        print "Usage: %s test_html_file" %sys.argv[0]
        sys.exit()

    page = open(sys.argv[1], "r").read()
    page = page.decode("gbk", "ignore")
    root = lxml.html.fromstring(page)

    print extract("", root, "/html/body/div/div[2]/div[2]/strong", None, "text").encode("utf-8")
    print extract("", root, "/html/body/div/div[2]/div[2]/span", None, "text").encode("utf-8")
    print extract("", root, '//*[@class="crumbs"]//a[3]', None, "link").encode("utf-8")
    print extract("", root, '/html/body/div/div[2]/div[2]/span/a[1]', re.compile("(\d+).*"), "int")
    print extract("", root, '/html/body/div/div[2]/div[2]/span/a[2]', re.compile("(\d+).*"), "float")
    print extract("", root, "/html/body/div/div[2]/div[2]/span", None, "rich_text").encode("utf-8")
