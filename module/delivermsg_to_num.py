import re
import dateparser
from datetime import datetime
import numpy as np

def Ru(text,time_text):
    # 3–5 рабочих дней
    # 1 рабочий день 工作日
    # 1–2 недели 週
    # 2 недели
    # Доставка с 13.11 по 17.11
    # на складе

    check_is_number_re = re.compile(r'(\d)')
    # 2 weeks
    case0_re = re.compile(r'(\d+)\s')
    # 2–3 business days
    case1_re = re.compile(r'(\d+)–(\d+)')
    # Доставка с 13.11 по 17.11
    case2_re = re.compile(r'\s(\d+\.\d+)\sпо\s(\d+\.\d+)')


    # 如果還有存貨的話 , 例如:In Stock
    # 如果 字串裡面有 - 的話 例如: 3 - 5 business day
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        if '–' in text:
            start_day = int(case1_re.findall(text)[0][0])
            end_day = int(case1_re.findall(text)[0][1])
            date_gap = start_day + (end_day - start_day)/2 
        else:
            date_gap = int(case0_re.findall(text)[0])
        if 'недели' in text or 'недель' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        else:
            return date_gap
    elif check_is_number_re.findall(text):
        #    Доставка с 13.11 по 17.11
        start_day = case2_re.findall(text)[0][0].replace('.','/')
        end_day = case2_re.findall(text)[0][1].replace('.','/')

        start_day = dateparser.parse(start_day,date_formats=['%d/%m'])
        end_day = dateparser.parse(end_day,date_formats=['%d/%m'])

        start_day = date_gap_calculate(start_day,time_text)
        end_day = date_gap_calculate(end_day,time_text)

        date_gap = start_day + (end_day - start_day)/2 
        return date_gap
    elif 'на складе' in text:
        date_gap = 0
        return date_gap
    else:
        date_gap = np.nan
        return date_gap
#--------------------------------------------------------------------
def Cn(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    # 8 周 13303
    # 1 个工作日 7044
    case0_re = re.compile(r'(\d+)\s')
    # 1-2 周 2464
    # 9-11 个工作日 38873
    case1_re = re.compile(r'(\d+)-(\d+)')
    #预计 10 月 23 日送达 (部分地区) 15201
    case2_re = re.compile(r'\s(\d+\s月\s\d+\s)日')

    # 有现货 0
    if check_is_number_re.findall(text[0]):
        if '-' in text:
            start_day = int(case1_re.findall(text)[0][0])
            end_day = int(case1_re.findall(text)[0][1])
            date_gap = start_day + (end_day - start_day)/2 

        else:
            date_gap = int(case0_re.findall(text)[0][0])
        if '周' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        elif '工作日' in text:
            return date_gap
    # 如果字串裡有數字
    elif check_is_number_re.findall(text):
        #预计 10 月 23 日送达 (部分地区) 15201

        end_day = case2_re.findall(text)[0].replace('月','/')
        end_day = dateparser.parse(end_day,date_formats=['%m / %d'])
        date_gap = date_gap_calculate(end_day,time_text)
        return date_gap

    elif '有现货' in text:
        date_gap = 0
        return date_gap
    else:
        date_gap = np.nan
        return date_gap
#--------------------------------------------------------------------
def Tw(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    # 8 週 13163
    # 1 個工作天 24130
    case0_re = re.compile(r'(\d+)\s')
    # 1-3 個工作天 44042
    # 3-4 週 13165
    case1_re = re.compile(r'(\d+)-(\d+)')
    # 2019/06/14 - 2019/06/18 43985
    # 2021/10/23 - 2021/10/30 — 免額外付費
    case2_re = re.compile(r'(.*)\s-\s(.{10})')
    # Delivers 13 November 15386
    case3_re = re.compile(r'\s(.*)')

    # 多數地區 10 月 23 日送達 15173
    case4_re = re.compile(r'\s(\d+\s月\s\d+\s)日') 


    # 2021/1/5 13633
    # 有現貨 0
    if check_is_number_re.findall(text[0]):
        if '-' in text:
            # 2019/06/14 - 2019/06/18 43985
            try:
                start_day = dateparser.parse(case2_re.findall(text)[0][0])
                end_day = dateparser.parse(case2_re.findall(text)[0][1])
                
                # start_day 已經是跟Timestamp的時間差了 ex: 5天
                start_day = date_gap_calculate(start_day,time_text)
                end_day = date_gap_calculate(end_day,time_text)
            # 1-3 個工作天 44042
            # 3-4 週 13165  
            except:
                start_day = int(case1_re.findall(text)[0][0])
                end_day = int(case1_re.findall(text)[0][1])
            date_gap = start_day + (end_day - start_day)/2 
        else:
            # 2 weeks
            # 3 business days
            if '週'in text or '工作天' in text:
                date_gap = int(case0_re.findall(text)[0])
            # 27 Dec
            else:
                end_day = dateparser.parse(text)
                date_gap = date_gap_calculate(end_day,time_text)
        # print(start_day,',',end_day)
        if '週' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        else:
            return date_gap
    # 如果字串裡有數字
    elif check_is_number_re.findall(text):
        # 多數地區 10 月 23 日送達 15173

        try:
            end_day = case4_re.findall(text)[0].replace('月','/')
            end_day = dateparser.parse(end_day,date_formats=['%m / %d'])
            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
        # 2021/1/5 13633
        except:
            # 星期五 2021/03/26 376
            if '星期' in text:
                end_day = dateparser.parse(case3_re.findall(text)[0])
            # 2021/1/5 13633
            else:
                end_day = dateparser.parse(case4_re.findall(text)[0])

            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
    elif '有現貨' in text:
        date_gap = 0
        return date_gap
    else:
        date_gap = np.nan
        return date_gap
#--------------------------------------------------------------------
def Uk(text,time_text):
    # 2 weeks 9595
    # 2-3 weeks
    # 3 business days
    # 2-3 business days

    # 27 Dec
    # 12-14 business days
    # Delivers 13 November
    # Wed 23 Sep 
    # Tue 4 Aug – Fastest
    # 7 Dec - 14 Dec

    # 27 Dec 45262

    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    # 2 weeks
    # 3 business days
    case0_re = re.compile(r'(\d+)\s')
    #3-5 Business Days 66
    #12-14 business days ok
    case1_re = re.compile(r'(\d+)-(\d+)')

    # 7 Dec - 14 Dec ok 46220
    case2_re = re.compile(r'(.*)\s-\s(.*)')
    # Wed 23 Sep 
    # Delivers 13 November 15386
    case3_re = re.compile(r'\s(.*)')

    # Tue 4 Aug – Fastest ok 21043
    case4_re = re.compile(r'.*\s(\d+.*)\s–\s') # 注意後面的前後橫槓是不一樣的

    #3-5 Business Days ok
    #12-14 business days ok
    # 7 Dec - 14 Dec ok
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        if '-' in text:
            # 7 Dec - 14 Dec
            try:
                start_day = dateparser.parse(case2_re.findall(text)[0][0])
                end_day = dateparser.parse(case2_re.findall(text)[0][1])
                # start_day 已經是跟Timestamp的時間差了 ex: 5天
                start_day = date_gap_calculate(start_day,time_text)
                end_day = date_gap_calculate(end_day,time_text)
            #3-5 Business Days 66
            #12-14 business days ok    
            except:
                start_day = int(case1_re.findall(text)[0][0])
                end_day = int(case1_re.findall(text)[0][1])

            date_gap = start_day + (end_day - start_day)/2 

        else:
            # 2 weeks
            # 3 business days
            if 'weeks'in text or 'day' in text:
                date_gap = int(case0_re.findall(text)[0])

            # 27 Dec
            else:
                end_day = dateparser.parse(text)
                date_gap = date_gap_calculate(end_day,time_text)

        # print(start_day,',',end_day)
        if 'weeks' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        else:
            return date_gap

    # 如果字串裡有數字
    elif check_is_number_re.findall(text):
        # Wed 23 Sep 
        # Delivers 13 November 15386
        try:
            end_day = dateparser.parse(case3_re.findall(text)[0])
            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
        # Tue 4 Aug – Fastest ok
        except:
            end_day = dateparser.parse(case4_re.findall(text)[0])
            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
    elif 'In stock' in text:
        date_gap = 0
        return date_gap
    else:
        return np.nan
#--------------------------------------------------------------------

def Hk(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    #如果有字串 3-5 Business Days
    case0_re = re.compile(r'(\d+)-(\d+)')
    #6–8 weeks
    case1_re = re.compile(r'(\d+)–(\d+)')
    # 01/04/2021 - 08/04/2021. 10/1- 10/8
    # "12/11/2021 - 19/11/2021 — Free",
    case2_re = re.compile(r'(.*)\s-\s(.{10})')
    # Wed 31/03/2021
    case3_re = re.compile(r'\s(.*)')


    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        #   01/04/2021 - 08/04/2021.
        if len(text)>20:
            start_day = dateparser.parse(case2_re.findall(text)[0][0],date_formats=['%d/%m/%Y'])
            end_day = dateparser.parse(case2_re.findall(text)[0][1],date_formats=['%d/%m/%Y'])
            # start_day 已經是跟Timestamp的時間差了 ex: 5天
            start_day = date_gap_calculate(start_day,time_text)
            end_day = date_gap_calculate(end_day,time_text)

        else:
            # 有兩種 槓槓 '–','–'
            if '-' in text:
                start_day = int(case0_re.findall(text)[0][0])
                end_day = int(case0_re.findall(text)[0][1])

            elif '–' in text:
                start_day = int(case1_re.findall(text)[0][0])
                end_day = int(case1_re.findall(text)[0][1])

            # 直接是日期 01/02/2020
            else:
                end_day = dateparser.parse(text,date_formats=['%d/%m/%Y'])
                end_day = date_gap_calculate(end_day,time_text)
                # 這樣子設定是因為等下帶入 gap = s + ( e- s)/2. gap 算出來才會是 e
                #e.g. 32 = 32 +(32-32)/2
                start_day = end_day

        date_gap = start_day + (end_day - start_day)/2          

        # 如果是週
        if 'weeks' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        else:
            return date_gap

    # 如果字串裡面有任何數字
    elif check_is_number_re.findall(text):
        # Wed 31/03/2021
        date = dateparser.parse(case3_re.findall(text)[0],date_formats=['%d/%m/%Y'])
        # 進行日期差的計算
        date_gap = date_gap_calculate(date,time_text)
        return date_gap
    elif 'Tomorrow' in text:
        date_gap = 1
        return date_gap
    else:
        return np.nan
#--------------------------------------------------------------------
def De(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    #如果有字串 à  5 à 7 jours ouvrables. 5-7 工作天
    case0_re = re.compile(r'(\d+)–(\d+)')
    # 如果是兩個日期 14 Jan - 17 Jan
    case1_re = re.compile(r'(.*)\s-\s(.*)')
    # Jeu. 16 Juil. – Gratuite. or Sat, Sep 19 – Express 這兩種情況
    case2_re = re.compile(r'\s(.*)\s–\s')
    # 如果是兩個日期再加一個字串 # 1 Oct. - 6 Oct. – Gratuite
    case3_re = re.compile(r'(.*)\s-\s(.*)\s–\s') # 注意後面的前後橫槓是不一樣的
    # Livraison am 13/11
    case4_re = re.compile(r'am\s(.*)')
    # Mo 4 Mai
    case5_re = re.compile(r'\s(.*)')
    
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        # 如果 Werktage or Wochen 在字串裡
        if 'Werktag' in text or 'Wochen' in text:
            #  3-5 Werktage
            if '–' in text:
                start_day = int(case0_re.findall(text)[0][0])
                end_day = int(case0_re.findall(text)[0][1])
                date_gap = start_day + (end_day - start_day)/2
            else:
                date_gap = int(text[0])
                # 如果是週
            if 'Wochen' in text:
                date_gap = date_gap * 7          
                return (date_gap)
            # 就是日
            else:
                return (date_gap)

        # 如果沒有 Werktage or Wochen
        # 如果是有 - 在字串裡
        elif '-' in text:
            # 1 Aug - 8 Aug – Schnellste: 不帶年分, 1 Sep - 8 Sep – Kostenlos: 不帶年分
            if 'Schnellste' in text or 'Kostenlos' in text:
                start_day = dateparser.parse(case3_re.findall(text)[0][0])
                end_day = dateparser.parse(case3_re.findall(text)[0][1])
            # 14 Jan - 17 Jan : 兩個日期 不帶年分
            else:
                start_day = dateparser.parse(case1_re.findall(text)[0][0])
                end_day = dateparser.parse(case1_re.findall(text)[0][1])

            # start_day 已經是跟Timestamp的時間差了 ex: 5天
            start_day = date_gap_calculate(start_day,time_text)
            end_day = date_gap_calculate(end_day,time_text)
            # 進行日期差的計算
            date_gap = start_day + (end_day - start_day)/2

            return (date_gap)

        # 10 Mrz:直接是日期 不帶年分
        else:
            date = dateparser.parse(text)
            # 把 timestamp 的 年份 帶入 寄送日期
            # 進行日期差的計算
            date_gap = date_gap_calculate(date,time_text)
            return (date_gap)
        
    # 如果字串裡面有任何數字
    elif check_is_number_re.findall(text):
        # 把 Timestemp 文字 轉成datetime
        date_timestamp = time_text
        date_timestamp = datetime.strptime(date_timestamp, "%Y-%m-%d")

        # Lieferung am 13.11. 11/13 送達
        if 'Lieferung' in text:
            date = case4_re.findall(text)[0]
            # 為了要通過dateparser 把. 換成/
            date = date.replace(".", "/")
            date = dateparser.parse(date)

            date_gap = date_gap_calculate(date,time_text)
            return (date_gap)

        # 如果是 Jeu. 21 Nov. 字串長度小於 15 但通常出現這個情況 date_gap is 1
        elif len(text)<15:
            date = case5_re.findall(text)[0]
            date = dateparser.parse(date)
            date_gap = date_gap_calculate(date,time_text)
            return (date_gap)
        # Jeu. 16 Juil. – Gratuite. or Sat, Sep 19 – Express 這兩種情況
        else:
            date = case2_re.findall(text)[0]
            date = dateparser.parse(date)
            date_gap = date_gap_calculate(date,time_text)
            return (date_gap)
    elif 'Auf Lager' in text:
        date_gap = 0
        return (date_gap)
    else:
        return (np.nan)
#--------------------------------------------------------------------
def Fr(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    #如果有字串 à  5 à 7 jours ouvrables. 5-7 工作天
    case0_re = re.compile(r'(\d+)\sà\s(\d+)')
    # 如果是兩個日期 1 Oct. - 8 Oct. 10/1- 10/8
    case1_re = re.compile(r'(.*)\s-\s(.*)')
    # Jeu. 16 Juil. – Gratuite. or Sat, Sep 19 – Express 這兩種情況
    case2_re = re.compile(r'\s(.*)\s–\s')
    # 如果是兩個日期再加一個字串 # 1 Oct. - 6 Oct. – Gratuite
    case3_re = re.compile(r'(.*)\s-\s(.*)\s–\s') # 注意後面的前後橫槓是不一樣的
    # Livraison le 13/11
    case4_re = re.compile(r'le\s(.*)')
    # Jeu. 21 Nov. 
    case5_re = re.compile(r'\s(.*)')
    
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        # 5 à 7 jours ouvrables. 5-7 工作天
        # 1 à 2 semaines. 1-2 週
        # 1 Oct. - 6 Oct. – Gratuite
        # 25 Sept.直接是日期
        if 'à' in text:
            start_day = int(case0_re.findall(text)[0][0])
            end_day = int(case0_re.findall(text)[0][1])
            date_gap = start_day + (end_day - start_day)/2
            # 如果是週
            if 'semaines' in text:
                date_gap = date_gap * 7
                return date_gap
                
            # 就是日
            else:
                return date_gap
        # 如果是兩個日期再加一個字串 # 1 Oct. - 6 Oct. – Gratuite
        # 如果是兩個日期 1 Oct. - 8 Oct. 10/1- 10/8
        elif '-' in text:
            if 'Gratuite' in text or'Express' in text:
                start_day = dateparser.parse(case3_re.findall(text)[0][0])
                end_day = dateparser.parse(case3_re.findall(text)[0][1])

            else:
                start_day = dateparser.parse(case1_re.findall(text)[0][0])
                end_day = dateparser.parse(case1_re.findall(text)[0][1])

#             date_timestamp = time_text
#             date_timestamp = datetime.strptime(date_timestamp, "%Y-%m-%d")
            # start_day 已經是跟Timestamp的時間差了 ex: 5天
            start_day = date_gap_calculate(start_day,time_text)
            end_day = date_gap_calculate(end_day,time_text)
            # 進行日期差的計算
            date_gap = start_day + (end_day - start_day)/2
            return date_gap
        
        else:
            # 1 jour ouvrable . 1 工作天
            if 'ouvrable' in text:
                date_gap = int(text[0])
                return (date_gap)
            elif 'semaines' in text:
                date_gap = int(text[0]) * 7
                return (date_gap)

            # 25 Sept.直接是日期
            else:
                date = dateparser.parse(text)
                # 把 timestamp 的 年份 帶入 寄送日期
                # 進行日期差的計算
                date_gap = date_gap_calculate(date,time_text)
                return (date_gap)

    # 如果字串裡面有任何數字 -- 這個部分要把日期拿去跟 Timestamp相減
    elif check_is_number_re.findall(text):
        # 把 Timestemp 文字 轉成datetime
        date_timestamp = time_text
        date_timestamp = datetime.strptime(date_timestamp, "%Y-%m-%d")

        # Livraison le 13/11. 11/13 送達
        if 'Livraison' in text:
            date = case4_re.findall(text)[0]
            date = dateparser.parse(date)
            # 把 timestamp 的 年份 帶入 寄送日期
            # 進行日期差的計算
            date_gap = date_gap_calculate(date,time_text)
            return (date_gap)

        # 如果是 Jeu. 21 Nov. 字串長度小於 15 但通常出現這個情況 date_gap is 1
        elif len(text)<15:
            date = case5_re.findall(text)[0]
            date = dateparser.parse(date)
            date_gap = date_gap_calculate(date,time_text)
            return date_gap
        # Jeu. 16 Juil. – Gratuite. or Sat, Sep 19 – Express 這兩種情況
        else:
            date = case2_re.findall(text)[0]
            date = dateparser.parse(date)
            # 把 timestamp 的 年份 帶入 寄送日期
            # 進行日期差的計算
            date_gap = date_gap_calculate(date,time_text)
            return date_gap
    elif 'En stock' in text:
        date_gap = 0
        return date_gap
    else:
        return np.nan
#--------------------------------------------------------------------
def Us(text,time_text):
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    # 2 weeks
    case0_re = re.compile(r'(\d+)\s')
    # 2–3 business days
    case1_re = re.compile(r'(\d+)–(\d+)')
    case2_re = re.compile(r'\s(.*)')


    # 如果還有存貨的話 , 例如:In Stock
    # 如果 字串裡面有 - 的話 例如: 3 - 5 business day
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        if '–' in text:
            start_day = int(case1_re.findall(text)[0][0])
            end_day = int(case1_re.findall(text)[0][1])
            date_gap = start_day + (end_day - start_day)/2 
        else:
            date_gap = int(case0_re.findall(text)[0])
        if 'weeks' in text:
            date_gap = date_gap * 7
            return date_gap
        # 就是日
        elif 'day' in text:
            return date_gap

    # 如果字串是: Delivers May 28
    elif 'Delivers' in text:
        date = case2_re.findall(text)[0]
        date = dateparser.parse(date)
        # 把 timestamp 的 年份 帶入 寄送日期
        # 進行日期差的計算
        date_gap = date_gap_calculate(date,time_text)
        return date_gap
    elif 'In Stock' in text:
        date_gap = 0
        return date_gap
    else:
        return np.nan
#-----------------------------------------------------------------------
def Jp(text,time_text):
    # 如果是隔一天就可以拿到，只要是長這樣都是隔一天拿到 範例: 水 2020/10/14
    #判斷是不是數字
    check_is_number_re = re.compile(r'(\d)')
    # 7〜8週間
    # 3-5営業日
    # 9〜11営業日
    # 9/20にお届け
    # 1営業日
    # 2018/11/27 - 2018/12/05
    # 2021/01/09
    case0_re = re.compile(r'(\d+)')
    # 3-5営業日
    # 9〜11営業日
    case1_re = re.compile(r'(\d+)[-〜](\d+)')
    # 水 2021/03/31
    case2_re = re.compile(r'\s(.*)')
    # 2018/11/27 - 2018/12/05
    case3_re = re.compile(r'(.*)\s-\s(.*)')
    # 9/20にお届け
    case4_re = re.compile(r'(\d+/\d+)にお届け')
    # 如果字串裡的第一個字是數字
    if check_is_number_re.findall(text[0]):
        #   01/04/2021 - 08/04/2021.
        if len(text)>20:
            start_day = dateparser.parse(case3_re.findall(text)[0][0])
            end_day = dateparser.parse(case3_re.findall(text)[0][1])
            # start_day 已經是跟Timestamp的時間差了 ex: 5天
            start_day = date_gap_calculate(start_day,time_text)
            end_day = date_gap_calculate(end_day,time_text)
            date_gap = start_day + (end_day - start_day)/2 
            return date_gap
        
        elif '週' in text or '日' in text:
            # 3-5営業日
            # 9〜11営業日
            if '–' in text or '〜' in text:
                start_day = int(case1_re.findall(text)[0][0])
                end_day = int(case1_re.findall(text)[0][1])
                date_gap = start_day + (end_day - start_day)/2 
            # 1営業日
            else:
                date_gap = int(case0_re.findall(text)[0])
            if '週' in text:
                date_gap = date_gap * 7
                return date_gap
            # 就是日
            else:
                return date_gap
        # 9/20にお届け
        elif 'にお届け' in text:
            end_day = dateparser.parse(case4_re.findall(text)[0])
            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
        # 2021/01/09
        else:
            end_day = dateparser.parse(text)
            date_gap = date_gap_calculate(end_day,time_text)
            return date_gap
    # 如果字串裡面有任何數字
    elif check_is_number_re.findall(text):
        # 水 2021/03/31
        end_day = dateparser.parse(case2_re.findall(text)[0])
        date_gap = date_gap_calculate(end_day,time_text)
        return date_gap
    elif '在庫' in text:
        date_gap = 0
        return date_gap
    else:
        return np.nan
    #-----------------------------------------------------------------------
# date_gap_calculate 函數會把 要寄送的日期 跟 紀錄的時間進行相減並調整
def date_gap_calculate(date,time_text)-> float:
    date_timestamp = time_text
    date_timestamp = datetime.strptime(date_timestamp, "%Y-%m-%d")
    # 把 timestamp 的 年份 帶入 寄送日期
    date = date.replace(year = date_timestamp.year)

    # 如果寄送日期在 1到 2月左右會發生 調整時間 後調到太前面 ex: date:2020/1/3 timestamp:2019/12/25 
    if (date - date_timestamp).days < 0:
        date = date.replace(year = date_timestamp.year + 1)
    date_gap = (date - date_timestamp).days
    # 回傳的時間差 單位是日 資料型態是 int or float
    return date_gap