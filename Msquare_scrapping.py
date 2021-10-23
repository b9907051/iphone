import json
import datetime
import pandas as pd
import re
import requests
import platform
import shutil
#35177 各支線, 35158 FBX指數
chart_dict = {'35158':'FBX指數','35177':'FBX支線','947':'SCFI','773':'BDIBCI'}
# '773'
# search_stk = re.compile('data-stk')


for chart_num, data_name in chart_dict.items():
    url1 = f'https://en.macromicro.me/charts/{chart_num}/baltic-dry-index'
    header1 = {
    'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile':'?0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    # 使用session 連線主網頁拿到相對應的cookie
    s = requests.Session()
    r = s.get(url1,headers = header1)

    # 如何取得 Authorization header
    # 帶資料的 header 有一個參數是 Authorization 這個 heaer 
    # 觀察網頁驅動 https://en.macromicro.me/api/view/chart/773  
    # 發現是從  
    # app-2.0.0.js?v=210816A 這個JS file 發出的  
    # headers: {
    #     Authorization: "Bearer " + App.stk,
    #     Docref: document.referrer
    # }
    # 繼續尋找 APP.stk可以發現
    # App.stk = $(".footer p[data-stk]").data("stk") 帶出來的
    # 而這個$(".footer p[data-stk]") 就是去操縱網頁下 footer 這個class 的<p> 他帶的 data-stk的資料
    # 在Html 裡  <p data-stk="163e87c0038dba02a82c4d9c75808bcd">長這樣

    # 從主網頁的HTML 我們必須要拿到等下要去拿資料的 header
    # data-stk="Bearer 18114bb608a49e95fbfcf5db9807a2fe"
    # 這個是等下 Header 要帶的 Authorization token要用的
    search_stk = re.compile(r'''(
    data-stk="(\w+)"
    )''',re.VERBOSE)

    auth = search_stk.search(r.text)
    auth = auth.group(2)

    url2 = f'https://en.macromicro.me/charts/data/{chart_num}'
    header2 = {
    'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Docref': 'https://www.google.com/',
    'X-Requested-With':'XMLHttpRequest',
    'sec-ch-ua-mobile':'?0',
    'Authorization':'Bearer '+ auth,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    r = s.get(url2,headers = header2)

    response = json.loads(r.text)

    chart_num_with_c = 'c:'+chart_num
    data_list = []
    for data_num in range(len(response['data'][chart_num_with_c]['c'])):
        date = []
        price = []
        # 拿到資料的名字 第一個引數是拿第幾個資料第二個無意義
        dataname = response['data'][chart_num_with_c]['c'][data_num]['stats'][0]['stat_name']
        for i in range(len(response['data'][chart_num_with_c]['s'][data_num])):
            
            data = {}
            data['dataname'] = dataname
            data['date'] = response['data'][chart_num_with_c]['s'][data_num][i][0]
            data['price'] = response['data'][chart_num_with_c]['s'][data_num][i][1]
            data_list.append(data)
        print(dataname,len(response['data'][chart_num_with_c]['s'][data_num]))


    df = pd.DataFrame(data_list)

    if data_name == 'BDIBCI':
        df = df[(df['dataname'] == 'BDI乾散貨指數') | (df['dataname'] == 'BCI海岬型貨運指數')]

    df2 = df.pivot(index='date', columns='dataname', values='price')

    if platform.system() == "Windows":
        # Local 端
        path = f'static/data/Shipping/{data_name}.csv'
        zip_path = f'static/data/'
    else:
        # AWS 端
        path = f'/home/cathaylife04/smartphone/iphone11/static/data/Shipping/{data_name}.csv'
        zip_path = f'/home/cathaylife04/smartphone/iphone11/static/data/'

    df2.to_csv(path, encoding='utf_8_sig')

# 前面放目的地檔案, 後面放要打包的檔案目錄
shutil.make_archive( zip_path +'zipfile/Shippingdata', 'zip', zip_path + 'Shipping/')