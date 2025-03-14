import pandas as pd
# 固定 09月 01日 的 YouBike2.0 站點，
# 取得在該日之後，每日各站點可容納車位數量

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
# mdlist.reverse()


fn = '新北市自行車租借站位歷史資料2023-{}-{}.JSON'

jsondf = pd.read_json(fn.format('09', '01'))

columns = ['StationID', '0901']
df = pd.DataFrame(columns=columns)
for i in range(len(jsondf)):
    if jsondf.loc[i, 'BikeStations']['ServiceType'] == 2:
        df = pd.concat([df, pd.DataFrame([[str(jsondf.loc[i, 'BikeStations']['StationID']), 
                                           jsondf.loc[i, 'BikeStations']['BikesCapacity']]], 
                                         columns=df.columns)], 
                       ignore_index=True)

def bike20(df, md):
    # 增加一欄位
    df[md] = 0
    
    try:
        jsondf = pd.read_json(fn.format(md[:2], md[2:]))
        
        for i in range(len(jsondf)):
            
            # 只取 YouBike2.0
            if jsondf.loc[i, 'BikeStations']['ServiceType'] == 2:
                
                # 只取 09月 01日 之固有站點
                if jsondf.loc[i, 'BikeStations']['StationID'] in df['StationID'].values:
                    mask = df['StationID'] == jsondf.loc[i, 'BikeStations']['StationID']
                    indexi = df[ mask ].index[0]
                    df.loc[indexi, md] = jsondf.loc[i, 'BikeStations']['BikesCapacity']
                    
    except Exception as e:
        # 缺少資料
        print('錯誤', md)
        print(e)
    return df


for md in mdlist:
    if int(md) == 901:
        continue
    else:
        df = bike20(df, md)
        print('已完成：', md)

# 亡羊補牢，把原本設為 0 的日期欄，改為 nan
import numpy as np
for i in range(1, len(df.columns)):
    if (df.iloc[:,i] == 0).all():
        df.iloc[:,i].replace(0, np.nan, inplace=True)

nan_collist = []
for j in range(1, len(df.columns)):
    if np.isnan(df.iloc[:,j]).all():
        nan_collist.append(j)

for j in nan_collist:
    nex = j+1
    if np.isnan(df.iloc[:,nex]).all():
        nex +=1
    back = j-1
    if np.isnan(df.iloc[:,back]).all():
        back -=1
    for i in range(len(df)):
        df.iloc[i,j] = max(df.iloc[i,back], df.iloc[i,nex])
        if df.iloc[i,back] != df.iloc[i,nex]:
            print(i, j)
            # 533 16        # 印出結果
            # 740 16
            # 744 16
            # 747 16
            # 767 16
            # 943 16
            # 363 22
            # 652 22
            # 1037 22

nan_collist2 = []
for j in range(1, len(df.columns)):
    if np.isnan(df.iloc[:,j]).all():
        nan_collist2.append(j)


df.to_csv('stop2_0901_1231.csv', index=False)

