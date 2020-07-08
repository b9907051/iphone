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

#TODO: 把四大品牌的爬蟲 function 都建立起來
#TODO: 每次 Call 完上面的 function 以後就做一次 資料合併的動作
# Product list:

huawei_list = {"P40":'10086013232739',"P40-Pro":'10086715691479'}
vivo_list = {"NEX3S":'10001939'}
oppo_list = {"FindX2":'1119',"FindX2-Pro":'1122',"Reno4-Pro":'1401'}

# new call back
xiomi_list = {"Mi10":'2200600011',"Mi10-Pro":'2200600001'}

# old call back
# xiomi_list = {"Mi10":'10000214',"Mi10-Pro":'10000213'}

#
def update_res(res,product,price):
    d = {}
    d["Product"] = product
    d["Timestamp"] = datetime.datetime.today().strftime("%Y-%m-%d")
    d["Dealprice"] = price
    
    res.append(d)
    return res

# 華為
def get_data_huawei(res,product_list):

# P40網址
# https://www.vmall.com/product/10086013232739.html

    # num 是網址列要放的東西
    for product, num in product_list.items():
        
        website = f"https://www.vmall.com/product/{num}.html"
        source = requests.get(website).text
        soup = Bt4(source, "lxml")

        A = soup.find_all(id = "pro-price-hide")
        B = A[0]['value']
        
        price = B[:-3]
        price = int(price)

        print(product,":",price)
        update_res(res,product,price)
        
    return(res)


def get_data_vivo(res, product_list):
# VIVO
# 官網
# https://shop.vivo.com.cn/wap/product/10001939

    #NEX 3S
    url = f'https://shop.vivo.com.cn/wap/fbApi/v1/product/getDetail.json?spuId=10001939'
    r = requests.get(url)
    response = json.loads(r.text)

    price = response['data']['102963']['salePrice']
    price = int(price)
    print('NEX3S:',price)
    update_res(res,'NEX3S',price)

    # X50 Pro
    url = 'https://shop.vivo.com.cn/api/v1/product/getInstallmentDetail?skuId=105106&money=4298'
    r = requests.get(url)
    response = json.loads(r.text)
    price = response['data']['antInstallment']['perInstallmentInfoList'][0]['totalPay']
    price = int(price)
    print('X50-PRO:',price)
    update_res(res,'X50-PRO',price)
    return(res)

def get_data_oppo(res, product_list):


# oppo Reno4-Pro :https://www.opposhop.cn/products/1401.html
    for product, num in product_list.items():
        # oppo find X2 Pro
        website = f"https://www.opposhop.cn/products/{num}.html"

        source = requests.get(website).text
        soup = Bt4(source, "lxml")

        A = soup.select('p.product-price')
        B = A[0].getText()

        if product == 'FindX2':

            price = B[3:-12]
            if not price:
                print('case1')
                price = B[1:-10]

        # 如果是 FindX2-Pro
        elif product == 'FindX2-Pro':
            price = B[3:-12]

            if int(price)< 100:
                print('case2')
                price = B[1:-4]
        # 如果是 
        else:
            try:
                price = int(B[1:-4])
            except:
                price = int(B[3:-4])


        price = int(price)

        print(product,":",price)
        update_res(res,product,price)
    return(res)

def get_data_xiomi(res, product_list):
    
    # 小米10
    #https://www.mi.com/buy/detail?product_id=10000214&selected=10000214&pClass=p
    for product, num in product_list.items():
        headers = {
            "Referer": f"https://item.mi.com/product/{num}.html?selected={num}&pClass=p"
        }
        # 新的Call back
        url = f'https://api2.order.mi.com/product/dynamicv2?goods_ids=2200600011,2200600001'

        # 舊的Call back
        # url = f'https://api.order.mi.com/product/get?jsonpcallback'+\
        # f'=proget2callback&product_id={num}'

        r = requests.get(url,headers=headers)

        tt = r.text.lstrip(' proget2callback(')
        tt = tt.rstrip(');\r\n')

        response = json.loads(tt)

        price = response['data'][num]['first']['price']['price']['price']


        # if product == 'Mi10-Pro':
        #     # 5/13 mi10pro 官網改放 高規格手機 低規改到次要
        #     price = response['data']['list'][0]['list'][0]['goods']['market_price']
        # else:
        #     # 6/18 有短期降價機會
        #     price = response['data']['list'][1]['list'][0]['goods']['market_price']
            
        price = int(price)

        print(product,":",price)
        update_res(res,product,price)

    return(res)


res = []

get_data_huawei(res,huawei_list)
get_data_vivo(res, vivo_list)
get_data_oppo(res, oppo_list)
get_data_xiomi(res,xiomi_list)


if platform.system() == "Windows":
    # Local 端
    path = "static/data/1H2020.csv"
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/1H2020.csv"

Data = pd.read_csv(path)
Old_Data = Data.to_dict("records")

newres = res + Old_Data
df = pd.DataFrame(newres)
df = df.round(0)
df = df.drop_duplicates()
df.to_csv(path, encoding="utf_8_sig", index=False)
print("執行完畢")
