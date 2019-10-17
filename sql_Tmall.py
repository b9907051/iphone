from bs4 import BeautifulSoup as Bt4
import requests #2.18.4
import json
import datetime
import pandas as pd
import urllib
import time
import re
import random

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'list.tmall.com',
'Cookie':'cna=zhUfFklCJnICAT3YSknK5icd; _med=dw:1536&dh:864&pw:1728&ph:972&ist:0; t=79d6fb89a0ae72213838fe10d5e0da8f; _tb_token_=a1bee7e361e0; cookie2=176a86413a3c9c0cbc41d95280356db5; _m_h5_tk=acd19319020a1144fd02a569eb3f3a8f_1570644520682; _m_h5_tk_enc=ba09262ec70187c8eb0c69c036e6ba76; dnk=lay9412206; uc1=cookie15=URm48syIIVrSKA%3D%3D&existShop=false&tag=8&pas=0&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&lng=zh_CN&cookie14=UoTbnV5vpUaYOQ%3D%3D&cookie21=U%2BGCWk%2F7oPIg; uc3=nk2=D8L11Gtav7Mfdw%3D%3D&id2=UUphy%2FA7bLfhK2tpIw%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dByuDm5RWLSqY5iII%3D; tracknick=lay9412206; lid=lay9412206; _l_g_=Ug%3D%3D; uc4=id4=0%40U2grEJfOjhrzTBMkSZEdu%2FOiPIFKfRJd&nk4=0%40DeF1P2922TLBbtywEbqwFHzdSh9S; unb=2201224705506; lgc=lay9412206; cookie1=B0f3xdYsfwH%2FP7qmTrJDVvgwSXKhKY99qALrSeXklYM%3D; login=true; cookie17=UUphy%2FA7bLfhK2tpIw%3D%3D; _nk_=lay9412206; sg=666; csg=10f75fae; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=210517; x=__ll%3D-1%26_ato%3D0; enc=0LxVaFfV%2B8bDkg%2ByNgopDbIOyLKOiD1GNPJwzG3u6Q%2BUh2cbUeiyj3gP%2BoAtOoI8dHqFkp5OQvKjPJggQoPd3A%3D%3D; pnm_cku822=098%23E1hvCvvUvbpvU9CkvvvvvjiPRssOsjl8P2sWzjYHPmPvQj1HR2Syzj3WnLLp1jDvPLZPvpvhMMGvvvhCvvOvCvvvphvEvpCWCjBxvvwQAbmxfXk4jomxfwLyd3ODN%2BLyaNpOHkyZ0nsy0COqb64B9W2%2B%2BfvsxI2hgR9t%2BFBCAfevD40Xjo2v%2B8c6e1DQpf2XS4ZAhbyCvm9vvvvvphvvvvvvvYxvpvAWvvv2vhCv2UhvvvWvphvWgvvvvQCvpvs9uphvmvvv9bf1s03NkphvC99vvOCzp2yCvvpvvvvviQhvCvvv9UU%3D; res=scroll%3A1688*1782-client%3A1688*803-offset%3A1688*1782-screen%3A1536*864; whl=-1%260%260%260; l=cBg5pR8cq4ywv3qCBOCZnurza779tIRxiuPzaNbMi_5aD18_3pbOk9WI2eJ6DfWdt9TB4tm2-g29-etksdB2Pjnqn7MV.; isg=BJ-fqJ2vPsj-ITrXbADQ8A_VLvMpBPOm4-krDjHses6VwL5COdLN9miahzgb6Mse',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
}

# 這個函式所有商品都可以用
def Get_the_dealnumber(htmlscript,shopname):

	shop_list = f'span[data-nick={shopname}]'
	find_shop_span = htmlscript.select(shop_list)

	try:
		get_dealnumber_with_chinese = find_shop_span[0].parent.find('em').text
		# 處理中文
		# 如果拿到的字理面有萬，把後面兩個字"萬筆"去掉
		if re.search("萬", get_dealnumber_with_chinese):
			find_deal_number = float(get_dealnumber_with_chinese[:-2])*10000
		# 其餘狀況把筆去掉
		else:
			find_deal_number = int(get_dealnumber_with_chinese[:-1])

		return shopname,find_deal_number

	# 如果搜尋的頁面找不到對應的商家
	except:
		return 0,0

# 轉換中文到網址的格式
def chinese_to_url(chinese):
	url = urllib.parse.quote(chinese)
	return url 

# 試看看有沒有ban掉
# sort = d 放在gcp上面會被ban掉
# 試看看能不能放在GCP
url = 'https://list.tmall.com/search_shopitem.htm?user_id=883737303&q=nex3&sort=td'
source = requests.get(url,headers = headers).text
soup = Bt4(source,'html.parser')
print(soup)
ban_by_Tmall = soup.find("p").text

# 如果IP被Tmall ban掉的話
if '二正忙' in ban_by_Tmall:
	print("目前被ban了")
	
else:

	shop_official = ['小米官方旗艦店','oppo官方旗艦店','華為官方旗艦店','vivo官方旗艦店']
	shop_two_name = ['蘇寧易購官方旗艦店','三際數碼官方旗艦店']

	#搜尋p30 = 搜尋p30+pro
	product_by_url = {'小米9':'%s' % chinese_to_url('小米9'),'Opporeno':'oppo+reno',
						'Vivo-X27':'vivo+x27','華為P30':'p30','華為P30Pro':'p30'} 

	products_by_shops = {'小米9':[shop_official[0]],'Opporeno':[shop_official[1]],
						'Vivo-X27':[shop_official[3]],'華為P30':[shop_official[2]],
						'華為P30Pro':[shop_official[2]]}

	# 把非官方的網站跟官方的網站合起來,這裡 sum(欲合併的陣列,[])會把所有的陣列攤平合在一起,並做 flatten array
	# 這裡稍微注意華為官方網站 的商品有兩個
	for key in products_by_shops.keys():
		products_by_shops[key] = sum([products_by_shops[key],shop_two_name],[])

	res = []

	#迴圈跑每個產品 - 如何華為的只跑一個??
	for key in products_by_shops.keys():

		# 如果產品是華為p30 直接跳過跑下一趟迴圈 只跑P30-Pro的商品
		if key == '華為P30':
			continue

		url = 'https://list.tmall.com/search_product.htm?q=%s&sort=d' % product_by_url[key]
		source = requests.get(url,headers = headers).text
		soup = Bt4(source,'html.parser')



		#迴圈跑所有的店名
		for shopname in products_by_shops[key]:
			d = {}

			#拿到 span標籤裡 data-nick 裡的文字是商店名
			if key == '華為P30Pro':
				p30_list = []
				p30_Pro_list = []

				find_a_label_for_huawei = soup.find_all("a",title=re.compile(r'p30',re.I))
				regular_expression_pro = re.compile(r'pro',re.I)

				for index, item in enumerate(find_a_label_for_huawei):
					# 如果找不到Pro 就表示產品為 p30
					
					if not regular_expression_pro.search(find_a_label_for_huawei[index]['title']):
						p30_list.append(item.parent.parent)
					# 否則該產品為p30 Pro

					else:
						p30_Pro_list.append(item.parent.parent)
				# 因為這裡不知道到底 產品 [key] 是 華為p30還是華為p30-Pro 我這裡用 try catch處理
				# 若 key 跑到 p30 的時候 沒有問題 

				# 
				for htmlscript_in_list in p30_list:
					# 抓下來的資料處理完以後的商店名字跟現在要處理的商店名字一樣實跳出迴圈
					if Get_the_dealnumber(htmlscript_in_list,shopname)[0] == shopname:
						d['Dealnumber'] = Get_the_dealnumber(htmlscript_in_list,shopname)[1]
						d['Shopname'] = shopname
						d['Product'] = '華為P30'
						d['Timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")
						res.append(d)
						# 這裡若 d 不做清空接著跑P30Pro的時候新寫入的資料會把P30給蓋掉
						d = {}
						break
				
				for htmlscript_in_list in p30_Pro_list:
					if Get_the_dealnumber(htmlscript_in_list,shopname)[0] == shopname:
						d['Dealnumber'] = Get_the_dealnumber(htmlscript_in_list,shopname)[1]
						d['Shopname'] = shopname
						d['Product'] = '華為P30Pro'
						d['Timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")
						res.append(d)
						d = {}
						break

				
			# 如果不是華為的產品
			else:

				time.sleep(random.randint(1,3))
				d['Shopname'] = shopname
				d['Product'] = key
				d['Timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")
				d['Dealnumber'] = Get_the_dealnumber(soup,shopname)[1]
				res.append(d)

