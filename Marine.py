import requests
import json
import datetime
import pandas as pd
import numpy as np
import platform
# 有時候的登入狀態會抓不到資料:
# 要抓的港口 'ID': 港口名稱
port_ID_map = {'87':'Los Angeles','2727':'longBeach','93':'Oakland','1253':'Shanhi','1006':'Yantian',
              '290':'Singapore','172':'Hamburg','2036':'Rotterdam','199':'Felixstowe'}
#船隻種類
ship_type = ['CONTAINER SHIPS','DRY BREAKBULK','DRY BULK','LNG CARRIERS','LPG CARRIERS',
             'PASSENGER SHIPS','RO/RO','WET BULK','SUPPORTING VESSELS','OTHER MARKETS']

url = 'https://www.marinetraffic.com/en/users/ajax_login'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    ,'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
,'X-Requested-With':'XMLHttpRequest'
}
form_data = {'email': 'lay9412206@gmail.com',
'password': 'lay9821529',
'remember': '1'}
# use session to login
s = requests.Session()
#login
s.post(url,headers = headers, data = form_data)
print(s)


# Define 合併函數的裝飾函數
def merge_data_func():
    #這個區塊在進行定義函數的時候會執行
    # different_data_fun 是我們要裝飾的函數 
    def decorator(different_data_fun):
        #這個區塊在進行定義函數的時候會執行
        def warp(df,data_name):
            # 合併舊資料
            old_data = pd.read_csv(data_name).to_dict('records')
            new_data = df.to_dict('records')
            # 以陣列的型態組合以後重新合併
            df = old_data + new_data
            df = pd.DataFrame(df)
            
            # 這個函數是 每個資料需要做不同處理的地方
            df = different_data_fun(df, data_name)

            # 輸出檔案
            df.to_csv(data_name,index = False)
            
        # 這個 return 是回給 decorator
        return warp
    # 這個return 是回給 merge_data_fun
    return decorator

@merge_data_func()
def congestion(df,data_name):
    # 移除重複資料 'Calendar_Week','Port_ID','categorization' 這三個欄位重複的篩掉
    df = df.drop_duplicates(subset=['Calendar_Week','Port_ID','categorization'])
    # 排序資料
    df = df.sort_values(['Port_ID','categorization','Calendar_Week'])
    return df



# 主爬蟲

# 要抓的港口 'ID': 港口名稱
port_ID_map = {'87':'Los Angeles','2727':'longBeach','93':'Oakland','1253':'Shanhi','1006':'Yantian',
              '290':'Singapore','172':'Hamburg','2036':'Rotterdam','199':'Felixstowe'}
#船隻種類
ship_type = ['CONTAINER SHIPS','DRY BREAKBULK','DRY BULK','LNG CARRIERS','LPG CARRIERS',
             'PASSENGER SHIPS','RO/RO','WET BULK','SUPPORTING VESSELS']
# 放所有的資料的地方
result = []

# 迴圈跑所有的港口
for port_ID,port_name in port_ID_map.items():
    
    url = f'https://www.marinetraffic.com/en/ais/getHighcharts/'
    myobj = {'PORT_ID':port_ID}
    
    # 分別要去拿到達的時間 跟離開的時間
    for job in ['TaA','TaP']:
    # 如果現在要拿的是 到達的時間
        if job == 'TaA':
            myobj['configID'] = 'VesselType_TaA'
        else:
            myobj['configID'] = 'VesselType_TaP'
        r = s.post(url,headers = headers, data = myobj)
        # print(r.text)
        response = json.loads(r.text)
        for i in range(len(response)):
            if job == 'TaA':
                response[i]['categorization'] = 'Arrive'
            else:
                response[i]['categorization'] = 'Departure'

        result = response + result

df = pd.DataFrame(result)
# 轉型把數字都轉成float
# print(df.columns)
df.loc[:,ship_type] = df.loc[:,ship_type].astype(float)
# 把port_ID maping 到看得懂的名字
df['Port_ID'] = df['Port_ID'].apply(lambda x: port_ID_map[x])
# print(df['Port_ID'].to_string())
# 重新安排欄位名稱
df = df[['Calendar_Week','Port_ID','categorization','ALL','CONTAINER SHIPS','DRY BREAKBULK'
           ,'DRY BULK','LNG CARRIERS','LPG CARRIERS','PASSENGER SHIPS','RO/RO','WET BULK'
           ,'SUPPORTING VESSELS']]

print(df)
# 檔案位置
if platform.system() == "Windows":
    # Local 端
    path = 'static/data/Shipping/congestion.csv'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/Shipping/congestion.csv"

# 執行合併檔案
congestion(df,data_name = path)
