import pandas as pd
import time
import numpy as np
# 得到 營運狀態個數統計

# 假日日期檔
df_holi = pd.read_csv('isholiday2023.csv')

# 設定假日日期成為 a list of strings
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

# 設定檔案名
csvfn = 'ff_{}.csv'
stopfn = r'C:\Users\student\Desktop\fileeeeeee\_project\p_f\stop2_0901_1231.csv'

# 移除資料不全日期 (from loss_ff.py 檔)
lossdate = ['1029', '1102', '1128']
for loss in lossdate:
    mdlist.remove(loss)

# 設定各指標
B, Bw, Bh, G, Gw, Gh, S, Sw, Sh = 0, 0, 0, 0, 0, 0, 0, 0, 0


# 設定閥值
threshold = .1

# 每日各站點的可容納車輛位數
dfstop = pd.read_csv(stopfn, index_col=0).astype('int64')


for md in mdlist:
    start = time.time()
    
    df = pd.read_csv(csvfn.format(md))
    
    statID = ''
    try:
        for i in range(len(df)):
            
            # 若站點代號已更換，將重新取得該日該站點之可容納車位
            if statID != df.loc[i, 'StationID']:
                statID = df.loc[i, 'StationID']    # 重新設定站點代號
                amount = dfstop.loc[statID, md]    # 重新取得 BikeCapacity
            
            # 可借數量：rent、可還數量：retu
            rent = abs(df.loc[i, 'AvailableRentBikes'])
            retu = abs(df.loc[i, 'AvailableReturnBikes'])
            
            # 零值提示
            if amount == 0:
                print(m+d, rent, retu, amount)
                
            else:
                b = rent / amount
                s = retu / amount
            
            if b < threshold:
                B += 1
                if md in holidays:
                    Bh += 1
                else:
                    Bw += 1
            
            if s < threshold:
                S += 1
                if md in holidays:
                    Sh += 1
                else:
                    Sw += 1
            
            if not b < threshold and not s < threshold:
                G += 1
                if md in holidays:
                    Gh += 1
                else:
                    Gw += 1
        print('已完成：', md, '，花', time.time()-start, '秒')
    
    except Exception as e:
        print(m+d)
        print(e)


pList = [B, G, S, Bw, Gw, Sw, Bh, Gh, Sh]

nn = np.array([pList[:3], pList[3:6], pList[6:]])
# array([[ 8248514, 30974681,  1069629],
#        [ 6159263, 20866168,   730224],
#        [ 2089251, 10108513,   339405]])



