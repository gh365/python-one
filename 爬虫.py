# _*_ coding:utf-8 _*_
"""
file: 爬虫.py
date: 2021-01-15 17:02
author: lw
desc:
"""

import requests  # 下载网页
import bs4  # 解析网页
import re
import random
import time

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'accept-encoding': 'gzip, deflate, br', #乱码https://www.sohu.com/a/431514392_453160
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.douban.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def solve_data(page_list):
    '''
    解析分页数据
    :param page_list:
    :return:
    '''
    url_list = set()
    for url in page_list:
        # 休眠5～10秒，取随机数，避免IP被限制
        time.sleep(random.randint(5, 10))
        page_obj = requests.get(url, headers=headers)
        # print(page_obj.text)
        bs4_obj = bs4.BeautifulSoup(page_obj.text, 'lxml')
        comments_eles = bs4_obj.find_all('div', attrs={'class': 'reply-doc'})
        # print(comments_eles)
        for ele in comments_eles:
            comment_ele = ele.find('p', attrs={'class': 'reply-content'})
            # print(comments_ele)
            # url=re.search('https', comment_ele.text, flags=re.A)
            pattern = re.compile(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
            if comment_ele.text:
                urls = re.findall(pattern, comment_ele.text)
                if urls:
                    for url in urls:
                        print(url)
                        url_list.add(url)
    # print(url_list)
    print(len(url_list))

page_list = ['https://www.douban.com/group/topic/39874547/', 'https://www.douban.com/group/topic/39874547/?start=100',
             'https://www.douban.com/group/topic/39874547/?start=200',
             'https://www.douban.com/group/topic/39874547/?start=300']
solve_data(page_list)