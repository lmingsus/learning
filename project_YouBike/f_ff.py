import pandas as pd

# 進一步取9月1日 YouBike2.0 的固有站點，
# 從 f 檔案轉換為 ff 檔案

# 取日期：0901 的 YouBike2.0 站點代碼
df0912 = pd.read_csv('stop2_0901_1231.csv', index_col=0)

id09 = list(df0912.index)
del df0912

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


# 砍掉 YouBike 1.0 部分
def dropTB10(df):
    df = df[df['StationID'].astype(int) > 9999]
    df.reset_index(drop=True, inplace=True)
    return df


# 再篩選出 0901 的固有站點
# 方法一
def drop1(df):
    indexdrop = []
    for i in range(len(df)):
        if df.loc[i, 'StationID'] not in id09:
            indexdrop.append(i)
    df.drop(indexdrop, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

# 方法二
def drop2(dff):
    gr = dff.groupby(dff['StationID'])
    
    indexdrop2 = []
    grDict = dict(gr.groups)
    for key in grDict.keys():
        # print(key)
        if key not in id09:
            indexdrop2.extend(grDict[key])
    dff.drop(indexdrop2, inplace=True)
    dff.reset_index(drop=True, inplace=True)
    return dff

fn = 'f_{}.csv'
new_fn = 'ff_{}.csv'

# md = '0901'

for md in mdlist:
    try:
        df = pd.read_csv(fn.format(md))
        df = dropTB10(df)
        df = drop2(df)
        df.to_csv(new_fn.format(md), index=False)
        print('已完成：', md)
    except Exception as e:
        print(md, e)


for md in mdlist:
    df = pd.read_csv(fn.format(md))


