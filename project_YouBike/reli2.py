import pandas as pd
import time
import numpy as np
# 得到 營運狀態個數統計
# 以一天每五分鐘共288個時段分

# 假日日期檔
df_holi = pd.read_csv('isholiday2023.csv')

# 設定假日日期，成為 a list of strings
holidays = []
for i in range(len(df_holi)):
    # 只取假日，且日期在九月之後
    if df_holi.loc[i, "isholiday"] and int(df_holi.loc[i, "date"]) > 900:
        date_str =  str(df_holi.loc[i, "date"])
        if len(date_str) == 3:
            holidays.append("0" + date_str)
        else:
            holidays.append(date_str)

# 驗證用： df_holi[df_holi.loc[:,"isholiday"] == True]
del df_holi


# 設定日期 list
months = [str(i) if i>9 else '0'+str(i) for i in range(9, 13)]
days30 = [str(i) if i>9 else '0'+str(i) for i in range(1, 31)]
days31 = days30 + ['31']
mdlist = []
for m in months:
    if m == '09' or m == '11':
        for d in days30:
            mdlist.append(m+d)
    else:
        for d in days31:
            mdlist.append(m+d)
del months, days30, days31

# 設定檔案名
csvfn = 'ff_{}.csv'
stopfn = 'stop2_0901_1231.csv'

# 移除資料不全日期 (from loss_ff.py 檔)
lossdate = ['1029', '1102', '1128']
for loss in lossdate:
    try:
        mdlist.remove(loss)
    except:
        pass

#%%
# 設定各指標
# B,  G,  S  = 0, 0, 0
# Bw, Gw, Sw = 0, 0, 0
# Bh, Gh, Sh = 0, 0, 0

# 設定閥值
set_threshold = .1

# 每日各站點的可容納車輛位數 df
dfstop = pd.read_csv(stopfn, index_col=0).astype('int8')

# 設定矩陣
k = 12*24       # 每五分鐘之各時段
i = 3           # 每日、平日、假日
j = 4           # 缺車B、正常G、缺位S、總和(B+G+S)
arr = np.zeros((k, i, j)).astype('int32')


for md in mdlist:
    # 設定開始時間
    start = time.time()
    # 取得每日車位狀況 dataframe，變數 md
    df = pd.read_csv(csvfn.format(md))
    
    # 計算時段標籤，增加欄位為 "label"
    t_array = np.array(df['time'])
    s = t_array // 100 *12 + t_array %100//5
    df['label'] = s
    print(time.time()-start)
    
    # 是否是假日
    isHoli_bool = True if md in holidays else False    
    
    statID = ''
    try:
        for i in range(len(df)):
            
            # 若站點代號已更換，將重新取得該日該站點之可容納車位
            if statID != df.loc[i, 'StationID']:
                statID = df.loc[i, 'StationID']    # 重新設定站點代號
                amount = dfstop.loc[statID, md]    # 重新取得 BikeCapacity
                threshold = amount*.1
            
            # 可借數量：rent，可還數量：retu
            # rent = abs(df.loc[i, 'AvailableRentBikes'])
            # retu = abs(df.loc[i, 'AvailableReturnBikes'])
            
            # 零值提示
            if amount == 0:
                print(md, statID)
                
            # else:
                # 計算缺車、缺位比率
                # b = rent / amount
                # s = retu / amount
            
            tLabel = df.loc[i, 'label']
            
            safeThres = True
            # 若是小於缺車門檻
            if abs(df.loc[i, 'AvailableRentBikes']) < threshold:
                # B += 1
                arr[tLabel][0][0] += 1
                safeThres = False
                if isHoli_bool:
                    # Bh += 1
                    arr[tLabel][2][0] += 1
                else:
                    # Bw += 1
                    arr[tLabel][1][0] += 1
            
            # 若是小於缺位門檻
            if abs(df.loc[i, 'AvailableReturnBikes']) < threshold:
                # S += 1
                arr[tLabel][0][2] += 1
                safeThres = False
                if isHoli_bool:
                    # Sh += 1
                    arr[tLabel][2][2] += 1
                else:
                    # Sw += 1
                    arr[tLabel][1][2] += 1
            
            # 若是位於安全門檻
            if safeThres:
                # G += 1
                arr[tLabel][0][1] += 1
                if isHoli_bool:
                    # Gh += 1
                    arr[tLabel][2][1] += 1
                else:
                    # Gw += 1
                    arr[tLabel][1][1] += 1
            
        print('已完成：', md, '，花', time.time()-start, '秒')
    
    except Exception as e:
        print(m+d)
        print(e)



#%%
np.save('arr09_10', arr)
