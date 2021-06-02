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
import shutil



#存檔函數(要存檔的資料,存檔的名字)
def store_csv(newdata,data_name):
    # --------------------------------------- 準備新舊資料合併
    if platform.system() == "Windows":
        # Local 端
        path = f'static/data/Electronics/{data_name}.csv'
    else:
        # AWS 端
        path = f'/home/cathaylife04/smartphone/iphone11/static/data/Electronics/{data_name}.csv'

#     newdata = [newdata]
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

    df = df.drop_duplicates(subset='Timestamp', keep="last")
    # Pivot value:欲處理的資訊(相加 取平均 等等等)
    #index:列向量
    #columns:行向量
    # path
    df.to_csv(path,encoding='utf_8_sig', index=False)



# newdata 是為了儲存到時要給網頁讀的csv
newdata = {}
# newdata_detail 是為了讓研究員 檢查數據 所紀錄的資料
newdata_detail_low = []
newdata_detail_high = []

# 拿到一年前的日期 協理指示我們只要看一年內的產品 52weeks
datetimenow = datetime.datetime.now()
one_year_earlier = datetimenow - datetime.timedelta(weeks=52)
one_year_earlier = datetime.datetime.strftime(one_year_earlier, "%Y-%m-%d")


product_list = {
    'laptop':'pcmcat138500050001'
}

# 把價格高到低 和低到高的資訊都抓出來
for product,code in product_list.items():
    # 搜索某個類別按價格排序(低到高)(條件:要是可以購買的狀態 orderable=Available)
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=Available&startDate>{one_year_earlier})'\
    '?format=json&show=salePrice,name&pageSize=100&sort=salePrice&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)

    lowprice = []
    low_item = []
    newdata_temp = {}
    for i in range(0,100):
        # 如果 Refurbished 在商品名稱裡就是整新機，要全部移除掉
        if 'Refurbished' not in response['products'][i]['name']:   
            lowprice.append(response['products'][i]['salePrice'])
            
            newdata_temp = {}
            newdata_temp['lowprice_'+ product ] = response['products'][i]['salePrice']
            newdata_temp['low_item'+ product ] = response['products'][i]['name']
            newdata_temp['Timestamp' ] = datetime.datetime.strftime(datetimenow, "%Y-%m-%d")
            newdata_detail_low.append(newdata_temp)
            
            if len(newdata_detail_low) >= 50:
                break
    newdata['lowprice_average'] = round(np.average(lowprice),2)
    df_lowprice = pd.DataFrame(newdata_detail_low)
    
#     newdata['lowprice_average_'+ product ] = round(np.average(lowprice),2)
#     newdata_detail['lowprice_'+ product ] = round(np.average(lowprice),2)
#     newdata_detail['low_item'+ product ] = round(np.average(lowprice),2)
    
#     # 搜索某個類別按價格排序(高到低)(條件:要是可以購買的狀態 orderable=Available)
    url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=Available&startDate>{one_year_earlier})'\
    '?format=json&show=salePrice,name&pageSize=100&sort=salePrice.dsc&apiKey=qhqws47nyvgze2mq3qx4jadt'
    r = requests.get(url)
    response = json.loads(r.text)

    highprice = []
    for i in range(0,100):
        if 'Refurbished' not in response['products'][i]['name']:  
            highprice.append(response['products'][i]['salePrice'])

            newdata_temp = {}
            newdata_temp['highprice_'+ product ] = response['products'][i]['salePrice']
            newdata_temp['high_item'+ product ] = response['products'][i]['name']
            newdata_detail_high.append(newdata_temp)
            
            if len(newdata_detail_high) >= 50:
                break
    newdata['highprice_average'] = round(np.average(highprice),2)
    df_highprice = pd.DataFrame(newdata_detail_high)
#     url = f'https://api.bestbuy.com/v1/products(categoryPath.id={code}&orderable=SoldOut&startDate>{one_year_earlier})'\
#     '?format=json&show=orderable&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
#     r = requests.get(url)
#     response = json.loads(r.text)
#     soldout_amount = response['total']

    # 價格部份的檢查資訊在這裡了
    newdata_detail_price = pd.concat([df_lowprice,df_highprice],axis=1)
    # 還是要轉換成 dictionary 跟舊資料合併
    newdata_data_detail_price = newdata_detail_price.to_dict('records')
    # 存檔
    store_csv(newdata_data_detail_price,'data_detail_HLprice'+product)
    print('輸出所有價格排序的細節')


# 所有產品的資訊 以及 產品的統計數據
url = f'https://api.bestbuy.com/v1/products(categoryPath.id=pcmcat138500050001&startDate>{one_year_earlier})'\
'?format=json&show=name,regularPrice,salePrice,onSale,orderable,&pageSize=100&apiKey=qhqws47nyvgze2mq3qx4jadt'
r = requests.get(url)
response = json.loads(r.text)
totalpage = response['totalPages']
product_list = {
    'laptop':'pcmcat138500050001'
}
newdata_status = []
total_amount = 0
soldout_amount = 0
ordeble_amount = 0
onsale_amount = 0
non_onsale_amount = 0
#totalpage 在range裡面不包括totalpage
# print(totalpage)
for product,code in product_list.items():
    for page in range(1,totalpage+1):
        url = f'https://api.bestbuy.com/v1/products(categoryPath.id=pcmcat138500050001&startDate>{one_year_earlier})'\
        f'?format=json&show=name,regularPrice,salePrice,onSale,orderable,startDate&pageSize=100&page={page}&apiKey=qhqws47nyvgze2mq3qx4jadt'
        r = requests.get(url)

        response = json.loads(r.text)
        # 每頁有幾個產品
        item_in_page = response['to']-response['from']+1

        for i in range(0,item_in_page):
            # 排除整新機 ---
            if 'Refurbished' not in response['products'][i]['name']:  
                newdata_temp = {}

                #------ 紀錄細部資料 -----#
                newdata_temp['timestamp' ] = datetime.datetime.strftime(datetimenow, "%Y-%m-%d")
                newdata_temp['regularPrice_'+ product ] = response['products'][i]['regularPrice']
                newdata_temp['salePrice'+ product ] = response['products'][i]['salePrice']
                newdata_temp['item_'+ product ] = response['products'][i]['name']
                newdata_temp['orderable_'+ product ] = response['products'][i]['orderable']
                newdata_temp['onSale_'+ product ] = response['products'][i]['onSale']
                newdata_temp['sale_start_date'] = response['products'][i]['startDate']
                newdata_status.append(newdata_temp)

                #------ 紀錄要做計算的數字---#
                # 所有商品的數量
                total_amount += 1
                # 使用商品現在可不可以購買 來統計 賣完 以及 還可以買的數量
                if response['products'][i]['orderable'] == 'Available':
                    ordeble_amount += 1
                    # 在可以購買商品的狀態下 如果 有打折的話:
                    if response['products'][i]['onSale'] == True:
                        onsale_amount += 1
                    else:
                        non_onsale_amount += 1
                else:
                    soldout_amount += 1
                    
                    
    newdata['soldout_percent'] = round(soldout_amount/total_amount*100,2)
    newdata['onsale_percent'] = round(onsale_amount/ordeble_amount*100,2)
    newdata['total_amount'] = total_amount
    newdata['ordeble_amount'] = ordeble_amount
    newdata['soldout_amount'] = soldout_amount
    newdata['onsale_amount'] = onsale_amount
    newdata['non_onsale_amount'] = non_onsale_amount
    newdata['timestamp'] = datetime.datetime.strftime(datetimenow, "%Y-%m-%d")
    store_csv([newdata],'bestbuy_'+product)
    print('輸出統計資料')
    store_csv(newdata_status,'data_detail_allproduct_'+product)
    # print('onsale_percent:',newdata['onsale_percent'])

    # print('total_amount:',newdata['total_amount'])
    # print('ordeble_amount:',newdata['ordeble_amount'])
    # print('soldout_amount:',newdata['soldout_amount'])
    # print('onsale_amount:',newdata['onsale_amount'])
    # print('non_onsale_amount:',newdata['non_onsale_amount'])
    print('輸出所有商品細節')

    
#----- 將檔案打包成 zip file -------
# product = 'laptop'
if platform.system() == "Windows":
    # Local 端
    path = 'static/data'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data"
output_direct = '/Electronics/'
output_filename = 'Bestbuy_'+product
# 打包所有檔案到zip
shutil.make_archive( path +'/zipfile/'+output_filename, 'zip', path + output_direct)
print('打包zip 成功')