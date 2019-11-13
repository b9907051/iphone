import csv
import pandas as pd
import math
import json
import numpy as np
import itertools
from . import dailydata_to_weeklydata as dw
from . import impose_none as impn

#TODO 因為天貓的main_info有兩個資訊 我想要在使用dw的時候可以一次把兩個資訊(Volume,Price)都處理完畢
#TODO 最大值 Max_info 有回傳出去 我想要增加最小值的回傳
#TODO 所以如果是在天貓的情況Max_info Min_info 會各有兩個資料,要決定哪一個index要填入Main_info的資訊


def get_csv(datasource, mainInfo, timeperiod="week"):

    if datasource == "Zhongguancun":
        Read_data = pd.read_csv("static/data/Zhongguancun_V2.csv", encoding="utf-8")
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
            tempdata = df.to_dict(orient='list')
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
    # print(product_info)
    # print(product_info)
    if timeperiod == "week":
        product_info = dw.dailydata_to_weeklydata(product_info, mainInfo) 
        # print(product_info)

    max_info = [] 
    timestamp_index_in_list = []
    for key,value in product_info.items():
        max_info.append(value[mainInfo])
        timestamp_index_in_list.append(value['Timestamp'])
    # Max 函數如果碰到mutlti dimension 會先以axis = 1 的方向sum
    # itertools 的用法 https://docs.python.org/zh-cn/3/library/itertools.html
    # itertools.chain.from_iterable() 會把目標陣列展開 (flatten array)

    # max_info = max(itertools.chain.from_iterable([info[mainInfo] for row in data for info in row.values()]))
    max_info = max(itertools.chain.from_iterable(max_info))
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
