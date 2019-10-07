def impose_none(Product_info,maininfo):
    # Max_length_data = 0
    Max_length_data = len(max(map(lambda x: x['Timestamp'],list(Product_info.values())),key=len))
    # for key,value in Product_info.items():
    #   data_length = len(value['Timestamp'])
    #   if data_length > Max_length_data:
    #       Max_length_data = data_length
    # 產生none
    
    for key,value in Product_info.items():
        data_length = len(value['Timestamp'])
        # print(data_length)
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

    return Product_info