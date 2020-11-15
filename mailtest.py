import pandas as pd
from datetime import datetime,date,timedelta
data = pd.read_csv('static/data/Data.csv')

# 要篩出來的國家及產品
data = data[data['Country'].isin(['Us','Jp','Cn','De','Fr'])]
data = data[data['Product'].isin(['iPhone 12 Pro Max','iPhone 12 Pro','iPhone 12','iPhone 12 mini'])]
data = data[data['Colors'].isin(['Silver'])]
data = data[data['Size'].isin(['128GB','256GB'])]


today = date.today() - timedelta(days=0)
last_week = date.today() - timedelta(days=7)
df_today = data[data['TimeStemp'] == today.strftime("%Y-%m-%d")]
df_last_week = data[data['TimeStemp'] == last_week.strftime("%Y-%m-%d")]
 
new = pd.concat([df_today , df_last_week])

# 把所有上週日期的Timestemp 都換成 今天日期
new_changedate = new.replace({'TimeStemp':last_week.strftime("%Y-%m-%d")},today.strftime("%Y-%m-%d"))
# 把所有重複的資料都丟掉
new_changedate.drop_duplicates(keep = False,inplace=True)


# 把修改的時間 利用index不變的狀態 將原本的時間套回來
new_changedate['TimeStemp'] = new['TimeStemp']
# 因為在python 的判斷式裡我們如果想要去比對 nan==nan 他總是給我們false 所以這裡我們把nan用0取代 0=0 會給True
new_changedate.fillna(0,inplace = True)
# new_changedate.to_csv('test.csv',encoding='utf_8_sig', index=False)


new_changedate_dict = new_changedate.to_dict(orient = 'record')
tot_index = [ i for i in range(int(len(new_changedate_dict)))]
middle_index = int(len(tot_index)/2)
# middle_index = 45
back_index = tot_index[middle_index:]
front_index = tot_index[:middle_index]

text = []
table = []
res = {}
key_to_be_deleted = ['Celluar','TimeStemp']

#掃前半段資料(日期是新的)將資訊先暫時存到 temp 字典裡
for i in front_index:
    temp = {}
    temp['Country'] = new_changedate_dict[i]['Country']
    temp['Product'] = new_changedate_dict[i]['Product']
    temp['Celluar'] = new_changedate_dict[i]['Celluar']
    temp['Size'] = new_changedate_dict[i]['Size']
    temp['Colors'] = new_changedate_dict[i]['Colors']
    temp['TimeStemp'] = new_changedate_dict[i]['TimeStemp']
    temp['Today'] = new_changedate_dict[i]['Deliver']

    #掃後半段資料(日期是舊的) 找到 [日期不同] 但 [其他欄位都一樣] 的產品
    for j in back_index:
        if (new_changedate_dict[j]['Country'] == temp['Country']
        and new_changedate_dict[j]['Product'] == temp['Product']
        and new_changedate_dict[j]['Celluar'] == temp['Celluar']
        and new_changedate_dict[j]['Size'] == temp['Size']
        and new_changedate_dict[j]['Colors'] == temp['Colors']
        and new_changedate_dict[j]['TimeStemp'] != temp['TimeStemp']) :

            # 記錄下來這個欄位上一個週一的運送日期內容        
            temp['Last Monday'] = new_changedate_dict[j]['Deliver']
            
            # 刪除我們不想要的key
            for key in key_to_be_deleted:
                del temp[key]
            table.append(temp)
            break


# 刪除同樣的字典 有很多產品的運送日期變化都一樣但細項不一樣 這樣資訊太多我們留下一個就好讓使用者自己去看什麼改變了
# 所以這裡我們把她都刪掉
# ex:iPhone12,Us,128G,5-6Week ; iPhone12,Us,256G,5-6Week
#用tuple包dictionary.items() 就可以進行 illiterate
table2 = [dict(t) for t in {tuple(d.items()) for d in table}]

table = pd.DataFrame(table2)
table = table[['Country','Product','Size','Colors','Last Monday','Today']]
table = table.sort_values(by=['Country'])
sorter = ['Us','Cn','Jp','De','Fr']
table['Country'] = table['Country'].astype("category")
table['Country'].cat.set_categories(sorter, inplace=True)

All_countries = {
        "Us": "美國",
        "Cn": "中國",
        "Jp": "日本",
        "Hk": "香港",
        "Uk": "英國",
        "De": "德國",
        "Ru": "俄羅斯",
        "Fr": "法國",
        "Tw": "台灣",
        "Br": "巴西",
        "Mx": "墨西哥",
}
table['Country'] = table['Country'].map(All_countries)
# sorter = ['iPhone 12 Pro','iPhone 12','iPhone 12 mini']
# table['Size'] = table['Size'].astype("category")
# table['Size'].cat.set_categories(sorter, inplace=True)

# table = table.sort_values(['Country'])
table.sort_values(['Country','Product','Size'], ascending=[True,False, True], inplace=True)

# Send Email
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
passwd = 'Lay9821529'
msg['To'] = 'jalinyang@cathaylife.com.tw;patrickyen@cathaylife.com.tw;'\
'ericfly168@cathaylife.com.tw;renny@cathaylife.com.tw;kcyu@cathaylife.com.tw;'\
'aywlang@cathaylife.com.tw;wthuang@cathaylife.com.tw;evanyeh@cathaylife.com.tw;'\
'jianyou@cathaylife.com.tw;sylviayang@cathaylife.com.tw;cw_huang@cathaylife.com.tw;'\
'boyu.chen@cathaylife.com.tw;layx@cathaylife.com.tw;liuziwei@cathaylife.com.tw;'\
'yitsung@cathaylife.com.tw;joelin@cathaylife.com.tw;yaojih@cathaylife.com.tw;yung666666@cathaylife.com.tw;'\
'layx@cathaylife.com.tw;lay9412206@gmail.com'

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
to = msg['TO'].split(";")
msg['subject'] = "iPhone最新產品運期異動更新(上週一 至 本週一)"

# body = table.to_html(classes="table table-striped table-hover",index=False)

body = build_table(table, 'blue_light')
msg.attach(MIMEText(body, 'html'))

s = smtplib.SMTP('cathaymail.linyuan.com.tw', 25)
s.starttls()
s.login(msg['From'], passwd)

context = msg.as_string()


s.sendmail(msg['From'], to, context)
print( 'successfully sent  email')
s.close()