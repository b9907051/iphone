
from sshtunnel import SSHTunnelForwarder
from module import dailydata_to_weeklydata as dw
from module import impose_none as impn

import pymysql.cursors
import platform
import paramiko
import math
import json

# 登入資訊 sql
sql_hostname = 'mytestdb.c72ftrj7ifc7.ap-northeast-1.rds.amazonaws.com'
sql_username = 'root'
sql_password = 'lay911225'
sql_main_database = 'Appleinfo'
sql_port = 3306
ssh_host = 'ec2-13-114-122-68.ap-northeast-1.compute.amazonaws.com'
ssh_user = 'ec2-user'
ssh_port = 22
sql_ip = '1.1.1.1.1'

#中關村的 maininfo 是 'price'
#天貓的 maininfo 是 'Dealnumber'
if platform.system() == 'Windows':
    #Local 端
    mypkey = paramiko.RSAKey.from_private_key_file('C:\\Users\\user\\Desktop\\Layx_Tokyo.pem')
else:
    # AWS 端
    mypkey = paramiko.RSAKey.from_private_key_file('/home/ec2-user/Chinasmartphone/Layx_Tokyo.pem')

def get_datafromsql(datasource,maininfo,timeperiod = 'week'):
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        connection = pymysql.connect(host='127.0.0.1', user=sql_username,
        passwd=sql_password, db=sql_main_database,
        port=tunnel.local_bind_port)


        with connection.cursor() as cursor:
            if datasource == 'China_Zhongguancun.Data':
            # cursor.execute("SELECT * FROM China_Zhongguancun.Data")
                cursor.execute("SELECT * FROM " + datasource)
            elif datasource == 'Tmall.Data':
                cursor.execute("""SELECT Product, Timestamp, SUM(Dealnumber) as Dealnumber FROM Tmall.Data
                            Group by Timestamp, Product
                            """)

            # myresult = cursor.fetchall()
            # cursor.description的第一個資訊是欄位名稱 ex:('Product', 253, None, 400, 400, 0, False)
            # columns 拿到所有SQL的欄位
            columns = [col[0] for col in cursor.description]

            data = cursor.fetchall()

            # 這個地方可能有效能的問題
            # zip 就是做1對1映射
            # 將columns 對 row 做1對1映射 EX: columns:(product,price,Timestamp) , row: (小米9,2999,20190328) 做一對一映射後用dic包
            # rows 是所有的把每一天的資料用dictionary包起來 再用list串起來

            rows = [dict(zip(columns, row)) for row in data]
            Product_name = [name[0] for name in data]

            # set ()函數會把唯一值取出來
            Product_name = list(set(Product_name))
            
            # 創造巢狀Dictionary 把不同的產品放進去
            Product_info = {k: [] for k in Product_name}

            # 將Product_info[key] 裡面每個 [產品] 裡面都加入 [Timestamp] 跟 [Price] 兩個空的dictionary
            for key in Product_info.keys():
                Product_info[key] = {'Timestamp':[], maininfo:[]}

            # print(Product_info)
            # 下一步要把data一個一個塞進去Product_info : 當Product = 小米9 時 把其他兩個欄位的資訊 Timestamp 跟 Price 塞到
            # 小米9的dictionary裡

            # price_array 要拿來放 [所有的價格] 到時候傳到前端判斷最大值
            # price_array 
            # MaxPrice 拿到最大的價格
            Max_info = max([int(row[maininfo]) for row in rows])
            # 計算價格為10的幾次方
            power = math.floor(math.log(Max_info,10))
            # 先將最大價格/power 得到個位數取無條件進位以後 再乘與power就可以得到 最大價格往上一個power的數字

            # print(MaxPrice)
            # 這裡準備為了前端的呈現設計成下列格式
            # Product_info = {'Opporeno':{Price:['200','200','200'.....],Timestamp:['20190504','20190505',''....]},'小米9':{Price:[],Timestamp:[]},..}
            # 
        Data_length_of_product = 0
            # 這裡我整個資料走了 一共 Len(Product_name)次,有幾個產品就走了幾次,有沒有更好的辦法??
        
        for numofdata in rows: # rows = {product:apple',price:'250',Timestamp:
            Product = numofdata['Product']
            Mainfo = numofdata[maininfo]
            Timestamp = numofdata['Timestamp']
            # 這裡有個error處理了兩小時 dictionary 不能 Append 所以
            # Dictionary 在value職擴增的時候要先把他包成串列
            Product_info[Product][maininfo] += [Mainfo]
            Product_info[Product]['Timestamp'] += [Timestamp]

            # 把Product的values 全部取出來用list合併起來
            # [{Price:[1,2,34],Timestamp:[20190531,20190601,20190602]},{Price:[2,3,4],Timestamp:[20190601,...]}..]
            # 每一個套到map裡的function裡處理 lambda 輸入 list(Product_info.values())) 吐出 x['Timestamp']
            # map 完以後會產生一個map的物件 要再用list或是其他函數處理
            # max([],key=len) 是抓取陣列最長的長度
        Timestamp_index_in_list = max(map(lambda x: x['Timestamp'], list(Product_info.values())), key=len)

        # 如果資料想換成週的 timeperiod 放字串 week
        if timeperiod == 'week':
            Product_info = dw.dailydata_to_weeklydata(Product_info,maininfo)

        # 送進去 impose_none 函數裡只能有兩個東西 所以 MaxPrice的部分到後面再放
        Product_info = impn.impose_none(Product_info,maininfo)
        

        Product_info['X_axis'] = Product_info['Opporeno']['Timestamp']
        Product_info['Max_info'] = math.ceil(Max_info / (10**power)) * (10 ** power)
        # print(Product_info)
        
        return json.dumps(Product_info , default=str)