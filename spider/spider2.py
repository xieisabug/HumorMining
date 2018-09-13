#!/usr/bin/env python3
# coding: utf-8
# File: spider2.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-9-13

#!/usr/bin/env python3
# coding: utf-8
# File: spider.py.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-9-13

from urllib import request
from lxml import etree
import pymongo

conn = pymongo.MongoClient()

'''获取新闻正文'''
def get_html(url):
    try:
        return request.urlopen(url).read().decode('utf-8', 'ignore')
    except:
        return ''

'''采集主函数'''
def main():
    count = 0
    links = ['http://www.xsxpw.com/juben/xiaopinjuben/index_%s.html'%i for i in range(2, 153)]
    links.append('http://www.xsxpw.com/juben/xiaopinjuben/')
    for link in links:
        html = get_html(link)
        selector = etree.HTML(html)
        urls = ['http://www.xsxpw.com'+ i for i in selector.xpath('//li[@class="list_title 3"]/a/@href')]
        for url in urls:
            count += 1
            print(count, url)
            data = {}
            data['url'] = url
            news = get_html(url)
            try:
                title = selector.xpath('//title/text()')[0]
                content = news.split('<div class="newsbody">')[1].split('<div class="page-nav">')[0].split('</')[0].replace('br', 'BR').replace('\u3000', '').replace('\x00','').replace('\r', '').replace('\n', '')
                body = content.split('<BR>')
                data['content'] = '\n'.join(body)
                data['title'] = title
                conn['humor']['news2'].insert(data)

            except Exception as e:
                print(e)




if __name__=='__main__':
    main()