#!/usr/bin/env python3
# coding: utf-8
# File: spider.py.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-9-13


from urllib import request
from lxml import etree
import pymongo

conn = pymongo.MongoClient()

def get_html(url):
    try:
        return request.urlopen(url).read().decode('GBK', 'ignore')
    except:
        return ''

def main():
    count = 0
    links = ['http://www.juben68.com/index_%s.html'%i for i in range(1, 16)]
    for link in links:
        html = get_html(link)
        selector = etree.HTML(html)
        urls = ['http://www.juben68.com'+ i for i in selector.xpath('//div[@class="block"]/h2/a/@href')]
        for url in urls:
            count += 1
            print(count, url)
            if count < 1262:
                continue
            data = {}
            data['url'] = url
            body = []
            news = get_html(url)
            selector = etree.HTML(news)
            try:
                ps = [selector.xpath('//div[@class="post_content"]/p')][0]
                for p in ps:
                    content = p.xpath('string(.)').replace('\r\n','').replace('\t', '').replace('\xa0', '').replace(' ','').replace('：',':')
                    if not content:
                        continue
                    if '后面更精彩' in content:
                        break
                    body.append(content)
                data['content'] = '\n'.join(body)
                conn['humor']['news'].insert(data)
            except Exception as e:
                print(e)
                pass

if __name__=='__main__':
    main()