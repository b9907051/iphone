import csv
import pandas as pd
import math
import json
import numpy as np
from . import dailydata_to_weeklydata as dw
from . import impose_none as impn


def get_csv(datasource, maininfo, timeperiod="week"):

    if datasource == "Zhongguancun":
        Read_data = pd.read_csv("static/data/Zhongguancun.csv", encoding="utf-8")
        # 如果現在不是在虛擬環境下的話路徑使用
        # Read_data = pd.read_csv("static/data/Zhongguancun.csv")
        df = Read_data

    else:
        Read_data = pd.read_csv("static/data/Tmall5G.csv", encoding="utf-8")
        # 把同一個產品同一個時間  所有的代理商[Shopname]的 銷售數字[Dealnumber] 加起來
        # 所有代理商的 銷售價格[Dealprice] 做平均

        # df = Read_data.groupby(["Timestamp", "Product"], as_index=False).sum()
        # TODO 把 Dealnumber Dealprice 分別做 sum 跟平均
        df = pd.pivot_table(
            Read_data,
            index=["Timestamp", "Product"],
            values=["Dealnumber", "Dealprice"],
            aggfunc={"Dealnumber": np.sum, "Dealprice": np.mean},
        )
        # df.reset_index(inplace=True) 這個動作可以幫我把 multiindex 補充起來
        # eg: df =
        # 2019-10-21 AAA TTT   2019-10-21 AAA TTT
        #            BBB GGG → 2019-10-21 BBB GGG
        #            CCC PPP   2019-10-21 CCC PPP
        df.reset_index(inplace=True)

    # TODO SUM DEALNUMBER GROUP BY TIMESTAMP PRODUCT
    # as_index = False 可以幫我補足 groupby 自動幫我做分組的欄位

    data = df.to_dict("records")
    columns = list(df.columns)
    Max_info = max([int(row[maininfo]) for row in data])

    power = math.floor(math.log(Max_info, 10))

    Product_name = df["Product"].unique()
    Product_info = {k: [] for k in Product_name}
    for key in Product_info.keys():
        Product_info[key] = {"Timestamp": [], maininfo: []}

    for row in data:  # rows = {product:apple',price:'250',Timestamp:
        Product = row["Product"]
        Mainfo = row[maininfo]
        Timestamp = row["Timestamp"]
        # 這裡有個error處理了兩小時 dictionary 不能 Append 所以
        # Dictionary 在value職擴增的時候要先把他包成串列
        Product_info[Product][maininfo] += [Mainfo]
        Product_info[Product]["Timestamp"] += [Timestamp]

    # print(Product_info.values())

    if timeperiod == "week":
        Product_info = dw.dailydata_to_weeklydata(Product_info, maininfo)

    # map 函數會對 list 的每個元素進行 lambda 匿名函數的映射
    # EX: a = map(lambda x:x+10,[1,2,3,4])
    # list(a) = [11, 12, 13, 14]
    # max(,key=len)會拿到最長的串列
    Timestamp_index_in_list = max(
        map(lambda x: x["Timestamp"], list(Product_info.values())), key=len
    )
    # 送進去 impose_none 函數裡只能有兩個東西 所以 MaxPrice的部分到後面再放
    Product_info = impn.impose_none(Product_info, maininfo)

    Product_info["X_axis"] = Timestamp_index_in_list
    Product_info["Max_info"] = math.ceil(Max_info / (10 ** power)) * (10 ** power)
    # print(Product_info)
    return json.dumps(Product_info, default=str)
