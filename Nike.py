import requests
import json
import datetime
import pandas as pd
import platform
import shutil
import datetime

itemperpage = 48

# --------------------------------------- 
# url 產生函數, 參數(ID,從第幾個產品開始,每一次querry拿幾個產品)
# url 產生函數, 參數(ID,從第幾個產品開始,每一次querry拿幾個產品)
def get_url(ID:str,pruduct_start:int,querry_each_num:int):
    url = f'https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=SmrGtQORwBasB6-53jE61&country=us'\
                '&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)'\
                f'%26filter%3DemployeePrice(true)%26filter%3DattributeIds('+ID+')'\
                f'%26anchor%3D{pruduct_start}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D'+str(itemperpage)+'&language=en'\
                '&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    return(url)

# 爬蟲函數, 引數(產品名稱 )
def craw_data(product: str) -> dict:
    shoes_ID = '16633190-45e5-4830-a068-232ac7aea82c'
    cloth_ID = 'a00f0bb2-648b-4853-9559-4cd943b7d6c6'
    
    if product == 'shoes':
        product_ID = shoes_ID

    else:
        product_ID = cloth_ID
        
    url = get_url(product_ID,24,itemperpage)    
    r = requests.get(url)
    response = json.loads(r.text)

    # 拿到 totalPage
    totalPages = response['data']['products']['pages']['totalPages']
    totalResources = response['data']['products']['pages']['totalResources']
    print('totalPages:',totalPages,'totalResources',totalResources)

    currentprice = []
    fullprice = []
    discount = []
    newdata = {}
    discount_item_num = 0
    instock_num = 0
    soldout_num = 0
    total_item_product = 0
    for page_num in range(totalPages):
        url = get_url(product_ID, page_num, itemperpage)

        r = requests.get(url)
        response = json.loads(r.text)

        # 迴圈loop  每個頁面總共有 item perpage個商品
        for item_count in range(itemperpage):
            # 計算產品數量
            # 確認每個主商品底下有幾個商品

            try:
                # 每個產品下有幾種顏色
                colorways_count = len(response['data']['products']['products'][item_count]['colorways'])
                for count in range(colorways_count):
                    # 先判斷有沒有庫存 如果有庫存的話
                    if response['data']['products']['products'][item_count]['colorways'][count]['inStock'] == True:
                        instock_num += 1

                        if response['data']['products']['products'][item_count]['colorways'][count]['price']['discounted'] == True:
                            discount_item_num += 1

                            currentprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['currentPrice'])
                            fullprice.append(response['data']['products']['products'][item_count]['colorways'][count]['price']['fullPrice'])
                    # 沒有庫存的狀況下
                    else:
                        soldout_num +=1
                    total_item_product +=1
            except:
                print('colorways exception')

    newdata['discount_item_ratio_'+product] = round(discount_item_num/instock_num*100,2)
    newdata['discount_money_'+product] = round(sum(currentprice)/sum(fullprice)*100,2)
    newdata['total_num_'+product] = total_item_product
    newdata['soldout_num_'+product] = soldout_num
    newdata['instock_num_'+product] = instock_num
    newdata['discount_num_'+product] = discount_item_num
    
    print('總產品數量:',total_item_product,'完售產品數量:',soldout_num,'可購買產品數量:',instock_num,'打折產品數量:',discount_item_num)
    print('有打折的數量占比',newdata['discount_item_ratio_'+product],'折扣平均',newdata['discount_money_'+product])
    return newdata

    
newdata_shoes = craw_data('shoes')
newdata_cloth = craw_data('cloth')
# 把兩個字典進行合併
newdata = {**newdata_shoes,**newdata_cloth}
newdata['timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")

#------------------------------------------- 存檔 -------------------------------------------------

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
cols = ['timestamp','discount_item_ratio_cloth','discount_money_cloth',
        'total_num_cloth','soldout_num_cloth','instock_num_cloth',
        'discount_num_cloth','discount_item_ratio_shoes','discount_money_shoes',
        'total_num_shoes','soldout_num_shoes','instock_num_shoes','discount_num_shoes']
df = df[cols]
# drop 重複的某個欄位資訊
# https://stackoverflow.com/questions/12497402/python-pandas-remove-duplicates-by-columns-a-keeping-the-row-with-the-highest
df = df.drop_duplicates(subset='timestamp', keep="last")
# Pivot value:欲處理的資訊(相加 取平均 等等等)
#index:列向量
#columns:行向量
# path
df.to_csv(path,encoding='utf_8_sig', index=False)