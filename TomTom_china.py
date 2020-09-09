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
city_list = {'chongqing':8.21,'guangzhou':9.09,'shenzhen':9.51,'beijing':11.85,
             'changsha':4.46,'chengdu':5.87,'xiamen':1.84,'shanghai':12.95,'nanjing':4.95,
             'hangzhou':5.33,'wuhan':5.67,'ningbo':4.16,'tianjin':7.84}

data = {key:{'dates':[],'diffratio':[],'weigh':[value]} for key,value in city_list.items()}

for city in city_list:
    url = f'https://api.midway.tomtom.com/ranking/dailyStats/CHN_' + city
    r = requests.get(url,headers=headers)
    response = json.loads(r.text)
    # 把每個城市 2020與2019 的diffRatio 乘上 GDP 佔比以後
    # 我們要計算 congestion 的程度要 把 diffratio 乘上 30 分鐘
    for rowdata in response:
        data[city]['dates'].append(rowdata['date'])
        data[city]['diffratio'].append(rowdata['diffRatio'] * 30 * data[city]['weigh'][0] /100)

length = []
for city in city_list:
    length.append(len(data[city]['diffratio']))

shortest_length = min(length)
print(shortest_length)
for city in city_list:
    data_num_diff = len(data[city]['diffratio']) - shortest_length
    
    if data_num_diff > 0:
        print(city,' 資料進行裁切 捨棄',data_num_diff,'筆資料')
        data2[city]['dates'] = data[city]['dates'][:-data_num_diff]
        data[city]['diffratio'] = data[city]['diffratio'][:-data_num_diff]
        print(city,"   ",len(data[city]['dates']),len(data[city]['diffratio']))


# 所以如果長度不一樣的話要進行資料裁切
# TODO 日期跟DIFF 都要進行裁切
totaldiff = map(lambda x: data[x]['diffratio'],city_list.keys())
totaldiff = [round(sum(x),2) for x in zip(*list(totaldiff))]
X_axis = [datetime.strptime(str(i), "%Y-%m-%d") for i in data[city]['dates']]


df = pd.DataFrame({'totaldiff':totaldiff,
             'X_axis':X_axis})

if platform.system() == "Windows":
    # Local 端
    path = "static/data/TomTom_china.csv"
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/TomTom_china.csv"

df.to_csv(path, encoding="utf_8_sig", index=False)