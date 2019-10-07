from bs4 import BeautifulSoup as Bt4
import requests
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import requests
import json
import datetime
import pandas as pd
import os
import shutil
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import paramiko
from paramiko import SSHClient
import urllib
import time
import requests
import re
import heapq
import random
import platform

from bs4 import BeautifulSoup
import requests
import random


headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'list.tmall.com',
'Cookie':'hng=TW%7Czh-TW%7CTWD%7C158; cna=jHXFFBm0WQoCATz7MNNIhhSZ; _med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; UM_distinctid=16a7b974bd6b4-0292494cbf0192-f353163-144000-16a7b974bd72f8; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=VmR9ETNvX%2BmMSD5EbeM22pqnb9rM4ICzcTYWnYET3%2BOPKftkMsbVSvL99lz9AzekqNmmnwauXVkExlCpPdY7QQ%3D%3D; lid=lay9412206; _uab_collina=155713150980738456613855; t=176cce93bf1d1d50235eafac551d6a73; _tb_token_=eeb5de3ee1e1e; cookie2=10bca5b3e4f3af28e3248103f28be498; tracknick=lay9412206; ck1=""; lgc=lay9412206; swfstore=21290; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=UtASsssmfufd&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoTZ7HULcZZRjA%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dBy3qOPriEl4sm1Tc%3D&id2=UUphy%2FA7bLfhK2tpIw%3D%3D&nk2=D8L11Gtav7Mfdw%3D%3D&lg2=URm48syIIVrSKA%3D%3D; csg=27cf4778; skt=993f3b24b65d53ba; whl=-1%260%260%260; x5sec=7b22746d616c6c7365617263683b32223a223362613864653238666437303235653562313930393736663362643831363538434d2b76694f6346454e4755334d47753673727a41786f504d6a49774d5449794e4463774e5455774e6a7378227d; res=scroll%3A1381*5894-client%3A1381*612-offset%3A1381*5894-screen%3A1536*864; cq=ccp%3D1; pnm_cku822=098%23E1hv5pvUvbpvUvCkvvvvvjiPRLLWAjDbRFS9QjYHPmPOQj3bPL5W1jtUnLs9QjlP2QhvCvvvMM%2FtvpvIvvvvvhCvvvvvvUUTphvUypvvvQCvpvACvvv2vhCv2RvvvvWvphvWgUyCvvOUvvVva6RivpvUvvmvnXRrVzUEvpCWmVs%2FvvwK%2BExr1CuKf3qxs4V9eEB%2Bm7zh6jZcR2xVI42viC4AVAdpafFCKdyIvWmy%2BE7rjC69D7zh68g7Ecqh6jc6RqwiLO2v%2BE7rVphCvvOvUvvvphvtvpvhvvvvv8wCvvpvvUmm; isg=BPX1ph6oxVb_XSHObfhQLj0sBHFv2nvK-6ZhkncbNGziThdAPsO7VSqMmFpdDsE8; l=bBaiAnZ7vfBUsT6oBOfNZuIJEZbtiIdb8sPzw49POICP_8f6nEfRWZt28b8BC3GNa6fWJ387PXqBByT3ty4Eh',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
}

# 這個函式所有商品都可以用
def Get_the_dealnumber(htmlscript,shopname):

	shop_list = 'span[data-nick="%s"]'% shopname
	find_shop_span = htmlscript.select(shop_list)

	try:
		get_dealnumber_with_chinese = find_shop_span[0].parent.find('em').text
		# 處理中文
		# 如果拿到的字理面有萬，把後面兩個字"萬筆"去掉
		if re.search("萬",get_dealnumber_with_chinese):
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
url = 'https://list.tmall.com/search_product.htm?q=p30&sort=d'
source = requests.get(url,headers = headers).text
soup = Bt4(source,'html.parser')
# print(soup)
ban_by_Tmall = soup.find("p").text
while True:
	# 如果IP被Tmall ban掉的話
	if '二正忙' in ban_by_Tmall:
		print("目前被ban了")
		time.sleep(3600)
		continue
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

		# return render_template('index.html')
		# print(res)
		sql_hostname = 'mytestdb.c72ftrj7ifc7.ap-northeast-1.rds.amazonaws.com'
		sql_username = 'root'
		sql_password = 'lay911225'
		sql_main_database = 'Appleinfo'
		sql_port = 3306
		ssh_host = 'ec2-13-114-122-68.ap-northeast-1.compute.amazonaws.com'
		ssh_user = 'ec2-user'
		ssh_port = 22
		sql_ip = '1.1.1.1.1'

		if platform.system() == 'Windows':
			#Local 端
			mypkey = paramiko.RSAKey.from_private_key_file('C:\\Users\\user\\Desktop\\Layx_Tokyo.pem')
		else:
			# AWS 端
			mypkey = paramiko.RSAKey.from_private_key_file('/home/ec2-user/Chinasmartphone/Layx_Tokyo.pem')

		with SSHTunnelForwarder(
			(ssh_host, ssh_port),
			ssh_username=ssh_user,
			ssh_pkey=mypkey,
			remote_bind_address=(sql_hostname, sql_port)) as tunnel:
			connection = pymysql.connect(host='127.0.0.1', user=sql_username,
			passwd=sql_password, db=sql_main_database,
			port=tunnel.local_bind_port)

			# 寫入資料	
			with connection.cursor() as cursor:
				for c in res:

					# '這個格式直接把'
					sql = """INSERT INTO
					 Tmall.Data 
					 (Product,Timestamp,Shopname,Dealnumber) 
					 VALUES (%(Product)s,%(Timestamp)s,%(Shopname)s,%(Dealnumber)s)"""

					# 執行sql語法 輸入 users

					# cursor.execute(sql, c)
					# print(sql,c)
					try:
						cursor.execute(sql,c)
						connection.commit()
					except:
						print(c)
						print("錯誤發生有可能是引入相同的資料")
						pass
				print('資料寫入完成')
		break
