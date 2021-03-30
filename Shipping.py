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
from lxml import etree
# ----------  爬取 主幹航線準班率  ----------
# 顯卡網址
website = f"https://www.sse.net.cn/index/singleIndex?indexType=gcspi"
source = requests.get(website).text
soup = Bt4(source, "lxml")

form = soup.find_all('tbody')

upper_form = form[0].find_all('td')

man_index = [] # 主幹航線準班率
for num in range(4,11,3):
    man_index.append(float(upper_form[num].get_text()))

lower_form = form[1].find_all('td')

arrive_harbor = [] #到離港服務準班率
logistic = [] #收發或服務準班率
#從第8個開始到58個 step:5
for num in range(8,58,5):
    arrive_harbor.append(float(lower_form[num].get_text()))
for num in range(10,60,5):
    logistic.append(float(lower_form[num].get_text()))

col1 = ['綜合準班率指數(%)',
'到離港服務準班率指數(%)',
'收发貨服務準班率指數(%)']
col2 = ['亞洲-歐洲',
'亞洲-地中海-到',
'亞洲-美西-到',
'亞洲-美東-到',
'亞洲-波斯灣-到',
'亞洲-澳新-到',
'亞洲-西非-到',
'亞洲-南非-到',
'亞洲-南美-到',
'歐洲-美東-到']
col3 = ['亞洲-歐洲-收',
'亞洲-地中海-收',
'亞洲-美西-收',
'亞洲-美東-收',
'亞洲-波斯灣-收',
'亞洲-澳新-收',
'亞洲-西非-收',
'亞洲-南非-收',
'亞洲-南美-收',
'歐洲-美東-收']

main_index = pd.DataFrame({0:man_index})
main_index = main_index.T
main_index.columns = col1
arrive_harbor = pd.DataFrame({0:arrive_harbor})
arrive_harbor = arrive_harbor.T
arrive_harbor.columns = col2
logistic = pd.DataFrame({0:logistic})
logistic = logistic.T
logistic.columns = col3

time = soup.find_all("div", {"class": "title2"})[0].get_text()[0:7]
date = pd.DataFrame({'日期':[time]})

result = pd.concat([date,main_index,arrive_harbor,logistic],axis = 1)

output_direct = 'Shipping/'
output_filename = 'shipment1'
# 依照作業系統決定輸出的檔案位置
if platform.system() == "Windows":
    # Local 端
    path = 'static/data/'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/"
    
# 將新舊的資料合併
old_data = pd.read_csv(path + output_direct +output_filename +'.csv',encoding='utf_8_sig')
save_data = pd.concat([old_data,result])
# 如果資料沒有更新就移除
save_data.drop_duplicates(inplace = True)
result.to_csv(path + output_direct +output_filename +'.csv',index = False,encoding='utf_8_sig')


# ----------  爬取 港口班輪班率  ----------

website = f"https://www.sse.net.cn/index/singleIndex?indexType=gcspi_port"
source = requests.get(website).text
soup = Bt4(source, "lxml")

form = soup.find_all('script')[1].getText()
# 把字串先做些前處理 把\' 換成 空的
form = form.replace('\'',"")

# 這裡把數字抓下來
# 抓下來會是一個tupo 第一個為 row的index 第二個為資料
# row[0]:港口名字, row[1]:本期準班率, row[3]:本期靠掛數, row[7]:在泊時間,row[8]:在港時間
#需注意的是抓下來的數字第6個index的倍數是隱藏的資訊沒有放在網頁上
search_rule = re.compile(r'''
row\[(\d)\]\= # row[數字]=
([^0-9.]+|[0-9.-]+);
''',re.VERBOSE)

all_data = search_rule.findall(form)

result = []
d = {}
for i in range(1,len(all_data)):
    if (all_data[i-1][0] == '0'):
        d['港口'] = all_data[i-1][1]
        
    elif (all_data[i-1][0] == '1'):
        d['本期準班率'] = all_data[i-1][1]

    elif (all_data[i-1][0] == '3'):
        d['本期靠掛數'] = all_data[i-1][1]

    elif (all_data[i-1][0] == '7'):
        d['在泊時間'] = all_data[i-1][1]

    elif (all_data[i-1][0] == '8'):
        d['在港時間'] = all_data[i-1][1]
#     迴圈每走9次就append一次 在index = 0的時候不算
    if (i%9) == 0:
        result.append(d)
        d = {}

table = pd.DataFrame(result)
# 只要幾個港口
# table[上海纽约长滩  洛杉矶 奥克兰（美国） 鹿特丹 安特卫普
# 只要幾個港口
table = table[(table['港口'] == '上海') | (table['港口'] == '纽约') | (table['港口'] == '长滩') |
      (table['港口'] == '洛杉矶') | (table['港口'] == '奥克兰（美国）') | (table['港口'] == '鹿特丹') | 
      (table['港口'] == '安特卫普')]
# table
table.index = table['港口']
table.drop(columns = '港口')

# 拿到資料的時間
time = soup.find_all("div", {"class": "title2"})[0].get_text()[0:7]
date = pd.DataFrame({'日期':[time]})

result = pd.DataFrame()
# 不知道為什麼已經把 港口drop掉了column還是會有港口 所以這裡我單獨拿出來處理
columnlist = ['本期準班率','本期靠掛數','在港時間','在泊時間']


# 本期靠掛數
for column in columnlist:
    temp = table.loc[:,[column,'港口']]
    temp = temp[[column]]
    temp = temp.T
    # 把 coulmnlist 前四個字加到
    temp.columns = [i + column[0:4] for i in temp.columns]
    temp.index = [time]
    result = pd.concat([result,temp],axis = 1)
    
# 把index改成 0 才能將 df 等下跟時間合併 
result.index = [0]
result = pd.concat([date,result],axis = 1)

output_direct = 'Shipping/'
output_filename = 'shipment2'

    
# 將新舊的資料合併
old_data = pd.read_csv(path + output_direct +output_filename +'.csv',encoding='utf_8_sig')
save_data = pd.concat([old_data,result])
# 如果資料沒有更新就移除
save_data.drop_duplicates(inplace = True)
result.to_csv(path + output_direct +output_filename +'.csv',index = False,encoding='utf_8_sig')

# ----------  爬取 主幹航線準班率  ----------

url = "https://container-xchange.com/features/cax/"
res = requests.get(url)
page = etree.HTML(res.text)
# td 標籤裡面 style 的屬性是空的
tem = page.xpath('//td[@style=""]')

# 最後一列的數據會是 column name把他扣掉
n = int(len(tem)/6)-1

#每六個資訊存到dataframe裡, 直接用 [[1,2,3,4,5,6,],[1,2,3,4,5,6]....] 包數據
df = pd.DataFrame( [ [tem[i*6+j].text for j in range(6)] for i in range(n) ] )
colname = ['WEEK', 'LOCATION', 'EQ TYPE', '2019', '2020', '2021']
df.columns = colname
# 把所有的逗點換成小數點
df = df.apply(lambda x:x.str.replace(',','.'))

result = df[(df['LOCATION']=='SHANGHAI') | (df['LOCATION']=='LOS ANGELES')]

output_direct = 'Shipping/'
output_filename = 'Shippingdata'


result.to_csv(path + output_filename +'.csv',index = False,encoding='utf_8_sig')

# 打包所有檔案到zip
shutil.make_archive( path +'/zipfile/'+output_filename, 'zip', path + output_direct)