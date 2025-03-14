import pandas as pd

# 這個檔案用來先把原始檔案砍到剩下需要用到的資訊
# 將原始檔案轉為 p_日期.csv

def pre(month, day):
    
    cf = r'C:\Users\student\Desktop\fileeeeeee\_project\新北市公共自行車站點剩餘數量歷史資料\新北市公共自行車站點剩餘數量歷史資料2023-{}-{}.CSV'
    
    try:
        data = pd.read_csv(cf.format(month, day))
        # data.columns 查看欄位名稱
        # Index(['StationUID', 'StationID', 'ServiceAvailable',
        #        'AvailableRentBikes', 'AvailableReturnBikes',
        #        'SrcUpdateTime', 'UpdateTime'], 
        #       dtype='object')
        # srcUpdateTime: 來源端平台資料更新時間
        # UpdateTime: 資料更新日期時間
        
        # 刪除不需要的欄位
        data.drop('StationUID', axis=1, inplace=True)
        data.drop('ServiceAvailable', axis=1, inplace=True)
        
        # 取時間的小時與分鐘
        # data['date'] = data['SrcUpdateTime'].str[5:7] + data['SrcUpdateTime'].str[8:10]
        data['time'] = data['SrcUpdateTime'].str[11:13] + data['SrcUpdateTime'].str[14:16]
        # data['hour'] = data['SrcUpdateTime'].str[11:13]
        # data['min'] = data['SrcUpdateTime'].str[14:16]
        
        # 刪除不需要的欄位
        data.drop('SrcUpdateTime', axis=1, inplace=True)
        data.drop('UpdateTime', axis=1, inplace=True)
        
        data = data.groupby('StationID').apply(lambda x: x.sort_values('time'))
        
        # 增加欄位：BikesCapacity
        # data.loc[:, 'BikesCapacity'] = 0
    
    except Exception as e:
        print("剩餘數量歷史資料df建立失敗：", e)
    
    
    jf = r"C:\Users\user\Desktop\projectD\新北市站位歷史資料[JSON]\新北市自行車租借站位歷史資料2023-{}-{}.JSON"
    # try:
    #     jsondf = pd.read_json(jf.format(month, day))
    #     columns = ['StationID', 'BikesCapacity']
    #     dfj = pd.DataFrame(columns=columns)
        
    #     for i in range(len(jsondf)):
    #         dfj = pd.concat([dfj, pd.DataFrame([[jsondf.iloc[i,-1]['StationID'], 
    #                                             jsondf.iloc[i,-1]['BikesCapacity']]],
    #                                           columns=dfj.columns)],
    #                           ignore_index=True)
    #     # dfj.set_index(['StationID'], inplace=True)
        
    # except Exception as e:
    #     print("站位歷史資料df建立失敗：", e)
    
    # try:
    #     for i in range(len(data)):
    #         ID = str(data.iloc[i,0])
    #         data.iloc[i, 5] = dfj[ dfj['StationID']==ID ].iloc[0, 1]
    # except Exception as e:
    #     print("增加BikesCapacity欄位失敗：", e)
    
    return data

#%%
# data5 = data.head()
# data55 = data.tail()
day30 = ['0'+str(i) for i in range(1, 10)]
day30 += [ str(i) for i in range(10, 31)]
day31 = day30 + ['31']
month = ['07', '08', '09', '10', '11','12'] 


for m in month:
    if m == '09' or m == '11':
        for d in day30:
            df = pre(m, d)
            new_filename = 'p_' + m + d + '.csv'
            df.to_csv(new_filename, index=0)
            print('已完成：', new_filename)
    else:
        for d in day31:
            df = pre(m, d)
            new_filename = 'p_' + m + d + '.csv'
            df.to_csv(new_filename, index=0)
            print('已完成：', new_filename)

