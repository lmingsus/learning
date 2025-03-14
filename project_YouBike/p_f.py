import pandas as pd
import time

# 將資料裁到每五分鐘一筆
# 檔案 p_{}.csv 轉換成 f_{}.csv

fp = r'p_{}.csv'

def five(df):
    df['label'] = 0
    
    for i in range(len(df)):
        n =  df.loc[i, 'time']
        hr = n // 100
        minute = n - hr*100
        m = minute // 5
        df.loc[i, 'label'] = hr*12 + m
        
    # 使用雙重 groupby 取得每組的第一筆索引
    idx_keep = df.groupby(['StationID', 'label']).head(1).index
    
    df = df.loc[idx_keep].reset_index(drop=True)
    
    df.drop('label', axis=1, inplace=True)
    
    return df

# day30 = ['0'+str(i) for i in range(1, 10)]
# day30 += [ str(i) for i in range(10, 31)]
# day31 = day30 + ['31']
# month = ['07', '08', '09', '10','11', '12']

mdlist = [str(1223-i) for i in range(8)]

try:
    for md in mdlist:
        start_time = time.time()
        
        dfc = pd.read_csv(fp.format(md))
        dfc = five(dfc)
        new_filename = 'f_' + md + '.csv'
        dfc.to_csv(new_filename, index=0)
        print('已完成：', new_filename)
        print('用', time.time()-start_time, '秒')
    
except Exception as e:
    print('錯誤：', e)