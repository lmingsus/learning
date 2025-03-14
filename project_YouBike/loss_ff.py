import pandas as pd
# 查看 ff 檔案中
# 取 日期：0901 的 YouBike2.0 站點代碼
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

fn = 'ff_{}.csv'


def lossstop(md):
    s = 0
    df = pd.read_csv(fn.format(md))
    
    # 依照各站點進行 groupby
    df_c = df.groupby(["StationID"]).count()
    
    # 是否有缺站點
    if len(df_c) != len(id09):
        print('有缺站點：', md)
    
    # 設定資料有缺失之門檻，每站每天之資料若完整將有 12*24 = 288 筆
    # 這裡設定 280
    df_c = df_c[df_c["time"] < 280]
    
    for i in df_c.index:
        # 印出有缺的
        # print(df_c.loc[i, "time"], end=', ')
        s += 1
    
    if s > 0:
        print('\n', md, s)

for md in mdlist:
    lossstop(md)

# 得到「資料非常不全」的日期：
lossdate = ['1029', '1102', '1128']
# 各日期分別只有 251、207、268 筆資料
