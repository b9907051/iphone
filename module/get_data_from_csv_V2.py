import csv
import pandas as pd
import math
import json
import numpy as np
import itertools
from . import dailydata_to_weeklydata as dw
from .impose_none import impose_none as impn

#TODO 因為天貓的main_info有兩個資訊 我想要在使用dw的時候可以一次把兩個資訊(Volume,Price)都處理完畢
#TODO 最大值 Max_info 有回傳出去 我想要增加最小值的回傳
#TODO 所以如果是在天貓的情況Max_info Min_info 會各有兩個資料,要決定哪一個index要填入Main_info的資訊


def get_csv(datasource, mainInfo, timeperiod="week"):

    if datasource == "Zhongguancun":

        Read_data = pd.read_csv("static/data/Zhongguancun_V2.csv", encoding="utf-8")
        # 如果現在不是在虛擬環境下的話路徑使用
        # Read_data = pd.read_csv("static/data/Zhongguancun.csv")
        product_info = {}
        country_list = Read_data["Product"].unique()
        for country in country_list:
            temp = Read_data[Read_data['Product'] == product]
            df = pd.pivot_table(
            temp,
            index=["Timestamp"],
            values=["Dealprice"],
            )
            df['Timestamp'] = df.index

            tempdata = df.to_dict(orient='list')

            tempdata = {product:tempdata}
            product_info.update(tempdata)

    # 中國 5G 手機的資料
    elif datasource == "1H2020":

        Read_data = pd.read_csv("static/data/1H2020.csv", encoding="utf-8")
        # 如果現在不是在虛擬環境下的話路徑使用
        # Read_data = pd.read_csv("static/data/Zhongguancun.csv")
        product_info = {}
        product_list = Read_data["Product"].unique()

        for product in product_list:
            temp = Read_data[Read_data['Product'] == product]
            df = pd.pivot_table(
            temp,
            index=["Timestamp"],
            values=["Dealprice"],
            )
            df['Timestamp'] = df.index

            # orient 使用 ='list' 就是使用 list 去把資料存起來 然後外層包一個dictionary
            # ex: {'Dealprice': [4488, 4488, 4488],'Timestamp':['2020-04-14', '2020-04-15', '2020-04-16']}
            tempdata = df.to_dict(orient='list')
            # print(tempdata)

            
            tempdata = {product:tempdata}
            product_info.update(tempdata)


    else:

        Read_data = pd.read_csv("static/data/Tmall5g.csv", encoding="utf-8")
        product_info = {}
        product_list = Read_data["Product"].unique()
        for product in product_list:
            temp = Read_data[Read_data['Product'] == product]
            df = pd.pivot_table(
            temp,
            index=["Timestamp"],
            values=["Dealnumber", "Dealprice"],
            aggfunc={"Dealnumber": np.sum, "Dealprice": np.mean},
            )

            df['Dealnumber'] = df['Dealnumber'].diff(1)
            df['Timestamp'] = df.index
            df.dropna(inplace=True)

            tempdata = df.to_dict(orient='list')
            tempdata = {product:tempdata}
             # dictionary 資料擴展的方法 把每個產品一個一個加到裡面
            product_info.update(tempdata)

    if timeperiod == "week":
        product_info = dw.dailydata_to_weeklydata(product_info, mainInfo) 
        # print(product_info)

    # 如果數據是 後來才開始 Update 的話 前面的數字要補 Nan 才能將資料對齊到對的時間
    # 我們使用 impn function 來做這件事
    product_info = impn(product_info,'Dealprice')


    max_info = [] 
    timestamp_index_in_list = []

    for key,value in product_info.items():
        max_info.append(value[mainInfo])
        timestamp_index_in_list.append(value['Timestamp'])

    # Max 函數如果碰到mutlti dimension 會先以axis = 1 的方向sum
    # itertools 的用法 https://docs.python.org/zh-cn/3/library/itertools.html
    # itertools.chain.from_iterable() 會把目標陣列展開 (flatten array)

    # 試看看直接計算資料裡面有沒有 NaN
    try:
    # if datasource == "1H2020":
        # print(pd.core.common.flatten(max_info))
        max_info = max(itertools.chain.from_iterable(max_info))

    except:
        # 如果 要計算的 list 裡面 有 Nan 要先把list 轉成 nparray 再利用 np.nanmax來忽略 nan 進行計算
        max_info = list(itertools.chain.from_iterable(max_info))
        max_info = np.array(max_info, dtype=np.float64)
        max_info = np.nanmax(max_info)

    power = math.floor(math.log(max_info, 10))

    # 找尋長度最大的陣列
    timestamp_index_in_list = max(timestamp_index_in_list, key=len)

    product_info["X_axis"] = timestamp_index_in_list
    product_info["Max_info"] = math.ceil(max_info / (10 ** power)) * (10 ** power)

    product_info['Main_info'] = mainInfo
    product_info['Time_period'] = timeperiod
    product_info['Step'] = 10**power/2
    # print(product_info)
    return json.dumps(product_info, default=str)
