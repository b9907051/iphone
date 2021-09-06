# 外部套件
import os
import pandas as pd
import numpy as np
import platform

data_name = 'SCFI'
if platform.system() == "Windows":
    # Local 端
    path = f'static/data/Shipping/{data_name}.csv'
else:
    # AWS 端
    path = f'/home/cathaylife04/smartphone/iphone11/static/data/Shipping/{data_name}.csv'
# 加入最新的資料
result = pd.read_csv(path,encoding = 'utf_8_sig')

result['date'] = pd.to_datetime(result['date'],format = '%Y-%m-%d')

#資料如果有NA就拿掉整列

result.dropna(axis='rows',how = 'any',inplace = True)

df = result
# 把 index 換成日期 並把原本日期的欄位丟掉
df.index = df['date']
# 留下字串有SCFI的表格
df = df.filter(regex='SCFI')

#----函數處理------

def fun_apply(x, targetfunction, window, **kwargs):
    # 軸向是0 就是一個一個列往下apply
    T = pd.DataFrame(
                np.apply_along_axis(targetfunction, 0, x, window = window, **kwargs )
            )
    T.index = x.index
    T.columns = x.columns
    return T

def lag(series, periods=1):
    '''
    將序列值落後一期。
    '''
    #     >> x = np.arange(10)  # x例子
    # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # >> np.roll(x, 1)  # axis为None，然后再向水平滾動2个位置
    # array([9, 0, 1, 2, 3, 4, 5, 6, 7, 8])
    series = np.roll(series, shift=periods)
    # np.roll會把最後的值捕到最前面，因此要把前面值變成nan

    series[: periods] = np.nan
    # array([Nan, 0, 1, 2, 3, 4, 5, 6, 7, 8])
    return series


#漲幅
def fun_ratio_diff(x, window = 1):
    return  x/lag(x,window)  -1
# 判斷窗格內的陣列是否滿足嚴格遞增
def fun_strict_deincrease(x, window = 2,**kwargs):
#     iterate through list like in sliding windows
    #     print(x)
    result = [False] * (window - 1)
    # 因為是從陣列的開始 loop 去往未來看 有沒有嚴格遞增例如 在1/2 看1/7 1/9 有沒有嚴格遞增，所以如果產生滿足的訊號
    # 應該是發生在未來 1/9 所以我們這裡一開始就先將結果做平移 2, (window - 1) 個False，這樣才是正確的
        # 迴圈最後不用跑完因為最後的資料沒得比
    for position in range(len(x)-window+1):
        # 每 N 個值 window = N 就拿出來算一次
        temp = x[position : position+window]
        # 假設window = 3
        # temp = [1,2,3] , zip(temp,temp[1:] )= (1,2),(2,3)
        # 這裡的 if 判斷是是來自於因為比較的數列都是 0 跟 Z score 大於門檻值的數列
        # ex: [0, 2.2, 2.3],[0,0,3] 而我們想要拿到是全部數列都大於 Z score6
        # 因為這裡我是傳 字典進來 所以取值我要去用 key 去拿
        
        # 只要Z score_threshoud 異常的話
        if all(temp > kwargs['Zscore_threshould']):
            
            if kwargs['way'] == 'strict':
                tempresult = all(i < j for i, j in zip(temp,temp[1:]))
            else:
                tempresult = True
        else:
            tempresult = False

        result.append(tempresult)

    return(result)
# 計算rolling 的 Z score
def fun_rolling_zscore(df,positive_df):
    # 第一列的值我們這邊直接拿進來因為沒辦法計算 std, 格式是Dataframe
    # positive_df 是 漲幅大於0的濾網
    progress_dataframe = df.iloc[0:1,:]
    for index in range( 1,df.shape[0]):#
        # 為了避免拿到 pd.series (在取值上面會捨去欄位) 盡量以 Dataframe 的格式tw進行運算
        # 所以這裡拿 index:index+1 就是為了保持 Dataframe的格式
        Zscore_eachrow = (df.iloc[index:index+1,:][positive_df.iloc[index:index+1,:]] - \
                        df.iloc[:index+1,:][positive_df.iloc[:index+1,:]].mean())/ \
                        df.iloc[:index+1,:][positive_df.iloc[:index+1,:]].std()

        progress_dataframe = pd.concat([progress_dataframe,Zscore_eachrow])
    return(progress_dataframe)
# Ture_false 轉換成布林值
def true_false(x,window):
    y = [bool(i) for i in x]
    return y


# 要拿來算產品的差幅的週數
window = 4
# Zscore 至少要大於多少
# Zscore_threshould = 1

#報價的漲跌幅
price_diff = fun_apply(df, fun_ratio_diff,window)
#         test = fun_ratio_diff(chemicalprice[chemicalobj],4)
# 這裡要注意 如果沒有把na 用0填滿等下在做判斷的時候就會有異常, nan 反而會滿足條件
# Zscore threshould: 小於 這個個數值就丟掉啦 都雜訊

price_diff_lagerthanzero = price_diff>0
price_diff_smallerthanzero = price_diff<0

# 沒有經過計算的 (price_diff_lagerthanzero 為 False 補 0)
Zscore_price_plus = fun_rolling_zscore(price_diff, price_diff_lagerthanzero).fillna(0)
Zscore_price_minus = fun_rolling_zscore(price_diff, price_diff_smallerthanzero).fillna(0)

# Zscore_diff.to_csv('outcome.csv',encoding='utf_8_sig')

# 如果這周漲幅有高於歷史平均才給True
signal_price_plus = Zscore_price_plus>0
signal_price_minus = Zscore_price_minus<0

# 我們只在乎前一周的資料沒有訊號 然後 本周的資料是有訊號的
# 我們只要前一周的資料是False 且最後一周是True的
Result_signal_plus = (signal_price_plus.iloc[-2,:] == False) & (signal_price_plus.iloc[-1,:] == True)
Result_signal_minus = signal_price_minus.iloc[-1,:] == False
# 符合目標 Zscore 的產品的最新報價
# chemicalprice[chemicalprice.columns[Result_signal]].iloc[-1:,:]
# 符合門檻的 產品 Zscore 並四捨五入到第一位
# Zscore_chemicalprice_diff[chemicalprice.columns[Result_signal]].iloc[-1:,:].round(1)
# mail content
mailcontent_plus = pd.concat([df[df.columns[Result_signal_plus]].iloc[-1:,:],
                        price_diff[df.columns[Result_signal_plus]].iloc[-1:,:].round(2)*100
                        ],axis = 1)
mailcontent_minus = pd.concat([df[df.columns[Result_signal_minus]].iloc[-1:,:],
                        price_diff[df.columns[Result_signal_minus]].iloc[-1:,:].round(2)*100
                        ],axis = 1)

def mail_handle(df):
    # 如果 表 不是空的話執行 (表如果只有index也是空的)
    if df.size != 0:
        df['Date'] = df.index
        df.columns = ['報價','漲跌幅','日期']
        df = df[['日期','報價','漲跌幅']]
    return df
mailcontent_plus = mail_handle(mailcontent_plus)
mailcontent_minus = mail_handle(mailcontent_minus)

# 寄信 模組
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import time
import sys
import os
import platform
from pretty_html_table import build_table

msg = MIMEMultipart()
msg['From'] = 'layx@cathaylife.com.tw'
# passwd = getpass.getpass(colors.OKGREEN + 'Password: ')
passwd = 'Lay@9412206'


#如果表都是空的
print(mailcontent_plus)
print(mailcontent_minus)
if (mailcontent_plus.empty) and (mailcontent_minus.empty):
    msg['subject'] = "SCFI 本週報價無異常 "
else:
    print('mailcontent_minus: ',mailcontent_minus)
    msg['subject'] = "SCFI 本週報價異常請見內容 "
start = f"""<html>
                <body>
                <style>

                    span {{
                        color: red;
                        font-weight:bold;
                        text-decoration:underline;
                    }}
                </style>
                <p> 本訊號上漲只有 上週 Z-score 為<span style="color: #000000;">負</span>本週Z-score為<span>正</span>才會出現 </p>
                <p> 本訊號下跌只要 本週 Z-score為<span>正</span>就會出現 </p>
                <p> 該Z-score 之計算為<span>(每週報價之月漲幅-歷史平均)/歷史標準差</span></p>

                </span>
                    </br></br></br>"""
# 在attach的部分不太知道在藂蝦小要怎麼把 plain text 跟 html 結合在一起???

#html 裡面CSS 在ID的權限是 0-1-0-0 高等級
# #bb{{color: black;}}
# id ="bb"


# 這個是一個html的範例
# <span style="font-weight:bold;text-decoration:underline;">
# 如果build_table 裡面的東西是空的會掛
try:
    body_positive = build_table(mailcontent_plus, 'blue_light')
except:
    body_positive = ""

try:
    body_negative = build_table(mailcontent_minus, 'blue_light')
except:
    body_negative = ""

end = """</body>
    </html>
    """
msg.attach(MIMEText(start + body_positive + body_negative + end, 'html'))

# 信箱
msg['To'] ='lay9412206@gmail.com;layx@cathaylife.com.tw;'\
'jalinyang@cathaylife.com.tw;patrickyen@cathaylife.com.tw;'\
'ericfly168@cathaylife.com.tw;renny@cathaylife.com.tw;kcyu@cathaylife.com.tw;'\
'aywlang@cathaylife.com.tw;wthuang@cathaylife.com.tw;evanyeh@cathaylife.com.tw;'\
'jianyou@cathaylife.com.tw;sylviayang@cathaylife.com.tw;cw_huang@cathaylife.com.tw;'\
'boyu.chen@cathaylife.com.tw;layx@cathaylife.com.tw;liuziwei@cathaylife.com.tw;'\
'yitsung@cathaylife.com.tw;joelin@cathaylife.com.tw;yaojih@cathaylife.com.tw;yung666666@cathaylife.com.tw;'

to = msg['To'].split(";")
#名單
# 楊嘉林  jalinyang@cathaylife.com.tw
# 閻志強  patrickyen@cathaylife.com.tw
# 蔡士弘  ericfly168@cathaylife.com.tw
# 王正聰  renny@cathaylife.com.tw
# 尤崑堅  kcyu@cathaylife.com.tw
# 郎遠聞  aywlang@cathaylife.com.tw
# 黃維泰  wthuang@cathaylife.com.tw
# 葉俊宏  evanyeh@cathaylife.com.tw
# 李建佑  jianyou@cathaylife.com.tw
# 楊子慧  sylviayang@cathaylife.com.tw
# 黃秋文  cw_huang@cathaylife.com.tw
# 陳柏玉  boyu.chen@cathaylife.com.tw
# 劉悌鐳  layx@cathaylife.com.tw
# 劉子瑋  liuziwei@cathaylife.com.tw
# 王怡聰  yitsung@cathaylife.com.tw
# 林士喬  joelin@cathaylife.com.tw
# 游堯日  yaojih@cathaylife.com.tw
# 楊又青  yung666666@cathaylife.com.tw
print(to)
s = smtplib.SMTP('cathaymail.linyuan.com.tw', 25)
s.starttls()
s.login(msg['From'], passwd)

context = msg.as_string()
s.sendmail(msg['From'], to, context)
print( 'successfully sent  email')
s.close()