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

product_index = {'Opporeno':['1262','1261155'],'小米9':['1225','1224655'],
				'華為P30':['1213','1212233'],'華為P30Pro':['1224','1223829'],
				'Vivo-X27':['1263','1262905'],
				'華為Mat30Pro-4G':['1292','1291827'],'華為Mat30Pro-5G':['1266','1265181']}

#為了方便接下來 不同的 網頁index 進行 產品  的對應 將 key 跟 產品互換
#舉例 product_index {1261155: 'Opporeno',...}
product_R = {value[1]: key for key, value in product_index.items()}

res = []
for key,index in product_index.items():

	d = {}

	website = "http://detail.zol.com.cn/%s/%s/price_1.shtml" % (index[0],index[1])

	source = requests.get(website).text
	soup = Bt4(source,'html.parser')
	price = soup.find('em',class_='price-type').text
	# print(price)
	# print(soup.prettify())
	d['Product'] = product_R[index[1]]
	d['Timestamp'] = datetime.datetime.today().strftime("%Y-%m-%d")
	d['Price'] = price

	res.append(d)

# return render_template('index.html')
# print(res)
# sql_hostname = 'mytestdb.c72ftrj7ifc7.ap-northeast-1.rds.amazonaws.com'
# sql_username = 'root'
# sql_password = 'lay911225'
# sql_main_database = 'Appleinfo'
# sql_port = 3306
# ssh_host = 'ec2-13-114-122-68.ap-northeast-1.compute.amazonaws.com'
# ssh_user = 'ec2-user'
# ssh_port = 22
# sql_ip = '1.1.1.1.1'

# if platform.system() == 'Windows':
# 	#Local 端
# 	mypkey = paramiko.RSAKey.from_private_key_file('C:\\Users\\user\\Desktop\\Layx_Tokyo.pem')
# else:
# 	# AWS 端
# 	mypkey = paramiko.RSAKey.from_private_key_file('/home/ec2-user/Chinasmartphone/Layx_Tokyo.pem')

# with SSHTunnelForwarder(
# 	(ssh_host, ssh_port),
# 	ssh_username=ssh_user,
# 	ssh_pkey=mypkey,
# 	remote_bind_address=(sql_hostname, sql_port)) as tunnel:
# 	connection = pymysql.connect(host='127.0.0.1', user=sql_username,
# 	passwd=sql_password, db=sql_main_database,
# 	port=tunnel.local_bind_port)

# 	# 寫入資料	
# 	with connection.cursor() as cursor:
# 		for c in res:

# 			# '這個格式直接把'
# 			sql = """INSERT INTO
# 			 China_Zhongguancun.Data 
# 			 (Product,Timestamp,Price) 
# 			 VALUES (%(Product)s,%(Timestamp)s,%(Price)s)"""

# 			# 執行sql語法 輸入 users
			
# 			# cursor.execute(sql, c)
# 			try:
# 				cursor.execute(sql,c)
# 				connection.commit()

# 			except:
# 				print(c)
# 				print("錯誤發生有可能是引入相同的資料")
# 				pass

