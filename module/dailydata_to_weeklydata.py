import pandas as pd
import datetime
import numpy as np


def explode_list(df, col):

    s = df[col]  # s is the column i got to deal with

    # len(s) give us the number of rows. arange(len(s)) give us a array of number start from 0 ex:arange(2):[0,1]
    # s.str.len() give us the length of list in each row
    # i represent a sequential number. the times of each number appears corresponds to the length of lists in each row
    i = np.arange(len(s)).repeat(
        s.str.len()
    )  # s.str.len() give us the length of list in each row
    ## **可以傳入字典的格式
    # concatenate method will Join a sequence of arrays along an existing axis
    # assign method will create or replace columns of dataframe by dictionary(keys for column name, values for content)
    #print(df)
    return df.iloc[i].assign(**{col: np.concatenate(s)})


def dailydata_to_weeklydata(productinfo, maininfo):
    # 下面一行是拿來測試用 //
    # productioninfo = {'Vivo-X27': {'Timestamp': [datetime.date(2019, 5, 31), datetime.date(2019, 6, 1), datetime.date(2019, 6, 2), datetime.date(2019, 6, 3), datetime.date(2019, 6, 20), datetime.date(2019, 6, 21)], 'maininfo': ['3598', '3598', '3598', '3598', '3598', '3598']}, '華為P30': {'Timestamp': [datetime.date(2019, 4, 15), datetime.date(2019, 4, 16), datetime.date(2019, 4, 17), datetime.date(2019, 4, 18), datetime.date(2019, 4, 19), datetime.date(2019, 4, 20), datetime.date(2019, 4, 21), datetime.date(2019, 4, 22), datetime.date(2019, 4, 23), datetime.date(2019, 4, 24), datetime.date(2019, 4, 25), datetime.date(2019, 4, 26), datetime.date(2019, 4, 27), datetime.date(2019, 4, 28), datetime.date(2019, 4, 29), datetime.date(2019, 4, 30), datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3), datetime.date(2019, 5, 4), datetime.date(2019, 5, 5), datetime.date(2019, 5, 6), datetime.date(2019, 5, 7), datetime.date(2019, 5, 8), datetime.date(2019, 5, 9), datetime.date(2019, 5, 10), datetime.date(2019, 5, 11), datetime.date(2019, 5, 12), datetime.date(2019, 5, 13), datetime.date(2019, 5, 14), datetime.date(2019, 5, 15), datetime.date(2019, 5, 16), datetime.date(2019, 5, 17), datetime.date(2019, 5, 18), datetime.date(2019, 5, 19), datetime.date(2019, 5, 20), datetime.date(2019, 5, 21), datetime.date(2019, 5, 22), datetime.date(2019, 5, 23), datetime.date(2019, 5, 24), datetime.date(2019, 5, 25), datetime.date(2019, 5, 26), datetime.date(2019, 5, 27), datetime.date(2019, 5, 28), datetime.date(2019, 5, 29), datetime.date(2019, 5, 30), datetime.date(2019, 5, 31), datetime.date(2019, 6, 1), datetime.date(2019, 6, 2), datetime.date(2019, 6, 3), datetime.date(2019, 6, 4), datetime.date(2019, 6, 5), datetime.date(2019, 6, 6), datetime.date(2019, 6, 7), datetime.date(2019, 6, 8), datetime.date(2019, 6, 9), datetime.date(2019, 6, 10), datetime.date(2019, 6, 11), datetime.date(2019, 6, 12), datetime.date(2019, 6, 13), datetime.date(2019, 6, 14), datetime.date(2019, 6, 15), datetime.date(2019, 6, 16), datetime.date(2019, 6, 17), datetime.date(2019, 6, 18), datetime.date(2019, 6, 19), datetime.date(2019, 6, 20), datetime.date(2019, 6, 21)], 'maininfo': ['3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988', '3988']}, '小米9': {'Timestamp': [datetime.date(2019, 4, 15), datetime.date(2019, 4, 16), datetime.date(2019, 4, 17), datetime.date(2019, 4, 18), datetime.date(2019, 4, 19), datetime.date(2019, 4, 20), datetime.date(2019, 4, 21), datetime.date(2019, 4, 22), datetime.date(2019, 4, 23), datetime.date(2019, 4, 24), datetime.date(2019, 4, 25), datetime.date(2019, 4, 26), datetime.date(2019, 4, 27), datetime.date(2019, 4, 28), datetime.date(2019, 4, 29), datetime.date(2019, 4, 30), datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3), datetime.date(2019, 5, 4), datetime.date(2019, 5, 5), datetime.date(2019, 5, 6), datetime.date(2019, 5, 7), datetime.date(2019, 5, 8), datetime.date(2019, 5, 9), datetime.date(2019, 5, 10), datetime.date(2019, 5, 11), datetime.date(2019, 5, 12), datetime.date(2019, 5, 13), datetime.date(2019, 5, 14), datetime.date(2019, 5, 15), datetime.date(2019, 5, 16), datetime.date(2019, 5, 17), datetime.date(2019, 5, 18), datetime.date(2019, 5, 19), datetime.date(2019, 5, 20), datetime.date(2019, 5, 21), datetime.date(2019, 5, 22), datetime.date(2019, 5, 23), datetime.date(2019, 5, 24), datetime.date(2019, 5, 25), datetime.date(2019, 5, 26), datetime.date(2019, 5, 27), datetime.date(2019, 5, 28), datetime.date(2019, 5, 29), datetime.date(2019, 5, 30), datetime.date(2019, 5, 31), datetime.date(2019, 6, 1), datetime.date(2019, 6, 2), datetime.date(2019, 6, 3), datetime.date(2019, 6, 4), datetime.date(2019, 6, 5), datetime.date(2019, 6, 6), datetime.date(2019, 6, 7), datetime.date(2019, 6, 8), datetime.date(2019, 6, 9), datetime.date(2019, 6, 10), datetime.date(2019, 6, 11), datetime.date(2019, 6, 12), datetime.date(2019, 6, 13), datetime.date(2019, 6, 14), datetime.date(2019, 6, 15), datetime.date(2019, 6, 16), datetime.date(2019, 6, 17), datetime.date(2019, 6, 18), datetime.date(2019, 6, 19), datetime.date(2019, 6, 20), datetime.date(2019, 6, 21)], 'maininfo': ['2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2899', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808', '2808']}, 'Opporeno': {'Timestamp': [datetime.date(2019, 4, 15), datetime.date(2019, 4, 16), datetime.date(2019, 4, 17), datetime.date(2019, 4, 18), datetime.date(2019, 4, 19), datetime.date(2019, 4, 20), datetime.date(2019, 4, 21), datetime.date(2019, 4, 22), datetime.date(2019, 4, 23), datetime.date(2019, 4, 24), datetime.date(2019, 4, 25), datetime.date(2019, 4, 26), datetime.date(2019, 4, 27), datetime.date(2019, 4, 28), datetime.date(2019, 4, 29), datetime.date(2019, 4, 30), datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3), datetime.date(2019, 5, 4), datetime.date(2019, 5, 5), datetime.date(2019, 5, 6), datetime.date(2019, 5, 7), datetime.date(2019, 5, 8), datetime.date(2019, 5, 9), datetime.date(2019, 5, 10), datetime.date(2019, 5, 11), datetime.date(2019, 5, 12), datetime.date(2019, 5, 13), datetime.date(2019, 5, 14), datetime.date(2019, 5, 15), datetime.date(2019, 5, 16), datetime.date(2019, 5, 17), datetime.date(2019, 5, 18), datetime.date(2019, 5, 19), datetime.date(2019, 5, 20), datetime.date(2019, 5, 21), datetime.date(2019, 5, 22), datetime.date(2019, 5, 23), datetime.date(2019, 5, 24), datetime.date(2019, 5, 25), datetime.date(2019, 5, 26), datetime.date(2019, 5, 27), datetime.date(2019, 5, 28), datetime.date(2019, 5, 29), datetime.date(2019, 5, 30), datetime.date(2019, 5, 31), datetime.date(2019, 6, 1), datetime.date(2019, 6, 2), datetime.date(2019, 6, 3), datetime.date(2019, 6, 4), datetime.date(2019, 6, 5), datetime.date(2019, 6, 6), datetime.date(2019, 6, 7), datetime.date(2019, 6, 8), datetime.date(2019, 6, 9), datetime.date(2019, 6, 10), datetime.date(2019, 6, 11), datetime.date(2019, 6, 12), datetime.date(2019, 6, 13), datetime.date(2019, 6, 14), datetime.date(2019, 6, 15), datetime.date(2019, 6, 16), datetime.date(2019, 6, 17), datetime.date(2019, 6, 18), datetime.date(2019, 6, 19), datetime.date(2019, 6, 20), datetime.date(2019, 6, 21)], 'maininfo': ['2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2999', '2799', '2799', '2799', '2799', '2799', '2799', '2799', '2799']}, '華為P30Pro': {'Timestamp': [datetime.date(2019, 4, 15), datetime.date(2019, 4, 16), datetime.date(2019, 4, 17), datetime.date(2019, 4, 18), datetime.date(2019, 4, 19), datetime.date(2019, 4, 20), datetime.date(2019, 4, 21), datetime.date(2019, 4, 22), datetime.date(2019, 4, 23), datetime.date(2019, 4, 24), datetime.date(2019, 4, 25), datetime.date(2019, 4, 26), datetime.date(2019, 4, 27), datetime.date(2019, 4, 28), datetime.date(2019, 4, 29), datetime.date(2019, 4, 30), datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3), datetime.date(2019, 5, 4), datetime.date(2019, 5, 5), datetime.date(2019, 5, 6), datetime.date(2019, 5, 7), datetime.date(2019, 5, 8), datetime.date(2019, 5, 9), datetime.date(2019, 5, 10), datetime.date(2019, 5, 11), datetime.date(2019, 5, 12), datetime.date(2019, 5, 13), datetime.date(2019, 5, 14), datetime.date(2019, 5, 15), datetime.date(2019, 5, 16), datetime.date(2019, 5, 17), datetime.date(2019, 5, 18), datetime.date(2019, 5, 19), datetime.date(2019, 5, 20), datetime.date(2019, 5, 21), datetime.date(2019, 5, 22), datetime.date(2019, 5, 23), datetime.date(2019, 5, 24), datetime.date(2019, 5, 25), datetime.date(2019, 5, 26), datetime.date(2019, 5, 27), datetime.date(2019, 5, 28), datetime.date(2019, 5, 29), datetime.date(2019, 5, 30), datetime.date(2019, 5, 31), datetime.date(2019, 6, 1), datetime.date(2019, 6, 2), datetime.date(2019, 6, 3), datetime.date(2019, 6, 4), datetime.date(2019, 6, 5), datetime.date(2019, 6, 6), datetime.date(2019, 6, 7), datetime.date(2019, 6, 8), datetime.date(2019, 6, 9), datetime.date(2019, 6, 10), datetime.date(2019, 6, 11), datetime.date(2019, 6, 12), datetime.date(2019, 6, 13), datetime.date(2019, 6, 14), datetime.date(2019, 6, 15), datetime.date(2019, 6, 16), datetime.date(2019, 6, 17), datetime.date(2019, 6, 18), datetime.date(2019, 6, 19), datetime.date(2019, 6, 20), datetime.date(2019, 6, 21)], 'maininfo': ['5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488', '5488']}}

    pd_productioninfo = pd.DataFrame(productinfo)

    pd_productioninfo_index = list(pd_productioninfo.index.values)
    pd_productioninfo_index.append("Week")
    tempdf = pd.DataFrame(
        columns=pd_productioninfo.columns, index=pd_productioninfo_index
    )
    # print(tempdf)
    for i in pd_productioninfo.columns:
        df = pd_productioninfo[i]
        
        # 因為這裡再處理astype('int')時是整串資料一起處理，所以如果使用try catch跳過的話接下來要進行其他的資料運算都會碰到問題，所以
        # 再進行週資料的轉換部分 要放到 impose non 函數之前 以免裡面有none的值出現

        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df[maininfo] = np.array(df[maininfo]).flatten().astype("int")
        df["Week"] = [1 if x == 5 else 0 for x in df["Timestamp"].weekday]
        df["Week"] = np.array(df.Week).cumsum()
        # 這裡不知道為什麼我不能用pd1_productinfo去存，Week的資訊進不去
        tempdf[i] = df


    # loc 是以 index 為主的取值方式, Timestamp 在 tempdf 裡是 index, 取出來會是一個以column為index的series
    for i in range(len(tempdf.loc['Timestamp'])):
        tempdf.loc['Timestamp'][i] = tempdf.loc['Timestamp'][i].strftime("%Y-%m-%d")

    tempdf = pd.DataFrame(tempdf).T

    # 把datime 格式 轉換成文字
    # 這裡要注意!! 雲端上跟這裡的iloc 好像不一樣!!!!
    # 如果是iloc[0,0]我們在windows端會拿到價格,但在linux端會拿到日期
    # 乾乾乾乾乾乾

    # for m in range(len(tempdf)):
    #     tempdf.iloc[m, 1] = [
    #         k.strftime("%Y-%m-%d") for k in pd.to_datetime(tempdf.iloc[m, 1]).tolist()
    #     ]
    # 從時間的格式 pass 成文字
    # print(tempdf["Timestamp"])
    # 這裡 denest dataframe裡的list 並且以index為Label把資料排在一起
    # print(tempdf['Timestamp'])
    df = pd.concat([explode_list(tempdf, col)[col] for col in tempdf.columns], axis=1)
    # print(df)
    dfs_column = [d for d, _ in df.groupby(df.index)]

    dfs = [d for _, d in df.groupby(df.index)]

    df_final = {}

    for k in range(len(dfs_column)):
        # 重設index為數列以後原本的index變成了一個欄位，把他drop掉
        dfs[k] = dfs[k].reset_index().drop(columns="index")
        # 創造出一個包含了所有產品的Dataframe
        df_final[dfs_column[k]] = dfs[k]

        ##進行pivot
        df_final[dfs_column[k]] = pd.pivot_table(
            df_final[dfs_column[k]],
            index=["Week"],
            values=[maininfo, "Timestamp"],
            aggfunc={maininfo: np.mean, "Timestamp": max},
        )
        # print(df_final)
        # 把 flot64轉成Int
        df_final[dfs_column[k]][maininfo] = df_final[dfs_column[k]][maininfo].astype(
            "int"
        )
        # DataFrame 轉dictionary 並且用list 包著
        df_final[dfs_column[k]] = df_final[dfs_column[k]].to_dict("list")
        # print(df_final)
    return df_final
