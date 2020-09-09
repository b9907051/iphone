from bs4 import BeautifulSoup as Bt4
import requests
from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging,
    jsonify,
    Response,
)

from functools import wraps
import pandas as pd
import json
import requests
import datetime
import pandas as pd
import os
import datetime
import impose_none


from module.get_data_from_csv_V2 import get_csv

# from module.get_data_from_sql import get_datafromsql
from module import dailydata_to_weeklydata as dw

# 登入資訊 login page
username = "Cathayequity"
password = "1qaz2wsxuk"

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

# if platform.system() == "Windows":
#     # Local 端
#     mypkey = paramiko.RSAKey.from_private_key_file(
#         "C:\\Users\\user\\Desktop\\Layx_Tokyo.pem"
#     )
# else:
#     # AWS 端
#     mypkey = paramiko.RSAKey.from_private_key_file(
#         "/home/ubuntu/Iphone11/Layx_Tokyo.pem"
#     )

# 抓下的資料若有缺值進行None的填補
def impose_none(Product_info):
    # Max_length_data = 0
    Max_length_data = len(
        max(map(lambda x: x["Timestamp"], list(Product_info.values())), key=len)
    )
    # for key,value in Product_info.items():
    # 	data_length = len(value['Timestamp'])
    # 	if data_length > Max_length_data:
    # 		Max_length_data = data_length
    # 產生none

    for key, value in Product_info.items():
        data_length = len(value["Timestamp"])
        # print(data_length)
        # 如果資料的常度沒有超過最大值的話
        if data_length < Max_length_data:
            List_none = [None] * (Max_length_data - data_length)
            # print(Product_info[key]['Timestamp'])
            Product_info[key]["Timestamp"] = List_none + Product_info[key]["Timestamp"]
            try:
                Product_info[key]["Dealnumber"] = (
                    List_none + Product_info[key]["Dealnumber"]
                )
            except:
                Product_info[key]["Price"] = List_none + Product_info[key]["Price"]

    return Product_info


# ----------------------------------------- 登入 --------------------------------------------------#


app = Flask(__name__, static_folder="static", static_url_path="")


# datetime.datetime.now().strftime("%Y%m%d")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get Form Fields
        username_candidate = request.form.get("username", False)
        password_candidate = request.form.get("password", False)

        if username_candidate == username:

            if password_candidate == password:
                # Passed
                session["logged_in"] = True
                session["username"] = username

                # flash('You are now logged in', 'success')
                return redirect(url_for("mainpage"))
            else:
                error = "Wrong Password"
                return render_template("login.html", error=error)

        else:
            error = "Username not found"
            return render_template("login.html", error=error)

    return render_template("login.html")


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


# @app.route('/')
# @is_logged_in
# def index():
#     return redirect(url_for('mainpage'))


@app.route("/")
@is_logged_in
def mainpage():
    return render_template("1H2020.html")

@app.route("/TomTom-page")
@is_logged_in
def TomTom_page():
    return render_template("TomTom.html")

@app.route("/1H2020-page")
@is_logged_in
def H12020_page():
    return render_template("1H2020.html")


@app.route("/Zhongguancun")
@is_logged_in
def Zhongguancun():
    return render_template("zhongguanchun.html")


@app.route("/Tmallpage")
@is_logged_in
def Tmallpage():
    return render_template("tmall.html")


# 去後端拿資料的地方
@app.route("/TomTom")
@is_logged_in
def TomTom():

    # name_of_data = request.values.get("namedata")
    df = pd.read_csv("static/data/TomTom.csv")
    df = df.to_dict(orient='list')
    # 把 data 用json的格式 return 回 TomTom.js
    return json.dumps(df)

@app.route("/TomTom2")
@is_logged_in
def TomTom2():

    # name_of_data = request.values.get("namedata")
    df = pd.read_csv("static/data/TomTom_china.csv")
    df = df.to_dict(orient='list')
    # 把 data 用json的格式 return 回 TomTom.js
    return json.dumps(df)

@app.route("/TomTom3")
@is_logged_in
def TomTom3():
    # name_of_data = request.values.get("namedata")
    df = pd.read_csv("static/data/TomTom_europe.csv")
    df = df.to_dict(orient='list')
    # 把 data 用json的格式 return 回 TomTom.js
    return json.dumps(df)

@app.route("/1H2020")
@is_logged_in
def H12020():

    timeperiod = request.values.get("timeperiod")
    # name_of_data = request.values.get("namedata")
    Product_info = get_csv(
        datasource="1H2020", mainInfo="Dealprice", timeperiod=timeperiod
    )
    # session
    # 把參數留在後端
    return Product_info

@app.route("/api")
def api():
    timeperiod = request.values.get("timeperiod")
    # name_of_data = request.values.get("namedata")
    Product_info = get_csv(
        datasource="Zhongguanchun", mainInfo="Dealprice", timeperiod=timeperiod
    )
    # session
    # 把參數留在後端
    return Product_info


@app.route("/Tmall")
def Tmall():

    # request.values.get("變數名稱") 
    # 在 axios.get(`/Tmall?timeperiod=${timePeriod}&mainInfo=Dealprice`) 
    # 這行拿到timeperiod這個標籤的內容 還有我們想看的 maininfo

    timeperiod = request.values.get("timeperiod")
    mainInfo = request.values.get("mainInfo")
    Product_info = get_csv(
        datasource="Tmall5G", mainInfo = mainInfo , timeperiod=timeperiod
    )
    
    return Product_info


@app.route("/delivery-message")
@is_logged_in
def dashboard():
    # 進行 request
    # 從網頁的呼叫拿資訊
    Country = request.values.get("Country")
    Index = request.values.get(
        "Index", "TimeStemp"
    )  # 這裡如果get不到index 會給default值 'TimeStemp'
    Product = request.values.get("Product", "IphoneSE")
    # print(Product)
    # df = get_df()
    # 如果現在是在虛擬環境下的畫路徑使用
    df = pd.read_csv("static/data/Data.csv")
    # 如果現在不是在虛擬環境下的話路徑使用
    # df = pd.read_csv("static/data/Data.csv")
    df = df.drop_duplicates()
    # --------------------- Maping 不同的 國家的名字 ---------------------#
    All_countries = {
        "Us": "美國",
        "Cn": "中國",
        "Jp": "日本",
        "Hk": "香港",
        "Uk": "英國",
        "De": "德國",
        "Ru": "俄羅斯",
        "Fr": "法國",
        "Tw": "台灣",
        "Br": "巴西",
        "Mx": "墨西哥",
    }
    All_countries_E = {
        "Us": "United State",
        "Cn": "China",
        "Jp": "Japan",
        "Hk": "Hong kong",
        "Uk": "Unkted Kingdom",
        "De": "German",
        "Ru": "Russia",
        "Fr": "French",
        "Tw": "Taiwan",
        "Br": "Brazil",
        "Mx": "Mexico",
    }

    df["All_countries"] = df.Country.map(All_countries)
    # 只把我們要的 product 拿出來
    df = df[df["Product"] == Product]

    # 如果是AirPod的話 沒有size color 等資訊
    try:
    # 把Size裡的項目轉成類別等等進行pivot就會排好
        Product_Categories = df["Size"].unique().tolist()
        df["Size"] = df["Size"].astype(
            pd.api.types.CategoricalDtype(categories=Product_Categories)
        )

        pivot = pd.pivot_table(
            df,
            values="Deliver",
            # index=["All_countries", "Colors", "Size"],
            index=Index,
            columns=["All_countries", "Colors", "Size"],
            aggfunc=lambda x: " ".join(x),
        ).sort_index(ascending=False)

        # ---------------------     協理要的國家排序    ---------------------#
        cols = ["美國", "中國", "香港", "台灣", "日本", "英國", "德國", "法國", "俄羅斯"]
        cols2 = ["美國", "中國", "香港", "日本", "德國", "英國", "法國", "英國", "俄羅斯"]
        try:
            pivot = pivot[cols]
        except:
            pivot = pivot[cols2]
        finally:
            # df_fill_country會把篩選過後的表格輸出

            # ---------------------  返回網頁 --------------------------#
            if not Country:
                Title = "Overview"
                Table = pivot
                Country = None

            # 如果有選擇國家的話
            else:
                df_fill_country = df[df["Country"] == Country]
                df_fill_country = pd.pivot_table(
                    df_fill_country,
                    values="Deliver",
                    index=Index,
                    columns=["All_countries", "Colors", "Size"],
                    aggfunc=lambda x: " ".join(x),
                ).sort_index(ascending=False)

                Table = df_fill_country
                Title = All_countries_E[Country]

            return render_template(
                "All.html",
                Table=Table.to_html(classes="table table-striped table-hover"),
                Title=Title,
                Country=Country,
                Product=Product,
            )
    except:
        pivot = df
        pivot = pd.pivot_table(
            pivot,
            values="Deliver",
            index=Index,
            columns=["All_countries"],
            aggfunc=lambda x: " ".join(x),
        ).sort_index(ascending=False)
        if not Country:
            Title = "Overview"
            Table = pivot
            Country = None

        # 如果有選擇國家的話
        else:
            df_fill_country = df[df["Country"] == Country]
            Table = df_fill_country
            Title = All_countries_E[Country]

        return render_template(
            "All.html",
            Table=Table.to_html(classes="table table-striped table-hover"),
            Title=Title,
            Country=Country,
            Product=Product,
        )

if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True, host="0.0.0.0", port=80)

