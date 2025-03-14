import pandas as pd
import numpy as np
import time
# 根據各個站點進行分類 B、G、S
# 專題簡報未呈現

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
B,  G,  S  = 0, 0, 0
Bw, Gw, Sw = 0, 0, 0
Bh, Gh, Sh = 0, 0, 0

# 設定閥值
set_threshold = .1

# 每日各站點的可容納車輛位數 df
dfstop = pd.read_csv(stopfn, index_col=0).astype('int16')

# 設定 df
df = pd.DataFrame(index=dfstop.index)
df[['B', 'Bw', 'Bh', 'G', 'Gw', 'Gh', 'S', 'Sw', 'Sh']] = 0


for md in mdlist:
    # 設定開始時間
    start = time.time()
    # 取得每日車位狀況 dataframe，變數 md
    dfmd = pd.read_csv(csvfn.format(md))
    dfmd.drop('time', axis=1, inplace=True)
    
    # 是否是假日
    isHoli_bool = True if md in holidays else False    
    
    statID = ''
    try:
        for i in range(len(dfmd)):
            
            # 若站點代號已更換，將重新取得該日該站點之可容納車位
            if statID != dfmd.loc[i, 'StationID']:
                statID = dfmd.loc[i, 'StationID']    # 重新設定站點代號
                amount = dfstop.loc[statID, md]    # 重新取得 BikeCapacity
                threshold = amount*0.1
            
            # 可借數量：rent，可還數量：retu
            rent = abs(dfmd.loc[i, 'AvailableRentBikes'])
            retu = abs(dfmd.loc[i, 'AvailableReturnBikes'])
            
            # 零值提示
            if amount == 0:
                print(md)
            # else:
                # 計算缺車、缺位比率
                # b = rent / amount
                # s = retu / amount
            
            # 若是小於缺車門檻
            if rent < threshold:
                # B += 1
                df.loc[statID, 'B'] += 1
                if isHoli_bool:
                    # Bh += 1
                    df.loc[statID, 'Bh'] += 1
                else:
                    # Bw += 1
                    df.loc[statID, 'Bw'] += 1
            
            # 若是小於缺位門檻
            if retu < threshold:
                # S += 1
                df.loc[statID, 'S'] += 1
                if isHoli_bool:
                    # Sh += 1
                    df.loc[statID, 'Sh'] += 1
                else:
                    # Sw += 1
                    df.loc[statID, 'Sw'] += 1
            
            # 若是位於安全門檻
            elif not rent < threshold:
                # G += 1
                df.loc[statID, 'G'] += 1
                if isHoli_bool:
                    # Gh += 1
                    df.loc[statID, 'Gh'] += 1
                else:
                    # Gw += 1
                    df.loc[statID, 'Gw'] += 1
            
        print('已完成：', md, '，花', time.time()-start, '秒')
    
    except Exception as e:
        print(md)
        print(e)



#%%

pList = [B, G, S, Bw, Gw, Sw, Bh, Gh, Sh]


a = np.array([pList[:3]+ [sum(pList[:3])],
              pList[3:6] + [sum(pList[3:6])],
              pList[6:] + [sum(pList[6:])],
              [pList[i]+pList[i+3]+pList[i+6] for i in range(3)]+[sum(pList)]])
# array([[ 8248514, 30974681,  1069629],
#        [ 6159263, 20866168,   730224],
#        [ 2089251, 10108513,   339405]])
print(a)
a.reshape(4, 4)
ss = a[0] / sum(a[0])

np.save('dfstop_11_12', df)

