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

1227

product_index = {
    # Oppo
    # 'Opporeno':['1262','1261155'],
    # 小米
    # '小米9':['1225','1224655'],
    # 華為
    # '華為P30':['1213','1212233'],'華為P30Pro':['1224','1223829'],
    "華為-Mate30": ["1294", "1293856"],
    "華為-Mate30-5G": ["1239", "1238183"],
    "華為-Mat30Pro": ["1294", "1293857"],
    "華為-Mat30Pro-5G": ["1266", "1265181"],
    # Vivo
    "Vivo-X27": ["1263", "1262905"],
    "Vivo-Nex3": ["1286", "1285391"],
    "Vivo-Nex3-5G": ["1292", "1291141"],
    # 三星
    "三星-Note10": ["1206", "1205967"],
    "三星-Note10-5G": ["1286", "1285705"],
}

# 為了方便接下來 不同的 網頁index 進行 產品  的對應 將 key 跟 產品互換
# 舉例 product_index {1261155: 'Opporeno',...}
product_R = {value[1]: key for key, value in product_index.items()}

res = []
for key, index in product_index.items():

    d = {}

    website = f"http://detail.zol.com.cn/{index[0]}/{index[1]}/price_1.shtml"

    source = requests.get(website).text
    soup = Bt4(source, "html.parser")
    price = soup.find("em", class_="price-type").text
    # print(price)
    # print(soup.prettify())
    d["Product"] = product_R[index[1]]
    d["Timestamp"] = datetime.datetime.today().strftime("%Y-%m-%d")
    d["Price"] = price
    print(d)
    res.append(d)

if platform.system() == "Windows":
    # Local 端
    path = "static/data/Zhongguancun.csv"
else:
    # AWS 端
    path = "/home/ubuntu/iphone11/mainweb/static/data/Zhongguancun.csv"

Data = pd.read_csv(path)
Old_Data = Data.to_dict("records")
newres = res + Old_Data
df = pd.DataFrame(newres)
df = df.drop_duplicates()
df.to_csv(path, encoding="utf_8_sig", index=False)
print("執行完畢")
