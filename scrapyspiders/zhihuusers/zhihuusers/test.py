# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-07-05 13:42 
# ide： PyCharm
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'method': 'GET',
    'authority': 'www.zhihu.com',
    'path': '/api/v4/members/mythly/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'referer': 'https://www.zhihu.com/people/mythly/following',
    'x-ab-param': 'tp_contents=2;qap_question_author=0;tp_dingyue_video=0;pf_noti_entry_num=0;tp_topic_style=0;pf_adjust=0;zr_slotpaidexp=1;zr_expslotpaid=1;qap_question_visitor= 0;top_test_4_liguangyi=1;se_ffzx_jushen1=0;tp_zrec=0',
    'x-ab-pb': 'CowBuwPkCqMDVgxgC6YBxwLCAtcLAQtnAGkBygKaA68DNwy1CzsCzAJXA6EDBwwqA40BwAL2AqADGwBSC0MAbQJyA0UD3Au5AnQBhAJqAVADtAqMAg8LmQOJDEcAtABsAyoCNAx9AsECmwurA9gCQAEyA6IDzwvsCj8AnwKLA7cATwHXAvQL4AuJAk8DRQISRgAAAAEAAAAAAAAAAAAAAAEDAAAAAAABAAAAAAABGAAAAAALAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAsBAAABAAAAAAAAAAA=',
    'x-requested-with': 'fetch',
    'x-zse-93': '101_3_2.0',
    'x-zse-96': '2.0_aMF0k7u068tYSLtyY0NBc6rqH92pQLFBs8x0ciuBb7Yp'}
import requests

a = requests.get('http://www.zhihu.com/api/v4/members/mythly/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20', headers=headers)
print(a.text)
