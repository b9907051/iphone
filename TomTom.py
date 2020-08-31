from datetime import datetime, date
import requests
import json
import pandas as pd
import platform

# 該檔案抓取TOMTOM在美國區域的 congestion

headers = {
#     "Referer": f"https://www.arrow.com/zh-cn/categories/power-management/regulators-and-controllers/linear-regulators?page=1",
"user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}
city_list = {'new-york':17.81,'los-angeles':12.85,'chicago':7.11,
'san-francisco':5.78,'washington':5.63,
'dallas-fort-worth':5.45,'houston':5.18,
'boston':4.8,'philadelphia':4.63,
'atlanta':4.15,'seattle':4.13,
'san-jose':3.71,'miami':3.66,
'detroit':2.77,'minneapolis':2.76,
'phoenix':2.65,'san-diego':2.55,
'denver':2.25,'baltimore':2.13}

data = {key:{'dates':[],'diffratio':[],'weigh':[value]} for key,value in city_list.items()}

for city in city_list:
    url = f'https://api.midway.tomtom.com/ranking/dailyStats/USA_' + city
    r = requests.get(url,headers=headers)
    response = json.loads(r.text)
    # 把每個城市 2020與2019 的diffRatio 乘上 GDP 佔比以後
    # 我們要計算 congestion 的程度要 把 diffratio 乘上 30 分鐘
    for rowdata in response:
        data[city]['dates'].append(rowdata['date'])
        data[city]['diffratio'].append(rowdata['diffRatio'] * 30 * data[city]['weigh'][0] /100)

# TODO 這裡抓完資料後發現資料長度有些沒有跟上最新的資料還沒更新上去
length = 0
for city in city_list:
    if len(data[city]['diffratio'])> length:
        # 把最長的資料長度紀錄起來
        longest_length = len(data[city]['diffratio'])
for city in city_list:
    data_num_diff = length - len(data[city]['diffratio'])
    if data_num_diff > 0:
        data[city]['dates'] = data[city]['dates'][:-data_num_diff]
        data[city]['diffratio'] = data[city]['diffratio'][:-data_num_diff]


# 所以如果長度不一樣的話要進行資料裁切
# TODO 日期跟DIFF 都要進行裁切
totaldiff = map(lambda x: data[x]['diffratio'],city_list.keys())
totaldiff = [round(sum(x),2) for x in zip(*list(totaldiff))]
X_axis = [datetime.strptime(str(i), "%Y-%m-%d") for i in data[city]['dates']]


df = pd.DataFrame({'totaldiff':totaldiff,
             'X_axis':X_axis})

if platform.system() == "Windows":
    # Local 端
    path = "static/data/TomTom.csv"
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/TomTom.csv"

df.to_csv(path, encoding="utf_8_sig", index=False)