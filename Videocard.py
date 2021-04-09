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
from datetime import datetime
import platform
import shutil
# ----------  爬取顯卡資料  ----------
# 顯卡網址
url = 'https://www.videocardbenchmark.net/gpu.php?gpu=GeForce+'

# 依照作業系統決定輸出的檔案位置
if platform.system() == "Windows":
    # Local 端
    path = 'static/data/'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/"
    
card_id_list = {'GTX+1050':'&id=3596',
'GTX+1050+Ti':'&id=3595',
'GTX+1060':'&id=3548',
'GTX+1070':'&id=3521',
'GTX+1070+Ti':'&id=3842',
'GTX+1080':'&id=3502',
'GTX+1080+Ti':'&id=3699',
'GTX+1650':'&id=4078',
'GTX+1650+SUPER':'&id=4167',
'GTX+1650+Ti':'&id=4195',
'GTX+1660':'&id=4062',
'GTX+1660+SUPER':'&id=4159',
'GTX+1660+Ti':'&id=4045',
'RTX+2060':'&id=4037',
'RTX+2060+SUPER':'&id=4117',
'RTX+2070':'&id=4001',
'RTX+2070+SUPER':'&id=4116',
'RTX+2080':'&id=3989',
'RTX+2080+SUPER':'&id=4123',
'RTX+2080+Ti':'&id=3991',
'RTX+3060+Ti':'&id=4318',
'RTX+3070':'&id=4283',
'RTX+3080':'&id=4282',
'RTX+3090':'&id=4284'
               }

search_rule = re.compile(r'''
x:\s(\d*)
.*
y:\s*(\d*\.\d*)
''',re.VERBOSE)


for key,value in card_id_list.items():
    
    website_url = url + key + value
    print(website_url)
    source = requests.get(website_url).text
    soup = Bt4(source, "lxml")
    # print(soup)
    target = soup.find_all('script')[12].string
    data = search_rule.findall(target)
    # print(data)
    res = []
    for i in range(len(data)):
        d = {}
        date = int(data[i][0])/1000
        d['date'] = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
        d['price'] = data[i][1]
#         print('date:',d['date'],'price:',d['price'])
        res.append(d)
#         print(res)
    
    df = pd.DataFrame(res)
    df.to_csv( path+'Videocard/' + key +'.csv', index=False)

# 依照作業系統決定輸出的檔案位置
output_directname = 'Videocard'
output_filename = 'Videocard'

if platform.system() == "Windows":
    # Local 端
    path = 'static/data/'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/"

shutil.make_archive( path +'/zipfile/'+output_filename, 'zip', path + output_directname)
