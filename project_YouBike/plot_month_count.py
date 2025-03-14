import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 1.
# 畫歷史站點數量變化

# 讀 csv檔
df = pd.read_csv('history_bikestop.csv')
# df.info()

# 去掉 2024年資料
index2024 = df[ df['VersionID'] > 20240000 ].index
df.drop(index2024, inplace=True)

# 新增一欄，用來放：yyyymm，原本日期drop掉
df.loc[:, 'yearmm'] = 0
for i in range(len(df)):
    ym = str(df.iloc[i, 0])[:6]
    df.iloc[i, 3] = ym
df.drop(columns='VersionID', inplace=True)

# 取每月最後一筆資料
dfm = df.groupby(['yearmm']).tail(1)
del df

#%%
plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] # 將字體設定為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False             # 用來正常顯示負號

plt.figure(figsize=(8, 4.8), dpi=500)

plt.title('新北市歷年各月份 YouBike 建置站點數量', fontsize=16)                  # 設定圖片標題

plt.xlabel('年月（該月月底）', fontsize=14, labelpad=4)    # 設定坐標軸標籤
plt.ylabel('站\n點\n數\n量', fontsize=14, rotation=0, labelpad=10)    # 設定坐標軸標籤

x1 = dfm['yearmm'].astype(str)
y1 = dfm['Bike1.0'].astype(int)

x2 = dfm[ dfm['Bike2.0'].astype(int) != 0]['yearmm'].astype(str)
y2 = dfm[ dfm['Bike2.0'].astype(int) != 0]['Bike2.0'].astype(int)


plt.plot(x1, y1, '.-', label='YouBike1.0')

plt.plot(x2, y2, 'o-', label='YouBike2.0')

xticksl = x1.copy()
xticksl.index = range(36)
for i in range(len(x1)):
    if int(xticksl[i]) % 100 != 1:
        xticksl[i] = ''

xticksl[36] = '202401'
plt.xticks(xticksl)
plt.yticks([i*200 for i in range(7)], fontsize=12) 

plt.grid(color='gray', linestyle='--', linewidth=1)   # 設定格線顏色、種類、寬度

plt.legend()
# loc='upper left'

plt.savefig('p1.png')
plt.show()


# , bbox_inches='tight'