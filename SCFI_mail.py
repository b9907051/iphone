# 外部套件
import os
import pandas as pd
import numpy as np
import platform

from module.zscore import *
from module.mail_module import send_mail
# 加入最新的資料
def data_preprocess(data_csv):

    if platform.system() == "Windows":
        # Local 端
        path = f'static/data/Shipping/' + data_csv
        zip_path = f'static/data/'
    else:
        # AWS 端
        path = f'/home/cathaylife04/smartphone/iphone11/static/data/Shipping/'+ data_csv
        zip_path = f'/home/cathaylife04/smartphone/iphone11/static/data/'

    df = pd.read_csv(path,encoding = 'utf_8_sig')
    df['date'] = pd.to_datetime(df['date'],format = '%Y-%m-%d')
    #資料如果有NA就拿掉整列
    df.dropna(axis='rows',how = 'any',inplace = True)
    
    # 把 index 換成日期 並把原本日期的欄位丟掉
    df.index = df['date']
    # 留下字串有SCFI的表格
    if data_csv == 'SCFI':
        df = df.filter(regex=data_csv)

    # 如果是BDI or BCI 的資料
    # 拿掉date欄位
    else:
        df = df.drop(columns='date')
        # 倒著排序 因為 這樣才可以確保等下是前面 N 組數據進行平均
        df = df[::-1]
        # 創造一個陣列 數字//N 表示留下商數捨去餘數
        df = df.groupby(np.arange(len(df))//5).mean()
        # 再倒回來一次
        df = df[::-1]
    # 拿掉date欄位
    return (df)
    
    
df_SCFI = data_preprocess('SCFI.csv')
df_BDIBCI = data_preprocess('BDIBCI.csv')

mailcontent_plus_SCFI,mailcontent_minus_SCFI = mail_content(df_SCFI,'SCFI')
mailcontent_plus_BDI,mailcontent_minus_BDI = mail_content(df_BDIBCI,'BDIBCI')

mail_output = pd.concat([mailcontent_plus_SCFI,mailcontent_minus_SCFI
                       ,mailcontent_plus_BDI,mailcontent_minus_BDI])

send_mail('航運指數皆正常','航運指數異常',mail_output)

