from datetime import datetime, date
import requests
import json
import pandas as pd
import platform


headers = {
#     "Referer": f"https://www.arrow.com/zh-cn/categories/power-management/regulators-and-controllers/linear-regulators?page=1",
"user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
}

city_list_us = {'new-york':17.81,'los-angeles':12.85,'chicago':7.11,
'san-francisco':5.78,'washington':5.63,
'dallas-fort-worth':5.45,'houston':5.18,
'boston':4.8,'philadelphia':4.63,
'atlanta':4.15,'seattle':4.13,
'san-jose':3.71,'miami':3.66,
'detroit':2.77,'minneapolis':2.76,
'phoenix':2.65,'san-diego':2.55,
'denver':2.25,'baltimore':2.13}

city_list_china = {'chongqing':8.21,'guangzhou':9.09,'shenzhen':9.51,'beijing':11.85,
             'changsha':4.46,'chengdu':5.87,'xiamen':1.84,'shanghai':12.95,'nanjing':4.95,
             'hangzhou':5.33,'wuhan':5.67,'ningbo':4.16,'tianjin':7.84}

city_list_europe = {'london':['GBR',21.79],'paris':['FRA',18.63],'madrid':['ESP',6.02],'milan':['ITA',5.64],
             'munich':['DEU',5.14],'berlin':['DEU',5.87],'amsterdam':['NLD',4.69],'barcelona':['ESP',4.45],
             'rome':['ITA',4.43],'hamburg':['DEU',4.29],'stockholm':['SWE',4.04],
             'stuttgart':['DEU',4.02],'dublin':['IRL',4.01],'brussels':['BEL',3.85]}

# 把所有國家的字典都放進 array 等等藥用迴圈處理
all_city_array = [city_list_us,city_list_china,city_list_europe]


df_result = pd.DataFrame()
# for 迴圈把 all_city_array 裡的資料全部都處理
for index in range(len( all_city_array )):

    # 我在看哪個國家 的 字典
    country = all_city_array[index]

    # 如果是歐洲國家資訊會比較複雜 第一個資訊是國家的縮寫 然後是GDP權重
    if country == city_list_europe:
        data = {key:{'dates':[],'diffratio':[],'weigh':[value[1]]} for key,value in country.items()}
        region_name = 'EU'

    elif country == city_list_us:
        data = {key:{'dates':[],'diffratio':[],'weigh':[value]} for key,value in country.items()}
        region_name = 'USA'

    else :
        data = {key:{'dates':[],'diffratio':[],'weigh':[value]} for key,value in country.items()}
        region_name = 'CHN'    


    for city in country:
        print(city)
        if region_name == 'EU':
            url = f'https://api.midway.tomtom.com/ranking/dailyStats/'+ country[city][0] + '_' + city
            print(url)
        else:
            url = f'https://api.midway.tomtom.com/ranking/dailyStats/'+ region_name + '_' + city

        r = requests.get(url,headers=headers)
        response = json.loads(r.text)

        # 把每個城市 2020與2019 的diffRatio 乘上GDP佔比以後
        for rowdata in response:
            data[city]['dates'].append(rowdata['date'])
            data[city]['diffratio'].append(rowdata['diffRatio'] * data[city]['weigh'][0] * 30 /100)

        print(city,'-- done')

    

    # 把每個城市的 'diffratio' 資料的長度放到 length 陣列裡
    length = []
    for city in country:
        length.append(len(data[city]['diffratio']))

    # 取得資料長度最小 的 數值
    shortest_length = min(length)

    for city in country:
        data_num_diff = len(data[city]['diffratio']) - shortest_length
        # 如果資料長度 比 最小的資料長度大 就捨棄多出來的資料
        if data_num_diff > 0:
            print(city,' 資料進行裁切 捨棄',data_num_diff,'筆資料')
            data[city]['dates'] = data[city]['dates'][:-data_num_diff]
            data[city]['diffratio'] = data[city]['diffratio'][:-data_num_diff]
            print(city,"   ",len(data[city]['dates']),len(data[city]['diffratio']))

    # 用 map 將取出每個城市的 diffratio 的函數 iliterate 所有的城市
    # 如果要把total diff拿來用要用list包起來不然他會是 map 的物件
    totaldiff = list(map(lambda x: data[x]['diffratio'],country.keys()))

    # *list 會把list展開
    # 沿著第二個維度計算平均並取小數點後兩位
    totaldiff = [round(sum(x),2) for x in zip( *totaldiff )]

    # 將時間字串轉成 datetime 格式
    X_axis = [datetime.strptime(str(i), "%Y-%m-%d") for i in data[city]['dates']]


    df = pd.DataFrame({'totaldiff':totaldiff,
                 'X_axis':X_axis,
                 'Region_name':region_name})

    df_result = pd.concat([df_result,df])

if platform.system() == "Windows":
    # Local 端
    # 
    path = "static/data/TomTom.csv"
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/TomTom.csv"

df_result.to_csv(path, encoding="utf_8_sig", index=False)