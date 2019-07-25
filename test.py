#!/usr/bin/env python

"""
author: ares
date: 2019/5/12
desc:
"""

import requests
from selenium import webdriver
import re
import json
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome('/Users/dukang02/Documents/python/chromedriver', options=chrome_options)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed'
              '-exchange;v=b3'
}


def get_douban_url(num):
    raw_url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start=%s'
    return [raw_url % (i*20) for i in range(num)]





# url_list = get_douban_url(1)
# for url in url_list:
#     req_session = requests.Session()
#     # res_dict = json.loads(req.text)
#     # movies = res_dict['data']
#     # for i in movies:
#     #     print(i['title'], i['rate'], i['url'], i['cover'])
#     # time.sleep(1)

pattern = re.compile("\{.*\}")
res = requests.get('http://yuehui.163.com/searchphoto.do?ajax=1&load=0&page=2&pagesize=36&sex=0&province=0&city=0&ageBegin=18&ageEnd=25&order=15', headers=headers).text
persons = json.loads(re.search(pattern, res).group())['list']
for i in persons:
    print(i)




