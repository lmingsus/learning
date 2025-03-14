import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 畫各個時段的B、G、S
# 讀取陣列
a1 = np.load('arr_09_10.npy')
a2 = np.load('arr_11_12.npy')
# 合併
a = a1 + a2

# 計算總和欄位
for d in range(288):
    for i in range(3):
        a[d][i][3] = sum(a[d][i][:3])

# 設定 a 的百分比 array
p = a.copy().astype('float32')
for d in range(288):
    for i in range(3):
        for j in range(4):
            p[d][i][j] = p[d][i][j]/p[d][i][3]

#%%
# 設定 x 座標資料
x = [str(hr)+':0'+str(m*5) if m<2 else str(hr)+':'+str(m*5) for hr in range(24) for m in range(12) ]

# 設定 y 座標資料
y1B = p[:, 0, 0]
y1G = p[:, 0, 1]
y1S = p[:, 0, 2]

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] # 將字體設定為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False             # 用來正常顯示負號

# 設定畫布，一定要在 plot() 函數前先設定
plt.figure(figsize=(12, 4.8), dpi=500)
# figsize：圖表的寬與高(單位英吋)，dpi:圖表解析度，facecolor:圖表底色，edgecolor:圖表邊框色
# figsize=(8, 4.8), dpi=100

# 設定圖表標題
plt.title('各時段營運狀態趨勢', fontsize=20)

# 設定坐標軸標題
plt.xlabel('時段', fontsize=14, labelpad=7)    
plt.ylabel('指\n標', fontsize=14, rotation=0, labelpad=16)

# 將資料帶入圖表
plt.plot(x, y1G, 'g--', label='G 可靠度')
plt.plot(x, y1B, 'b', label='B 缺車風險')
plt.plot(x, y1S, ':', label='S 缺位風險', color='brown')


# 設定x軸與y軸的刻度
xticks = x.copy()
for i in range(len(xticks)):
    if not int(xticks[i][-2:]) % 30 == 0:
        xticks[i] = ''
plt.xticks(xticks, rotation=90)
plt.yticks([i*.1 for i in range(11)], fontsize=14)

# 設定y軸顯示範圍
plt.ylim(0, .93)

# 設定格線顏色、種類、寬度
plt.grid(color='lightgray', linestyle='--', linewidth=.5)   

# 設定圖例
plt.legend()
# loc='upper left'

plt.show()

# plt.savefig('.png')
#%%
# 平日
# 設定 x 座標資料
x = [str(hr)+':0'+str(m*5) if m<2 else str(hr)+':'+str(m*5) for hr in range(24) for m in range(12) ]

# 設定 y 座標資料
y1Bw = p[:, 1, 0]
y1Gw = p[:, 1, 1]
y1Sw = p[:, 1, 2]

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] # 將字體設定為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False             # 用來正常顯示負號

# 設定畫布，一定要在 plot() 函數前先設定
plt.figure(figsize=(12, 4.8), dpi=500)
# figsize：圖表的寬與高(單位英吋)，dpi:圖表解析度，facecolor:圖表底色，edgecolor:圖表邊框色
# figsize=(8, 4.8), dpi=100

# 設定圖表標題
plt.title('「平日」各時段營運狀態趨勢', fontsize=20)

# 設定坐標軸標題
plt.xlabel('時段', fontsize=14, labelpad=7)    
plt.ylabel('指\n標', fontsize=14, rotation=0, labelpad=16)

# 將資料帶入圖表
plt.plot(x, y1Gw, 'g--', label='G 可靠度')
plt.plot(x, y1Bw, 'b', label='B 缺車風險')
plt.plot(x, y1Sw, ':', label='S 缺位風險', color='brown')


# 設定x軸與y軸的刻度
xticks = x.copy()
for i in range(len(xticks)):
    if not int(xticks[i][-2:]) % 30 == 0:
        xticks[i] = ''
plt.xticks(xticks, rotation=90)
plt.yticks([i*.1 for i in range(11)], fontsize=14)

# 設定y軸顯示範圍
plt.ylim(0, .93)

# 設定格線顏色、種類、寬度
plt.grid(color='lightgray', linestyle='--', linewidth=.5)   

# 設定圖例
plt.legend()
# loc='upper left'

plt.show()
#%%
# 假日

# 設定 x 座標資料
x = [str(hr)+':0'+str(m*5) if m<2 else str(hr)+':'+str(m*5) for hr in range(24) for m in range(12) ]

# 設定 y 座標資料
y1Bh = p[:, 2, 0]
y1Gh = p[:, 2, 1]
y1Sh = p[:, 2, 2]

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] # 將字體設定為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False             # 用來正常顯示負號

# 設定畫布，一定要在 plot() 函數前先設定
plt.figure(figsize=(12, 4.8), dpi=500)
# figsize：圖表的寬與高(單位英吋)，dpi:圖表解析度，facecolor:圖表底色，edgecolor:圖表邊框色
# figsize=(8, 4.8), dpi=100

# 設定圖表標題
plt.title('「假日」各時段營運狀態趨勢', fontsize=20)

# 設定坐標軸標題
plt.xlabel('時段', fontsize=14, labelpad=7)    
plt.ylabel('指\n標', fontsize=14, rotation=0, labelpad=16)

# 將資料帶入圖表
plt.plot(x, y1Gh, 'g--', label='G 可靠度')
plt.plot(x, y1Bh, 'b', label='B 缺車風險')
plt.plot(x, y1Sh, ':', label='S 缺位風險', color='brown')


# 設定x軸與y軸的刻度
xticks = x.copy()
for i in range(len(xticks)):
    if not int(xticks[i][-2:]) % 30 == 0:
        xticks[i] = ''
plt.xticks(xticks, rotation=90)
plt.yticks([i*.1 for i in range(11)], fontsize=14)

# 設定y軸顯示範圍
plt.ylim(0, .93)

# 設定格線顏色、種類、寬度
plt.grid(color='lightgray', linestyle='--', linewidth=.5)   

# 設定圖例
plt.legend()
# loc='upper left'

plt.show()