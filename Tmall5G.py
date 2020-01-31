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

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "list.tmall.com",
    "Cookie": "cna=zhUfFklCJnICAT3YSknK5icd; _med=dw:1536&dh:864&pw:1728&ph:972&ist:0; t=79d6fb89a0ae72213838fe10d5e0da8f; _tb_token_=a1bee7e361e0; cookie2=176a86413a3c9c0cbc41d95280356db5; dnk=lay9412206; tracknick=lay9412206; lid=lay9412206; lgc=lay9412206; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=210517; x=__ll%3D-1%26_ato%3D0; _uab_collina=157084999806509442489467; hng=TW%7Czh-TW%7CTWD%7C158; enc=QPrXIalV%2FsbEiSGLrm3aO9uA9ZOnX5y3lkx5fphRS%2BS6IvlEsEY2T4m4ntQspA%2Fvwo5jhFPEIvHN3DasXFvrxg%3D%3D; whl=-1%260%260%260; _fbp=fb.1.1571124426952.1840870754; _m_h5_tk=59f14bec0cb3ef4d5dd4071ecdcff03c_1571291926047; _m_h5_tk_enc=09d56624359b802d0b2313738f7cf7ce; res=scroll%3A1215*1782-client%3A1215*578-offset%3A1215*1782-screen%3A1536*864; uc1=cookie14=UoTbnKCr47rp6w%3D%3D&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&tag=8&cookie21=W5iHLLyFfoaZ&pas=0&existShop=false&lng=zh_CN&cookie15=UtASsssmOIJ0bQ%3D%3D; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dByuDtxkcz3MaUS7w%3D&id2=UUphy%2FA7bLfhK2tpIw%3D%3D&nk2=D8L11Gtav7Mfdw%3D%3D; _l_g_=Ug%3D%3D; uc4=nk4=0%40DeF1P2922TLBbtywEbqxJxpBFtQ9&id4=0%40U2grEJfOjhrzTBMkSZEdu%2FOj0OKfDh6X; unb=2201224705506; cookie1=B0f3xdYsfwH%2FP7qmTrJDVvgwSXKhKY99qALrSeXklYM%3D; login=true; cookie17=UUphy%2FA7bLfhK2tpIw%3D%3D; _nk_=lay9412206; sg=666; csg=091e06d3; tt=login.tmall.com; pnm_cku822=098%23E1hvK9vUvbpvUpCkvvvvvjiPRszW0jtjRFsyQjnEPmPp1jtWn2spljDnPFMZtjrPR9GCvvpvvvvvvphvC9v9vvCvpvyCvhQvSLGvCsfW0RoQRqwiLO2vqU0QKoZH1nFIAfUTnZJt98c6%2Bull8PmxfwmKHA1EKXzBIX%2FXahNWTR2pVBO0747B9Wma%2BoHoDO2hzC6tkphvC99vvOCzp8yCvv9vvUm05m5AnqyCvm9vvvvvphvvvvvvvKXvpv9Evvv2vhCv2UhvvvWvphvWgvvvvQCvpvs9RphvCvvvvvm5vpvhvvmv99%3D%3D; cq=ccp%3D0; l=dBg5pR8cq4ywvbT2BOCwquIJE579_IRY6uPRwLSvi_5aG18saQ7OkG1nAeJ6DfWfTIYB4NSLztv9-etkZU9UIe60ll2zUxDc.; isg=BMPDPmrJmoOnXFbDqMz0XAPBUoetkIUFVtr-LvWgDiKZtOPWfQqJyuAmKwxfS69y",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    "reffer": "https://login.tmall.com/?spm=a220m.1000862.a2226mz.2.521077cfFKkpDM&redirectURL=https%3A%2F%2Flist.tmall.com%2Fsearch_shopitem.htm%3Fuser_id%3D883737303%26q%3Dnex3%26sort%3Dtd",
}

# 這個函式所有商品都可以用
# 回傳的東西是 (售價，售量)
def get_the_dealinfo(htmlscript):
    try:
        # 拿到售價
        # 雖然select出來裡面只有一個東西但因為出來是一個list，要把它拿來用還是要加[0]把內容取出來
        # find(text=True, recursive=False) 這個用法會只抓標籤最外層的東西，標籤裡面就不拿了
        #
        deal_price = int(
            float(
                htmlscript.parent.parent.select(".productPrice")[0]
                .find("em")
                .find(text=True, recursive=False)
            )
        )
        # 拿到 銷售量
        get_dealnumber_with_chinese = (
            htmlscript.parent.parent.select(".productStatus")[0].find("em").text
        )
        # 處理中文
        # 如果拿到的字理面有萬，把後面"萬"去掉並乘上10000
        if re.search("萬", get_dealnumber_with_chinese):
            deal_number = int(float(get_dealnumber_with_chinese[:-1]) * 10000)
        # 其餘狀況直接轉int
        else:
            deal_number = int(get_dealnumber_with_chinese)

        return deal_price, deal_number

    # 如果搜尋的頁面找不到對應的商家
    except:
        return 0, 0


# 轉換中文到網址的格式
def chinese_to_url(chinese):
    url = urllib.parse.quote(chinese)
    return url


# 試看看有沒有ban掉
# sort = d 放在gcp上面會被ban掉
# 試看看能不能放在GCP
url = "https://list.tmall.com/search_shopitem.htm?user_id=883737303&q=nex3&sort=td"
source = requests.get(url, headers=headers).text
soup = Bt4(source, "html.parser")
ban_by_Tmall = soup.find("p").text

# 如果IP被Tmall ban掉的話
if "二正忙" in ban_by_Tmall:
    print("目前被ban了")

else:
    time.sleep(random.randint(1, 3))

    # 店家的部分想要改成使用 user_id=883737303 的方式來把 商家的名字 去做對應
    # key:user_id , value:商家名字
    shop_official = {
        "883737303": "Vivo官方旗艦店",
        "2838892713": "華為官方旗艦店",
        "1714128138": "小米官方旗艦店",
        "901409638": "Oppo官方旗艦店",
        "370627083": "三星官方旗艦店",
    }
    shop_dealer = {"2616970884": "蘇寧易購官方旗艦店", "268451883": "三際數碼官方旗艦店"}
    shop_dealer_list = ["蘇寧易購官方旗艦店", "三際數碼官方旗艦店"]

    # 合併兩個 dictionary
    shop_all = {**shop_official, **shop_dealer}

    # shop_all_R 把 key跟value對調
    #     {'Vivo官方旗艦店': '883737303',
    #  '華為官方旗艦店': '2838892713',...
    shop_all_R = {value: key for key, value in shop_all.items()}

    # 搜尋p30 = 搜尋p30+pro
    product_of_url = {
        "小米9": chinese_to_url("小米9"),
        "Opporeno": "oppo+reno",
        "Vivo-Nex3": "vivo+nex3",
        "Vivo-Nex3-5G": "nex3",
        "Vivo-X27": "vivo+X27",
        "華為-P30": "p30",
        "華為-Mate30": "mate30",
        "華為-Mate30Pro": "mate30",
        "三星-Note10": "note10",
        "三星-Note10-5G": "note10",
    }

    #     '小米9':'小米官方旗艦店'
    shop_product_id = {
        "Vivo官方旗艦店": {
            "Vivo-Nex3-5G": "601903805660",
            "Vivo-Nex3": "601717764536"
            #                  ,'Vivo-X27':'590812353617'
        },
        "華為官方旗艦店": {
            #         '華為-P30':'','華為-P30Pro':'',
            "華為-Mate30": "602918373522",
            "華為-Mate30Pro": "603330883901"
            #              ,'華為-Mate30-5G':'','華為-Mate30Pro-5G':''
        },
        #     '小米官方旗艦店':['小米9':'','小米9-5G':''],
        #     'Oppo官方旗艦店':['Oppo-Reno':''],
        "三星官方旗艦店": {
            "三星-Note10": "600469192419",
            "三星-Note10-5G": "601093283698"
            #                ,'Note10plus':'','Note10plus-5G':''
        },
        "蘇寧易購官方旗艦店": {
            "Vivo-Nex3-5G": "600891657529",
            "Vivo-Nex3": "602577338304"
            #                  ,'Vivo-X27':'',
            ,
            "華為-Mate30": "600662536849",
            "三星-Note10": "600453072145",
            "三星-Note10-5G": "600453936466",
        },
        "三際數碼官方旗艦店": {
            "華為-Mate30": "603187202582",
            "華為-Mate30Pro": "602973425447",
            "三星-Note10": "600932362045",
            "三星-Note10-5G": "600933006447",
        },
    }

    # 把非官方的網站跟官方的網站合起來,這裡 sum(欲合併的陣列,[])會把所有的陣列攤平合在一起,並做 flatten array
    #     products_of_shops 的 key 是所有的產品
    #     products_of_shops 的 value 是所有產品相關的店家
    # 這裡稍微注意華為官方網站 的商品有兩個

    shop_id = {}
    for shop_item in shop_product_id.keys():  # countries.keys 是全部的型號
        shop_id[shop_item] = [v for v in shop_product_id[shop_item].values()]

    product_id = {}
    for product_item in shop_product_id.values():
        for product in product_item.keys():
            product_id.setdefault(product, [])  # added key
            product_id[product] += [product_item[product]]

    # 把url都印出來
    # for shop in shop_product_id.keys():
    #     for product in shop_product_id[shop].keys():
    #         url = f'https://list.tmall.com/search_shopitem.htm?user_id={shop_all_R[shop]}&start_price=1000&q={product_of_url[product]}&sort=td&style=w'
    #         print(url)

    res = []
    d = {}
    # 迴圈跑每個產品
    # product:'mate30','nex30'...
    for shop in shop_product_id.keys():
        for product in shop_product_id[shop].keys():

            # .\可以讓過長的字串換行
            url = f"https://list.tmall.com/search_shopitem.htm?user_id={shop_all_R[shop]}\
                &start_price=1000&q={product_of_url[product]}&sort=td&style=w"
            sessions = requests.session()
            sessions.headers = headers
            source = sessions.get(url, allow_redirects=False).text
            # source = requests.get(url, headers=headers).text
            soup = Bt4(source, "html.parser")

            # search_id 是一個正則表示 要拿去對 html 搜尋 <a>標籤裡的 href 有沒有符合的
            search_id = re.compile(shop_product_id[shop][product])
            deal_price, deal_number = get_the_dealinfo(soup.find("a", href=search_id))

            d["Product"] = product
            d["Shopname"] = shop
            d["Dealprice"] = deal_price
            d["Dealnumber"] = deal_number
            d["Timestamp"] = datetime.datetime.today().strftime("%Y-%m-%d")
            res.append(d)
            print(d)

            d = {}
            #         等一會再跑下一圈
            time.sleep(random.randint(1, 3))

    if platform.system() == "Windows":
        # Local 端
        path = "static/data/Tmall5g.csv"
    else:
        # AWS 端
        path = "/home/cathaylife04/smartphone/iphone11/static/data/Tmall5g.csv"

    Data = pd.read_csv(path)
    Old_Data = Data.to_dict("records")
    newres = res + Old_Data
    df = pd.DataFrame(newres)
    df = df.drop_duplicates()
    df.to_csv(path, encoding="utf_8_sig", index=False)
    print("執行完畢")
