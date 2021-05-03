import requests
import json
import datetime
import pandas as pd
import platform
import shutil


#-------------------------------------------Nike 鞋子-------------------------------------------------
# 每頁我有幾個Item 測試過後應該48是極限
itemperpage = 48

url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&country=us'\
'&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c)'\
    '%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
   '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'



r = requests.get(url_cloth)
response = json.loads(r.text)

# 拿到 totalPage
totalPages = response['data']['products']['pages']['totalPages']
totalResources = response['data']['products']['pages']['totalResources']
print('totalPages:',totalPages,'totalResources',totalResources)
colorways_list = []
currentprice = []
fullprice = []
discount = []
newdata = {}
total_item_product = 0
for page_num in range(totalPages):
    url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&country=us'\
    '&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c)'\
    '%26anchor%3D'+str(page_num)+'%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
   '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    r = requests.get(url_cloth)
    response = json.loads(r.text)

    # 迴圈loop  每個頁面總共有 item perpage個商品
    for item_count in range(itemperpage):
        # 計算產品數量
        # 確認每個主商品底下有幾個商品

        try:
            colorways_count = len(response['data']['products']['products'][item_count]['colorways'])
            for count in range(colorways_count):
                if response['data']['products']['products'][item_count]['colorways'][count]['price']['discounted'] == True:
                    currentprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['currentPrice'])
                    fullprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['fullPrice'])
                total_item_product += 1
        except:
            print('colorways exception')
            
print('鞋子打折的item數量:',len(currentprice),'鞋子打折的item數量:',len(fullprice))
newdata['discount_item_ratio_shoes'] = round(len(currentprice)/total_item_product*100,2)
newdata['discount_money_shoes'] = round(sum(currentprice)/sum(fullprice)*100,2)

print('有打折的數量占比',newdata['discount_item_ratio_shoes'],'折扣平均',newdata['discount_money_shoes'])

#------------------------------------------- Nike cloth -------------------------------------------------
url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&country=us'\
'&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(a00f0bb2-648b-4853-9559-4cd943b7d6c6)'\
    '%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
    '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'

r = requests.get(url_cloth)
response = json.loads(r.text)

# 拿到 totalPage
totalPages = response['data']['products']['pages']['totalPages']
totalResources = response['data']['products']['pages']['totalResources']
print('totalPages:',totalPages,'totalResources',totalResources)
colorways_list = []
currentprice = []
fullprice = []
discount = []

total_item_product = 0
for page_num in range(totalPages):
    url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&country=us'\
    '&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c)'\
    '%26anchor%3D'+str(page_num)+'%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
   '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    r = requests.get(url_cloth)
    response = json.loads(r.text)

    # 迴圈loop  每個頁面總共有 item perpage個商品
    for item_count in range(itemperpage):
        # 計算產品數量
        # 確認每個主商品底下有幾個商品

        try:
            colorways_count = len(response['data']['products']['products'][item_count]['colorways'])
            for count in range(colorways_count):
                if response['data']['products']['products'][item_count]['colorways'][count]['price']['discounted'] == True:
                    currentprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['currentPrice'])
                    fullprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['fullPrice'])
                total_item_product += 1
        except:
            print('colorways exception')
print('衣服打折的item數量:',len(currentprice),'衣服打折的item數量:',len(fullprice))
newdata['discount_item_ratio_clothes'] = round(len(currentprice)/total_item_product*100,2)
newdata['discount_money_clothes'] = round(sum(currentprice)/sum(fullprice)*100,2)

print('有打折的數量占比',newdata['discount_item_ratio_clothes'],'折扣平均',newdata['discount_money_clothes'])

# 加上時間戳記
newdata['timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")

# --------------------------------------- 準備新舊資料合併
if platform.system() == "Windows":
    # Local 端
    path = 'static/data/Sports/nike.csv'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/Sports/nike.csv"

newdata = [newdata]
# Read Old Data 
try:
    # 如果沒有Data
    Data = pd.read_csv(path)
    Old_Data = Data.to_dict('records')
    newdata = newdata + Old_Data
except:
    print('no old data')

df = pd.DataFrame(newdata)
# drop 重複的某個欄位資訊
# https://stackoverflow.com/questions/12497402/python-pandas-remove-duplicates-by-columns-a-keeping-the-row-with-the-highest
df = df.drop_duplicates(subset='timestamp', keep="last")
# Pivot value:欲處理的資訊(相加 取平均 等等等)
#index:列向量
#columns:行向量
# path
df.to_csv(path,encoding='utf_8_sig', index=False)