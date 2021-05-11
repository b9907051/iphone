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
import numpy as np


product_list = {
    'laptop':'pcmcat138500050001'
}

newdata = {}

for product,code in product_list.items():

    # 我們直接取排名50個
    # 搜索某個類別按價格排序(低到高)(條件:要是可以購買的狀態 orderable=Available)
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=Available )'\
    '?format=json&show=salePrice&pageSize=50&sort=salePrice&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)

    lowprice = []
    for i in range(0,50):
        lowprice.append(response['products'][i]['salePrice'])
    newdata['lowprice_average_'+ product ] = round(np.average(lowprice),2)

    # 搜索某個類別按價格排序(高到低)(條件:要是可以購買的狀態 orderable=Available)
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=Available )'\
    '?format=json&show=salePrice&pageSize=50&sort=salePrice.dsc&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)

    highprice = []
    for i in range(0,50):
        highprice.append(response['products'][i]['salePrice'])
    newdata['highprice_average_'+ product] = round(np.average(highprice),2)

    # 搜索某個類別全部的商品
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&(orderable=Available|orderable=SoldOut))'\
    '?format=json&show=onSale&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)
    total_amount = response['total']
    print('total_amount:',total_amount)

    # 搜索某個類別在架上的商品
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=Available)'\
    '?format=json&show=onSale&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)
    orderable_amount = response['total']
    print('orderable_amount:',orderable_amount)

    # 搜索某個類別有打折且在架上的商品
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&onSale=true&orderable=Available)'\
    '?format=json&show=onSale&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)
    onsale_amount = response['total']
    print('onsale_amount:',onsale_amount)


    # 搜索某個類別賣光的商品
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=SoldOut)'\
    '?format=json&show=orderable&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)
    soldout_amount = response['total']
    print('soldout_amount:',soldout_amount)


    # 賣光比: 所有賣光的量/所有商品量
    newdata['soldout_percent_'+ product] = round(soldout_amount/total_amount*100,2)
    print('sold_outratio',newdata['soldout_percent_'+ product])

    # 打折比比: 所有打折的量/所有架上商品量
    newdata['onsale_percent_'+ product] = round(onsale_amount/orderable_amount*100,2)
    print('onsale_percent',newdata['onsale_percent_'+ product])

    # 加上時間戳記
    newdata['timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")


    # --------------------------------------- 準備新舊資料合併
    if platform.system() == "Windows":
        # Local 端
        path = 'static/data/Electronics/bestbuy.csv'
    else:
        # AWS 端
        path = "/home/cathaylife04/smartphone/iphone11/static/data/Electronics/bestbuy.csv"

    newdata = [newdata]
    # Read Old Data 
    try:
        # 如果沒有Data
        Data = pd.read_csv(path)
        Old_Data = Data.to_dict('records')
        newdata = newdata + Old_Data
    except:
        print('no old data')

    df = pd.DataFrame(newdata)
    # drop 重複的某個欄位資訊
    # https://stackoverflow.com/questions/12497402/python-pandas-remove-duplicates-by-columns-a-keeping-the-row-with-the-highest
    df = df.drop_duplicates(subset='timestamp', keep="first")
    # Pivot value:欲處理的資訊(相加 取平均 等等等)
    #index:列向量
    #columns:行向量
    # path
    df.to_csv(path,encoding='utf_8_sig', index=False)