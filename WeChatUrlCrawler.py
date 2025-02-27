# -*- coding: UTF-8 -*-
import requests
import time
import pandas as pd
import math
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",
]

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
cookie = "appmsglist_action_3872294534=card; qq_domain_video_guid_verify=794a419c8248bf4e; _qimei_uuid42=186090e3b1810020b5e119daf9d671a4d6c6863b34; _qimei_q36=; _qimei_h38=98e55369b5e119daf9d671a403000004618609; pgv_pvid=2295125626; _qimei_fingerprint=909aea0aea69f2aef5ecf5d71acf50fa; RK=mMGw5ymiQd; ptcz=73230320146b75980bcbf4f7071bd0dc32800510ea57c08f980aa9f49a437240; ua_id=8wpxG4BTJJbKCURlAAAAAFgUyRvS-Yj5keDcfNZxpp8=; wxuin=24145373675458; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; uin=o0547648596; skey=@s1n1ZjlhN; pac_uid=0_Np6taBHmAa98A; suid=user_0_Np6taBHmAa98A; wedrive_uin=13102672509794510; wedrive_sid=z850OIz4aWUujXRBAKxlYwAA; wedrive_skey=13102672509794510&4d286d8b25f0b7899820290ebb10ccde; wedrive_ticket=13102672509794510&CAESIObRCKkYnKvSun-HnqPBjeTf13gBwnIDAqh27Whbpjou; uuid=bf6cab1e747342fdf3f37b6beae68c16; _clck=u601up|1|fqx|0; rand_info=CAESIBWfvVjcntBCSlu3Zub+9iSMSuxwvTydqpdnc9vblfDp; slave_bizuin=3872294534; data_bizuin=3872294534; bizuin=3872294534; data_ticket=q/59RemKH+YBppsycRLaiqtxhHs7A5lNnpnjzVmizECZEk7zPr06EoeyfRx24dpf; slave_sid=ODliQ2xYREV0VEZveHUyck9tSGtfVXFNcFNMT3pFSVlQVTl4ZHAwMk1ZMG50RGpYbU1nUmxRWEVRY3hTbUtVWVZLZXFCTGc0RGxYVU9jajVFNEZ4ZUhWdWFmNVJibGVDZWdxREptSFhIeDRES2hTVDVrVk1KOVo4SkE1eWEzWGxoaVpRVUVFa1Jvd2FIbVE0; slave_user=gh_35f0187d232b; xid=d6d27c072ea75bf8747b531e3539204e; _clsk=14c6j7o|1731778169933|9|1|mp.weixin.qq.com/weheat-agent/payload/record"

# 使用Cookie，跳过登陆操作

data = {
    "token": "1639339367",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MzkwMDY2NzIxNQ==",
    "type": "9",
}
headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

    }
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(count)
page = int(math.ceil(count / 5))
print(page)
content_list = []
# 功能：爬取IP存入ip_list列表

for i in range(page):
    data["begin"] = i * 5
    user_agent = random.choice(user_agent_list)
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,

    }
    ip_headers = {
        'User-Agent': user_agent
    }
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        t = time.localtime(item["create_time"])
        items.append(time.strftime("%Y-%m-%d %H:%M:%S", t))
        content_list.append(items)
    print(i)
    if (i > 0) and (i % 10 == 0):
        name = ['title', 'link', 'create_time']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("url.csv", mode='a', encoding='utf-8')
        print("第" + str(i) + "次保存成功")
        content_list = []
        time.sleep(random.randint(60,90))
    else:
        time.sleep(random.randint(15,25))

name = ['title', 'link', 'create_time']
test = pd.DataFrame(columns=name, data=content_list)
test.to_csv("url.csv", mode='a', encoding='utf-8')
print("最后一次保存成功")