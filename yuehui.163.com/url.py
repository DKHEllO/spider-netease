#!/usr/bin/env python

"""
author: ares
date: 2019/5/15
desc:
"""

import requests
import re
import json
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed'
              '-exchange;v=b3'
}


def get_persons_info(sex, province, age_begin, age_end, city=-1, page_size=36, page_num=0):
    province_num_dict = {
        '北京': '0',
        '上海': '1',
        '天津': '2',
        '重庆': '3',
        '河北': '4',
        '山西': '5',
        '内蒙古': '6',
        '辽宁': '7',
        '吉林': '8',
        '黑龙江': '9',
        '江苏': '10',
        '浙江': '11',
        '安徽': '12',
        '福建': '13',
        '江西': '14',
        '山东': '15',
        '河南': '16',
        '湖北': '17',
        '湖南': '18',
        '广东': '19',
        '广西': '20',
        '海南': '21',
        '四川': '22',
        '贵州': '23',
        '云南': '24',
        '西藏': '25',
        '陕西': '26',
        '甘肃': '27',
        '青海': '28',
        '宁夏': '29',
        '新疆': '30',
        '香港': '31',
        '澳门': '32',
        '台湾': '33'
    }
    province_num = province_num_dict[province]
    pattern = re.compile("\{.*\}")
    persons_info = []
    while True:
        url = 'http://yuehui.163.com/searchphoto.do?ajax=1&load=0&page={page_num}&pagesize={page_size}&sex={sex}&' \
              'province={province}&city={city}&ageBegin={age_begin}&ageEnd={age_end}&order=15'.\
            format(page_num=page_num, page_size=page_size, sex=sex, province=province_num, city=city,
                   age_begin=age_begin, age_end=age_end)
        res = requests.get(url, headers=headers).text
        persons_list = json.loads(re.search(pattern, res).group()).get('list', None)
        if not persons_list:
            print('%s %s' % (province, page_num))
            break
        page_num += 1
        persons_info += persons_list
        time.sleep(1)
    return persons_info


def get_detail_page(user_id):
    url = 'http://yuehui.163.com/viewuser.do?id={user_id}'.format(user_id=user_id)
    req = requests.get(url, headers=headers)
    return req.text


def get_image(url, image_name):
    f = open(image_name, 'wb')
    res = requests.get(url, headers=headers).content
    f.write(res)




