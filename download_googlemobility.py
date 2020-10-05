# 把想要的國家拿出來另存新檔
import requests
import pandas as pd
import platform
import os
req = requests.get('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv')
url_content = req.content
csv_file = open('Global_Mobility_Report.csv', 'wb')

csv_file.write(url_content)
csv_file.close()
country_list = ['US','JP','IT','ES','CA','DE','GB','FR','BR','IN','TW','RU']

df = pd.read_csv("Global_Mobility_Report.csv", encoding="utf-8", index_col=False)
# sub_rigion_1 就是國家後面跟的子區域，這裡我們只要國家的資訊所以只拿 sub_region_1 是 Nan的列
df = df[df['sub_region_1'].isnull()].reset_index(drop=True)
df = df[df['metro_area'].isnull()].reset_index(drop=True)

datatemp = pd.DataFrame()
# data_dic = {}
for country in country_list:
    df_country = df[df['country_region_code'] == country]
    # print(df_country)
    datatemp = pd.concat([datatemp, df_country])

datatemp.rename(columns={"date": "X_axis",
                         "retail_and_recreation_percent_change_from_baseline": "retail_and_recreation",
                         "grocery_and_pharmacy_percent_change_from_baseline": "grocery_and_pharmacy",
                         "parks_percent_change_from_baseline": "parks",
                         "transit_stations_percent_change_from_baseline":"transit_stations",
                         "workplaces_percent_change_from_baseline":"workplaces",
                         "residential_percent_change_from_baseline":"residential"
                         }, inplace=True)

if platform.system() == "Windows":
    # Local 端
    path = 'static/data/Global_Mobility_Report.csv'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/Global_Mobility_Report.csv"
datatemp.to_csv(path,encoding='utf_8_sig', index=False)
os.remove("Global_Mobility_Report.csv")
print('done')