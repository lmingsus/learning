import requests as rq
import pandas as pd

# 取得2023下半年的假日日期

# api 網址
url = 'https://data.ntpc.gov.tw/api/datasets/308dcd75-6434-45bc-a95f-584da4fed251/json?page={}&size=500'

# 設定 DataFrame
df = pd.DataFrame(columns=['date', 'isholiday'])
# 注意：欄位'isholiday'會有「否」，例如：星期六的補行上班日，故列入欄位備用

for page in range(0, 4):
    # 取得所有內容
    content = rq.request('get', url.format(page))
    json_data = content.json()      # type: list
    
    # json_data[0] 為：
    # {'date': '2021/4/25',
    #  'chinese': '',
    #  'isholiday': '是',
    #  'holidaycategory': '星期六、星期日',
    #  'description': ''}
    
    
    # 由於該 json 依日期排列，故設定開始點：gotodf
    gotodf = False
    for day in json_data:
        
        if day['year'] == '2023':    # 開始點
            gotodf = True
        elif day['year'] == '2024':
            # 2024結束點，直接 break
            break
        
        if gotodf:
            date = day["date"][4:]
            
            # 轉換為 bool值
            if day['isholiday'] == '是':
                isholiD = True
            else:
                isholiD = False
            
            # 放進 DateFrame
            df = pd.concat([df, pd.DataFrame([[date, isholiD]], columns=df.columns)],
                         ignore_index=True)

# 匯出
df.to_csv('isholiday2023.csv', index=0)

        