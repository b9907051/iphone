from sshtunnel import SSHTunnelForwarder
from module import dailydata_to_weeklydata as dw
from module import impose_none as impn

import pymysql.cursors
import platform
import paramiko
import math
import json
import csv


# 登入資訊 sql
sql_hostname = "mytestdb.c72ftrj7ifc7.ap-northeast-1.rds.amazonaws.com"
sql_username = "root"
sql_password = "lay911225"
sql_main_database = "Appleinfo"
sql_port = 3306
ssh_host = "ec2-13-114-122-68.ap-northeast-1.compute.amazonaws.com"
ssh_user = "ec2-user"
ssh_port = 22
sql_ip = "1.1.1.1.1"

# 中關村的 maininfo 是 'price'
# 天貓的 maininfo 是 'Dealnumber'
if platform.system() == "Windows":
    # Local 端
    mypkey = paramiko.RSAKey.from_private_key_file(
        "C:\\Users\\user\\Desktop\\Layx_Tokyo.pem"
    )
else:
    # AWS 端
    mypkey = paramiko.RSAKey.from_private_key_file(
        "/home/ec2-user/Chinasmartphone/Layx_Tokyo.pem"
    )


with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_pkey=mypkey,
    remote_bind_address=(sql_hostname, sql_port),
) as tunnel:
    connection = pymysql.connect(
        host="127.0.0.1",
        user=sql_username,
        passwd=sql_password,
        db=sql_main_database,
        port=tunnel.local_bind_port,
    )

    with connection.cursor() as cursor:
        # 拿到天貓的所有資料
        datasource = 'Tmall'
        cursor.execute("""SELECT Product, Timestamp,Dealnumber FROM Tmall.Data""")

        # 拿到中關村的所有資料
        # datasource = 'Zhongguancun'
        # cursor.execute("SELECT * FROM China_Zhongguancun.Data")
        # cursor.description的第一個資訊是欄位名稱 ex:('Product', 253, None, 400, 400, 0, False)
        # columns 拿到所有SQL的欄位
        columns = [col[0] for col in cursor.description]

        data = cursor.fetchall()


# print(data)
# print(columns)
with open(f"static/data/{datasource}.csv", "w", newline="",encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 寫入第一列的欄位名稱
    writer.writerows([columns])

    # 寫入資料
    writer.writerows(data)
