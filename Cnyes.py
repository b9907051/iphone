# 鉅亨網 的爬蟲 要爬SCFI不同支線的數值
import requests
import json
import datetime
import pandas as pd
import re
from bs4 import BeautifulSoup
import time
from module import get_directory

# 準備舊資料

path = get_directory('Shipping/SCFI_branch.csv')
data = pd.read_csv('path.csv')
Old_Data = data.to_dict('records')

# 對 api 下達 搜尋 航運指數 的結果
url1 = 'https://ess.api.cnyes.com/ess/api/v1/siteSearch/main?\
q=%E8%88%AA%E9%81%8B%E6%8C%87%E6%95%B8&category=TW&limit=5'
s = requests.Session()
r = s.get(url1)
data = json.loads(r.text)

# 拿第一個 NEWS ID 這個ID 到時候是要每30分鐘去跟新的ID 比對
news_ID_previously = data['data']['news'][0]['newsId']

#最多讓程式跑6小時
time_limit = range(12)

for i in time_limit:
    r = s.get(url1)
    data = json.loads(r.text)
    news_ID_latter = data['data']['news'][0]['newsId']
    
    # 如果newsID 拿到的時候是新的 就開始執行資料擷取
    if news_ID_previously != news_ID_latter:
        url = f'https://news.cnyes.com/news/id/{news_ID_latter}'
        r = s.get(url)
        soup = BeautifulSoup(r.text)

        # 把 所有支線 pattern 設定好
        scfi_pattern = re.compile(r'SCFI\s綜合指數.*(\d\d\d\d.\d\d)\s點')
        east_pattern = re.compile(r'美東.*(至|到)\s(\d+)\s美元')
        west_pattern = re.compile(r'美西.*(至|到)\s(\d+)\s美元')
        europe_pattern = re.compile(r'歐洲.*(至|到)\s(\d+)\s美元')
        new_data = {}
        
        # 遍歷所有p標籤
        for i in range(len(soup.find_all('p'))):
            scfi_text = re.search(scfi_pattern,soup.find_all('p')[i].text)
            east_price_text = re.search(east_rule,soup.find_all('p')[i].text)
            west_price_text = re.search(west_rule,soup.find_all('p')[i].text)
            europe_price_text = re.search(europe_rule,soup.find_all('p')[i].text)
            # 如果是 None 的話就往下跳過
            if scfi_text is not None:
                new_data['SCFI綜合'] = scfi_text.group(1)
            elif east_price_text is not None:
                new_data['SCFI美東'] = east_price_text.group(2)
        #         east_price = int(east_price_text.group(2))
            elif west_price_text is not None:
                new_data['SCFI美西'] = west_price_text.group(2)
        #         west_price = int(west_price_text.group(2))
            elif europe_price_text is not None:
                new_data['SCFI歐洲'] = europe_price_text.group(2)
        #         europe_price = int(europe_price_text.group(2))
        new_data['Date'] = datetime.datetime.today().strftime("%Y-%m-%d")
        new_data['News_ID'] = news_ID_latter
        # 結合資料
        new_data = Old_Data + [new_data]
        data = pd.DataFrame(new_data)
        
        # 輸出資料
        data.to_csv(path,encoding='utf_8_sig',index = False)
        
        break
    else:
        # 如果 news_ID 跟之前的一樣就再等30分鐘
        print('再等30分')
        time.sleep(1800)