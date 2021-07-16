# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-06-28 13:16 
# ide： PyCharm
import json
from urllib.parse import urlencode

import requests

s = requests.session()
headers = {
    'authority': 'pjapi.jd.com',
    'method': 'Get',
    "path": '/book/sort?source=bookSort&callback=jsonp_1624940841415_40194',
    # 'scheme': 'https',
    'accept':'*/*',
    'accept-encoding': 'gzip, deflate, br',
    'referer': 'https://book.jd.com/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}
# url = 'https://pjapi.jd.com/book/sort?source=bookSort&callback=jsonp_1624856707553_24193'
url='http://list.jd.com/1713-3258-3297.html'
response = s.get(url=url, headers=headers)
t = response.text
l = t.index('{')
t = t[l:-1]
b=url+urlencode()
a = json.loads(t)
