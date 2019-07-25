#!/usr/bin/env python

"""
author: ares
date: 2019/5/16
desc:
"""
import sys
sys.path.append('../')
from url import get_image, get_detail_page, get_persons_info
from database import MysqlConnector

mysql_db = MysqlConnector()
mysql_db.select_db('yuehui')
table = {
        'name': 'VARCHAR(255)',
        'age': 'INT(4)',
        'province': 'VARCHAR(255)',
        'stature': 'INT(4)',
        'birthday': 'VARCHAR(255)',
        'degreeName': 'VARCHAR(255)',
        'id': 'INT(4)',
        'industryName': 'VARCHAR(255)',
        'photo_urls': 'TEXT(65535)'
    }
mysql_db.create_table('persons', table)

provinces = ['北京', '上海', '天津', '重庆', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门', '台湾']

for province in provinces:
    persons = get_persons_info(0, province, 18, 25)
    for i in persons:
        num = 0
        name, age, stature, birthday, degreeName, pid, industryName, photo_urls = i['nick'], i['age'], i['stature'], \
                                                                                  i['birthday'], i['degreeName'], i['id'], \
                                                                                  i['industryName'], str(i['photoList']).replace("'", '"')
        row = (name, age, province, stature, birthday, degreeName, pid, industryName, photo_urls)
        print(row)
        mysql_db.insert('persons', row)
print(mysql_db.select('persons', ''))
