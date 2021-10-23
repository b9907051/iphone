# from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from functools import wraps
import requests
import json
import datetime
import pandas as pd
import platform
import shutil
import datetime
from module import delivermsg_to_num
import time
from module.Apple_ID.all_id import *
import random
import math

if platform.system() == "Windows":
    # Local 端
	path = 'static/data/Data.csv'
else:
    # AWS 端
	path = "/home/cathaylife04/smartphone/iphone11/static/data/Data.csv"


# path = 'static/data/Data.csv'
Data = pd.read_csv(path)
Old_Data = Data.to_dict('records')

# 把
headers = {
'sec-ch-ua':'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':"Windows",
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
'upgrade-insecure-requests': '1'
}
s = requests.Session()
# 把 預期要刪掉的字串組成 list 傳到 function裡
bagofwords = [' – 送料無料',' — Free',' – 免額外付費']

# 引數前面加星號 就是不預設有幾個變數
def replacestring(x,*bagofwords):
    for text in bagofwords:
        if text in x:

            y = x.replace(text,'')
            return y
    return x

# 使用try except 解決可能遇到的反爬蟲機制
# 傳入 d產品資訊, url產品的連結
def anti_scrapping(d,url):
    while True:
        try:
            print(url)
            r = s.post(url,headers = headers)
            response = json.loads(r.text)
            d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['deliveryOptionMessages'][0]['displayName']
            exec('d["Day"] = delivermsg_to_num.'+d['Country']+'(d["Deliver"],d["TimeStemp"])')
            print(d)
            time.sleep(1)
        # 如果被反爬蟲的話持續進行這個迴圈
        except Exception as e:
            print('被反爬蟲',str(e))
            # f = random.uniform(1, 10)
            # time.sleep(math.floor(f * 10) / 10.0)
            time.sleep(2)
            continue
        # 如果try 成功的話 break 迴圈
        else:
            break
    return d,res,url_fail_list

res=[]
# 如果被反爬蟲擋下來
url_fail_list = []
# 美國的要單獨跑 因為地址網址的dictionary 是空的
# count = 0
for Model in Model_Us:

    # count = count +1
    # if count % 30 == 0 :
    #     time.sleep(5)
	# if Product_Us_R[Model] == 'IpadPro':
	# print(Model)
    d = {} #清空dictionary
    d['Country'] = 'Us'
    d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")
    d['Product'] = Product_Us_R[Model]

    # try:
    # 如果是AirPodPro 因為沒有Size也沒有Color的資訊所以 除了 AirPodPro 以外其他產品都有Color 跟 Size 的 key
    if Product_Us_R[Model] == 'AirPodPro':

        url = 'https://www.apple.com/shop/fulfillment-messages?parts.0=%s&little=true' % ( Model )
        d,res,url_fail_list = anti_scrapping(d,url)
        res.append(d)

    # 產品線是 AppleWatch 系列 或是 iPad 系列
    elif Product_Us_R[Model][0:10] == 'AppleWatch' or Product_Us_R[Model][0:4] == 'iPad':
    # Applwatch6 及 AppleWatchSE 的型號要塞 兩個 變得比較複雜了所以要單獨處理
        if Product_Us_R[Model] == 'AppleWatch6' or Product_Us_R[Model] == 'AppleWatchSE':
            url = f'https://www.apple.com/shop/fulfillment-messages?parts.0=Z0YQ&option.0='+ Model +'&little=true'
            d['Celluar'] = Celluar_R[Model]
            d['Size'] = Size_R[Model]

            d,res,url_fail_list = anti_scrapping(d,url)


        else:
            url = f'https://www.apple.com/shop/fulfillment-messages?parts.0='+ Model + '&little=true'
            d,res,url_fail_list = anti_scrapping(d,url)

        # 如果是iPad 則多了 Colar 這個 項目
        if Product_Us_R[Model][0:4] == 'iPad':
            d['Colors'] = Color_R[Model[0:5]]

        # 如果產品不是 Apple watch6 跟 ApplewatchSE
        if 'Celluar' not in d.keys():
            d['Celluar'] = Celluar_R[Model[0:5]]
            d['Size'] = Size_R[Model[0:5]]

        # d['Days'] = delivermsg_to_num.Us(d['Deliver'],d['TimeStemp'])
        # d["Days"] = eval('delivermsg_to_num.'+d['Country']+'(d["Deliver"],d["TimeStemp"])')

        res.append(d)
    #一般的產品線:
    else: 
    # 如果找不到 Size 就 不去做request. 產品都會對 Size 256GB做下架  

        url = 'https://www.apple.com/shop/fulfillment-messages?mt=regular&parts.0=%s&little=true' % ( Model )
        d['Colors'] = Color_R[Model[0:5]]
        d['Size'] = Size_R[Model[0:5]]
        d,res,url_fail_list = anti_scrapping(d,url)
        res.append(d)
            # print(url)
            # f = random.uniform(1, 1.5)
            # time.sleep(math.floor(f * 10) / 10.0)
            # r = requests.get(url)
            # response = json.loads(r.text)


for Product in countries:
	#外迴圈跑國家
    for Country in countries[Product]:
    #內迴圈跑型號
        for Model in countries[Product][Country]:
            # if Product_R[Model] == 'IpadPro':
            d = {} #清空dictionary
            # 現在 要處理新增的選項一樣丟在color裡嗎XD
            d['Country'] = Country
            d['Product'] = Product_R[Model]
            d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")

            # try:

                # 如果是AirPod 因為沒有Size也沒有Color的資訊所以單獨處理
            if Product_R[Model] == 'AirPodPro':

                url = 'https://www.apple.com/%s/shop/fulfillment-messages?parts.0=%s&little=true' % (d['Country'].lower(), Model)

                d,res,url_fail_list = anti_scrapping(d,url)
                res.append(d)

            # 產品線是 AppleWatch 系列 或是 iPad 系列
            elif Product_R[Model][0:10] == 'AppleWatch' or Product_R[Model][0:4] == 'iPad':

                # Applwatch6 及 AppleWatchSE 的型號要塞 兩個 變得比較複雜了
                if Product_R[Model] == 'AppleWatch6' or Product_R[Model] == 'AppleWatchSE':

                    url = f'https://www.apple.com/'+ d['Country'].lower() +'/shop/fulfillment-messages?parts.0=Z0YQ&option.0='+ Model +'&little=true'
                    r = requests.get(url)
                    response = json.loads(r.text)
                    deliver_string = response['body']['content']['deliveryMessage']['Z0YQ']['deliveryOptionMessages'][0]['displayName']

                    d['Deliver'] = replacestring(deliver_string,*bagofwords)
                    d['Celluar'] = Celluar_R[Model]
                    d['Size'] = Size_R[Model]
                else:

                    url = 'https://www.apple.com/%s/shop/fulfillment-messages?parts.0=%s&little=true' % (d['Country'].lower(), Model)
                    d,res,url_fail_list = anti_scrapping(d,url)


                # 如果是iPad 則多了 Colar 這個 項目
                if Product_R[Model][0:4] == 'iPad':
                    d['Colors'] = Color_R[Model[0:5]]

                # 如果產品不是 Apple watch6 跟 ApplewatchSE
                if 'Celluar' not in d.keys():
                    d['Celluar'] = Celluar_R[Model[0:5]]
                    d['Size'] = Size_R[Model[0:5]]
                
                res.append(d)

			#一般的產品線:
            else:
            # 如果找不到 Size 就 不去做request. 產品都會對 Size 256GB做下架	
                
                url = 'https://www.apple.com/%s/shop/fulfillment-messages?mt=regular&parts.0=%s&little=true' % (d['Country'].lower(), Model)

                d['Colors'] = Color_R[Model[0:5]]
                d['Size'] = Size_R[Model[0:5]]

                d,res,url_fail_list = anti_scrapping(d,url)
                res.append(d)

            # except:
                # print(d,'下架')


newres = res + Old_Data
# newres = res
df = pd.DataFrame(newres)
df = df.drop_duplicates()
# Pivot value:欲處理的資訊(相加 取平均 等等等)
#index:列向量
#columns:行向量
# path
# df.to_csv(path,encoding='utf_8_sig', index=False)


# #要去哪裡
# destname = "/home/ec2-user/Mainweb/static/Data.csv"
# #來源資料
# fromname = "/home/ec2-user/Mainweb/Data.csv"
# shutil.copy2(fromname, destname)

print("ok")