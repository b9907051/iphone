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
import dateparser

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'upgrade-insecure-requests': '1'}
# upgrade-insecure-requests: 1
def get_total_page(url):
    
    r = requests.get(url,headers=headers)

    soup = Bt4(r.text, "html.parser")
    tag = soup.find("span", class_="pageinfo")
    page_total = tag.get_text()
    pattern = r'(\d+)\sResults'
    product_total = int(re.findall(pattern,page_total)[0])
    page_total = math.ceil(product_total/12)
    return page_total

# post ID 拿到時間間隔
def payload_create(soup):
    tag = soup.find("div", class_="ps")
    # shipping info
    data = json.loads(tag.attrs['data-shipping-info'])
    payload_list = []
    data_item = data['items']
    for i in data_item.keys():
        payload = {}
        payload['id'] = i
        payload['articleId'] = data_item[i]['orderCode']
        payload['businessUnitId'] = data_item[i]['businessUnitId']
        payload['chassisId'] = data_item[i]['chassisId']
        payload['isDellStoreProduct'] = data_item[i]['isDellStoreProduct']
        payload['isSnP'] = data_item[i]['isSnP'] 
        payload['orderCode'] = data_item[i]['orderCode']
        payload['shippableItems'] = [data_item[i]['skus']]
        payload_list.append(payload)
        
    return payload_list

def product_list_create(tag,product_list):
    for i in range(len(tag)):
        product = {}
        try:
            product_id = tag[i]['id']

            product['ID'] = product_id

            product_data = json.loads(tag[i].find('label')['data-compare'])

            product['ModelName'] = product_data[product_id]['title']
            price = product_data[product_id]['dellPrice']
            # 抓下來的詞有 $字號 要把它取代掉
            product['Price'] = price[1:-3].replace(',','')
            
            product['Date'] = datetime.strftime(datetime.now(), "%Y-%m-%d")
            product_list.append(product)
        except:
            pass
    return product_list

product_list = []
payload_list = []

# 因為range函數會把最後一個數字丟掉 所以要+1
url_list = [
    # home
    'https://www.dell.com/en-us/shop/dell-laptops/sr/laptops',
    # business
    'https://www.dell.com/en-us/work/shop/dell-laptops/sr/laptops'
]
for url in url_list:
    # 拿到總共有幾頁
    page_total = get_total_page(url)
    for page in range(1,page_total+1):

        url_temp = url + f'?page={page}'
        
        r = requests.get(url_temp,headers=headers)
        soup = Bt4(r.text, "html.parser")
        # 拿到等下payload 的字典
        payload_list = payload_list + payload_create(soup)

        # 取出 article 的 tag 
        tag = soup.find_all('article')
        # 如果有商品的話會是數量是總共 article 的 tag量 -2
        product_list = product_list_create(tag, product_list)
        
# 藉由 set 的特性 把重複的商品ID 給拿掉
product_dict = {}
payload_dict = {}
# 把型號抽出來當作 key, 如此就不會有重複的資料存在了
for i in product_list:
    product_dict["{}".format(i['ID'])] = i
for i in payload_list:
    payload_dict["{}".format(i['orderCode'])] = i
# 把去重的payload_list,跟product_list 建起來
product_list = []
payload_list = []
for k,v in product_dict.items():
    product_list.append(v)
for k,v in payload_dict.items():
    payload_list.append(v)

print('準備好 要抓的所有頁面')

# 進行商品的 querry
url_1 = 'https://www.dell.com/csbapi/shipping/deliveryoptions/us/en/dhs/19/?zipcode=94016'
url_2 = 'https://www.dell.com/csbapi/shipping/deliverydates/us/en/bsd/04/?zipcode=94016'
headers = {
    'Content-Type': 'application/json',
#     'Host':'www.dell.com'
}
def delievery_time(r):
    if 'tomorrow' in r.text:
        date_gap = 1

    # 沒有的話 要取最後一個
    else:    
        soup1 = Bt4(r.text, "html.parser")

        date_text = soup1.find_all("td", class_="date")[0].get_text()
            # 如果日期是這樣子的話 By Thursday, Jun 23
            # if 'By' in date_text:
            #     date_text = date_text[3:]
        date = dateparser.parse(date_text)
        date_gap = (date- datetime.today()).days

    return date_gap

for i in range(len(payload_list)):
# for i in range(10):
    # 如果是要post json 記得格式要使用下面的樣子 json =...
    r = requests.post(url_1,headers=headers,json = payload_list[i])
    
    # 如果第一個 url 沒有找到產品 用第二個 url
    try:
        date_gap = delievery_time(r)
    except:
        r = requests.post(url_2,headers=headers,json = payload_list[i])
        date_gap = delievery_time(r)
        pass
    
    product_id = payload_list[i]['orderCode']
    
    try:
        # 如果 product_dict 裡面有包含 product_id:
        product_dict[product_id]['DateGAP'] = date_gap
        print('剩下',len(payload_list)-i,'個商品')
    except:
        # 如果 product_dict 裡面沒有包含 product_id的商品
        
        pass

product_list = []
# 把更新好的 dicitonary 寫進新的 product_list準備換成DF
for k,v in product_dict.items():
    product_list.append(v)


# 有一種可能是 product_list 裡面的產品 沒有在 pyload_list裡面: 網站上有這個產品 但賣完了所以沒有可運送資訊
# 直接填寫資訊為0
df = pd.DataFrame(product_list)
df['DateGAP'].fillna(0,inplace=True)

import db
from db import db as db_task
db_task.upload_data(df, 'Dell', db.router.mysql_financialdata_conn)