import requests
import json
import datetime
import pandas as pd
import platform
import shutil


#-------------------------------------------Nike 鞋子-------------------------------------------------
# 每頁我有幾個Item 測試過後應該48是極限
itemperpage = 48
newdata = {}
# 對這個url 下request 只是為了拿總共有多少頁的產品 這個url是衣服的
url_shoe = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&'\
    'country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684)'\
    '%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
    '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
# 每頁我有幾個Item 測試過後應該48是極限
itemperpage = 48
r = requests.get(url_shoe)
response = json.loads(r.text)

# 拿到 totalPage
totalPages = response['data']['products']['pages']['totalPages']
# 總共有多少產品
totalResources = response['data']['products']['pages']['totalResources']
print('totalPages:',totalPages,'totalResources',totalResources)

colorways_list = []
currentprice = []
fullprice = []
discount = []



for page_num in range(totalPages):
    url_shoe = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&'\
    'country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
    '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C5b21a62a-0503-400c-8336-3ccfbff2a684)'\
    '%26anchor%3D'+str(page_num)+'%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
    '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    r = requests.get(url_shoe)
    response = json.loads(r.text)
    # price = response['data']['products']['products'][0]['colorways'][0]['price']['currentPrice']
    # 迴圈loop  每個頁面總共有 item perpage個商品
    for item_count in range(itemperpage):
        # 確認每個主商品底下有幾個商品
        try:
            colorways_count = len(response['data']['products']['products'][item_count]['colorways'])
            for count in range(colorways_count):
                currentprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['currentPrice'])
                fullprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['fullPrice'])
        except:
            print('colorways exception')
            
newdata['discountrate_shoe'] = round(sum(currentprice)/sum(fullprice)*100,2)
newdata['totalResources_shoe'] = totalResources
print('discountrate_shoe:',newdata['discountrate_shoe'],'totalResources_shoe',newdata['totalResources_shoe'])

#------------------------------------------- Nike cloth -------------------------------------------------
# 每頁我有幾個Item 測試過後應該48是極限
itemperpage = 48

url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&'\
        'country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
        '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(a00f0bb2-648b-4853-9559-4cd943b7d6c6%2C5b21a62a-0503-400c-8336-3ccfbff2a684)'\
        '%26anchor%3D0%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
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
    url_cloth = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&'\
        'country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
        '%26filter%3DemployeePrice(true)%26filter%3DattributeIds(a00f0bb2-648b-4853-9559-4cd943b7d6c6%2C5b21a62a-0503-400c-8336-3ccfbff2a684)'\
        '%26anchor%3D'+str(page_num)+'%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
        '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    r = requests.get(url_cloth)
    response = json.loads(r.text)
    # price = response['data']['products']['products'][0]['colorways'][0]['price']['currentPrice']
    # 迴圈loop  每個頁面總共有 item perpage個商品
    for item_count in range(itemperpage):
        # 計算產品數量
        total_item_product += 1
        # 確認每個主商品底下有幾個商品

        try:
            colorways_count = len(response['data']['products']['products'][item_count]['colorways'])
            for count in range(colorways_count):
                currentprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['currentPrice'])
                fullprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['fullPrice'])
        except:
            print('colorways exception')

newdata['discountrate_cloth'] = round(sum(currentprice)/sum(fullprice)*100,2)
newdata['totalResources_cloth'] = totalResources
print('discountrate_cloth:',newdata['discountrate_cloth'],'totalResources_cloth',newdata['totalResources_cloth'])


newdata['timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")

# --------------------------------------- 準備新舊資料合併
if platform.system() == "Windows":
    # Local 端
    path = 'static/data/Sports/nike.csv'
else:
    # AWS 端
    path = "/home/cathaylife04/smartphone/iphone11/static/data/Sports/nike.csv"

# Read Old Data 
Data = pd.read_csv(path)
Old_Data = Data.to_dict('records')

newdata = [newdata]
newdata = newdata + Old_Data

df = pd.DataFrame(newdata)
# drop 重複的某個欄位資訊
# https://stackoverflow.com/questions/12497402/python-pandas-remove-duplicates-by-columns-a-keeping-the-row-with-the-highest
df = df.drop_duplicates(subset='timestamp', keep="last")
# Pivot value:欲處理的資訊(相加 取平均 等等等)
#index:列向量
#columns:行向量
# path
df.to_csv(path,encoding='utf_8_sig', index=False)