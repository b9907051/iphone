
# Product_info:
# maininfo:

def impose_none(Product_info,maininfo):
    # Max_length_data = 0
    # map(a,b)  會把 list b 的東西一個一個套到函數 a 裡面再輸出
    Max_length_data = len(max(map(lambda x: x['Timestamp'],list(Product_info.values())),key=len))

    
    for key,value in Product_info.items():
        data_length = len(value['Timestamp'])
        # 如果資料的常度沒有超過最大值的話
        if data_length < Max_length_data:
            List_none = [None] * (Max_length_data - data_length)
            # print(Product_info[key]['Timestamp'])
            Product_info[key]['Timestamp'] = List_none + Product_info[key]['Timestamp']
            Product_info[key][maininfo] = List_none + Product_info[key][maininfo]
            # try:
            #     Product_info[key]['Dealnumber'] = List_none + Product_info[key]['Dealnumber']
            # except:
            #     Product_info[key]['Price'] = List_none + Product_info[key]['Price']
    # print(Product_info)
    return Product_info