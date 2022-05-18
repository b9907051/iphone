from bs4 import BeautifulSoup as Bt4
import requests
import json
import datetime
import pandas as pd
import urllib
import time
import re
import random
import platform
from datetime import datetime
import math


# upgrade-insecure-requests: 1
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'upgrade-insecure-requests': '1'}

# 拿到所有的產品的數量
product_list = ['Laptop','Desktop']#'Workstation','Thin-Client'
pattern = r'hp-.*'
# 拿到運送時間
res = []

# 掃過每個 product
for product in product_list:
    # 紀錄商品id的list
    id_list = []
    
    url = 'https://www.hp.com/wcs/resources/store/10151/component/vwa/finder-results?'\
            f'path=vwa%2Fbusiness-solutions%2Fbizcat%3D{product}&beginIndex=0'
    r = requests.get(url,headers=headers)
    # 拿到 product裡 總共有多少個商品
    data = json.loads(r.text)
    quantity = data['vwaDetails']['totalProducts']
    print(product)
    # 進行迴圈每12個商品換一頁
    for i in range(0,int(quantity),12):
        # 把這12頁商品的 id 都串起來
        url = 'https://www.hp.com/wcs/resources/store/10151/component/vwa/finder-results?'\
        f'path=vwa%2Fbusiness-solutions%2Fbizcat%3D{product}&beginIndex={i}'
        r = requests.get(url,headers=headers)
        data = json.loads(r.text)
        for j in range(12):
            try:
                id_list.append(
                    re.findall(pattern,data['vwaDetails']['products'][j]['ctaViewDetailsLink'])[0])
            except:
                print('product missing')

    for item in id_list:
        url = 'https://www.hp.com/us-en/shop/app/api/web/graphql/page/'\
        f'pdp%2F{item}/sync'
        r = requests.get(url,headers=headers)
        data = json.loads(r.text)
        d = {}
        if 'Customizable' not in data['data']['page']['pageComponents']['productInitial']['name']:
            d['ProductType'] = product
            d['ModleName'] = data['data']['page']['pageComponents']['productInitial']['pm_model']
            d['DelieverMSG'] = data['data']['page']['pageComponents']['productInitial']['shipMessage']
            d['RegularPrice'] = data['data']['page']['pageComponents']['productInitialPrice']['regularPrice']
            d['SalePrice'] = data['data']['page']['pageComponents']['productInitialPrice']['salePrice']
            d['Date'] = datetime.strftime(datetime.now(), "%Y-%m-%d")
            d['Oid'] = data['data']['page']['pageComponents']['productInitial']['oid']
            res.append(d)


df = pd.DataFrame(res)
import db
from db import db as db_task
db_task.upload_data(df, 'HP', db.router.mysql_financialdata_conn)