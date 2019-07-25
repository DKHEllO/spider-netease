#!/usr/bin/env python

"""
author: ares
date: 2019/5/20
desc:
"""

from bs4 import BeautifulSoup
import requests

from url import get_detail_page


html = get_detail_page(16699062)
bs_obj = BeautifulSoup(html)
name = bs_obj.find_all('div', {'class': 'nickwrap'}).get_text()
print(name)

