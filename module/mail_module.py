# 寄信 模組
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import time
import sys
import os
import platform
from pretty_html_table import build_table

def send_mail(subject_normal,subject_abnormal,mail_output):
    msg = MIMEMultipart()
    msg['From'] = 'layx@cathaylife.com.tw'
    # passwd = getpass.getpass(colors.OKGREEN + 'Password: ')

    passwd = 'Lay@9412206'

    #如果mail_output 是空的
    if mail_output.empty:
        msg['subject'] = subject_normal
    else:
        msg['subject'] = subject_abnormal
        
    start = f"""<html>
                    <body>
                    <style>

                        span {{
                            color: red;
                            font-weight:bold;
                            text-decoration:underline;
                        }}
                    </style>
                    <p> 本訊號上漲只有 上週 Z-score 為<span style="color: #000000;">負</span>本週Z-score為<span>正</span>才會出現 </p>
                    <p> 本訊號下跌只要 本週 Z-score為<span>正</span>就會出現 </p>
                    <p> 該Z-score 之計算為<span>(每週報價之月漲幅-歷史平均)/歷史標準差</span></p>

                    </span>
                        </br></br></br>"""
    # 在attach的部分不太知道在藂蝦小要怎麼把 plain text 跟 html 結合在一起???

    #html 裡面CSS 在ID的權限是 0-1-0-0 高等級
    # #bb{{color: black;}}
    # id ="bb"


    # 這個是一個html的範例
    # <span style="font-weight:bold;text-decoration:underline;">
    # 如果build_table 裡面的東西是空的會掛
    try:
        body = build_table(mail_output, 'blue_light')
    except:
        body = ""

    end = """</body>
        </html>
        """
    msg.attach(MIMEText(start + body + end, 'html'))

    # 信箱
    msg['To'] ='lay9412206@gmail.com;'\
    'jalinyang@cathaylife.com.tw;patrickyen@cathaylife.com.tw;'\
    'ericfly168@cathaylife.com.tw;renny@cathaylife.com.tw;kcyu@cathaylife.com.tw;'\
    'aywlang@cathaylife.com.tw;wthuang@cathaylife.com.tw;evanyeh@cathaylife.com.tw;'\
    'jianyou@cathaylife.com.tw;sylviayang@cathaylife.com.tw;cw_huang@cathaylife.com.tw;'\
    'boyu.chen@cathaylife.com.tw;layx@cathaylife.com.tw;liuziwei@cathaylife.com.tw;'\
    'yitsung@cathaylife.com.tw;joelin@cathaylife.com.tw;yaojih@cathaylife.com.tw;yung666666@cathaylife.com.tw;'

    to = msg['To'].split(";")
    #名單
    # 楊嘉林  jalinyang@cathaylife.com.tw
    # 閻志強  patrickyen@cathaylife.com.tw
    # 蔡士弘  ericfly168@cathaylife.com.tw
    # 王正聰  renny@cathaylife.com.tw
    # 尤崑堅  kcyu@cathaylife.com.tw
    # 郎遠聞  aywlang@cathaylife.com.tw
    # 黃維泰  wthuang@cathaylife.com.tw
    # 葉俊宏  evanyeh@cathaylife.com.tw
    # 李建佑  jianyou@cathaylife.com.tw
    # 楊子慧  sylviayang@cathaylife.com.tw
    # 黃秋文  cw_huang@cathaylife.com.tw
    # 陳柏玉  boyu.chen@cathaylife.com.tw
    # 劉悌鐳  layx@cathaylife.com.tw
    # 劉子瑋  liuziwei@cathaylife.com.tw
    # 王怡聰  yitsung@cathaylife.com.tw
    # 林士喬  joelin@cathaylife.com.tw
    # 游堯日  yaojih@cathaylife.com.tw
    # 楊又青  yung666666@cathaylife.com.tw
    print(to)
    s = smtplib.SMTP('cathaymail.linyuan.com.tw', 25)
    s.starttls()
    s.login(msg['From'], passwd)

    context = msg.as_string()
    s.sendmail(msg['From'], to, context)
    print( 'successfully sent  email')
    s.close()