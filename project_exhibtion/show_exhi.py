import json
import random
import urllib.parse


def bubb_temp(img_url, exhi_url, exhi_name, exhi_loca, exhi_date, exhi_id):
    # 對中文 exhi_loca 進行 URL 編碼
    encoded_exhi_loca = urllib.parse.quote(exhi_loca.replace(' ', '').replace('、', ''))

    bubble = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": exhi_url.replace(' ', '')
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": exhi_name,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://png.pngtree.com/element_our/20190530/ourmid/pngtree-cartoon-navigation-icon-download-image_1251411.jpg",
                                    "position": "relative"
                                },
                                {
                                    "type": "text",
                                    "text": exhi_loca,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://png.pngtree.com/element_our/20190531/ourmid/pngtree-clock-time-icon-image_1287819.jpg",
                                    "size": "lg"
                                },
                                {
                                    "type": "text",
                                    "text": exhi_date,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary", # 顯示為次要按鈕
                    # "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "官方網站",
                        "uri": exhi_url.replace(' ', '')
                    }
                },
                {
                    "type": "button",
                    "style": "secondary", # 顯示為次要按鈕
                    # "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "展覽位置",
                        "uri": f"https://www.google.com.tw/maps/search/?api=1&query={encoded_exhi_loca}"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary", # 顯示為次要按鈕
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "店家推薦",
                        "data": f"show_shop@@@@@{exhi_id}"
                    }
                },
                {
                    "type": "button",
                    "style": "primary", # 顯示為主要按鈕
                    "action": {
                        "type": "postback",
                        "label": "加到我的最愛",
                        "data": f"add_love_exhib@@@@@{exhi_id}",
                        "displayText": f"我喜歡「{exhi_name}」！"
                    }
                }
            ],
            "flex": 0
        }
    }
    # return json.dumps(bubble) # 轉換成 json 格式
    # label: 按鈕上的文字
    # "displayText": 發送到聊天視窗上的文字
    return bubble


def show_exhi(love_exhi: list = list()) -> dict:
    '''
    產生一個 carousel ，格式為 dict，裡面包含最多 12 個展覽的資訊
    params:
        love_exhi: list, 使用者收藏的展覽 id
    return:
        dict, carousel
    '''
    
    try:
        with open('static/checked/kuei_20241229_0045.json', 'r', encoding='utf-8') as f:
            kuei_dict = json.load(f)
    except Exception as e:
        kuei_dict = {"message": "Error reading kuei.json"}
        print(f"Error reading kuei.json: {e}")
        return kuei_dict
    
    if love_exhi == []:
        # 如果 love_exhi 是空的，則從 kuei_dict 隨機挑選 5 個展覽

        exhi_list = random.sample(kuei_dict, 5)
    else:
        # 從 love_exhi 中挑選展覽，最多只能有 12 個展覽
        exhi_list = []
        for exhi in kuei_dict:
            if exhi['id_add'] in love_exhi:
                exhi_list.append(exhi)
                if len(exhi_list) == 12: # 最多只能有 12 個展覽
                    break
    
    # contents 為 bubble 的 list，每個 bubble 代表一個展覽
    contents = []
    for exhi in exhi_list:
        # 檢查 name 是否是 None
        if exhi.get('name', None) is None:
            exhi['name'] = '展覽名稱待更新'
        
        # 檢查 date 是否是 None
        if exhi.get('date', None) is None:
            exhi['date'] = '展覽時間待更新'

        # 檢查 location 是否是 None
        if exhi.get('location', None) is None:
            exhi['location'] = '展覽地點待更新'

        # 檢查 logo 是否是 None
        if exhi.get('logo', None) is None:
            exhi['logo'] = 'https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png'
        
        # 檢查 url 是否是 None
        if (url_list := exhi.get('url', None)):
            if url_list[1] != '':
                exhi['url'] = url_list[1]
            elif url_list[0] != '':
                exhi['url'] = url_list[0]
            else:
                exhi['url'] = 'https://www.google.com.tw/search?q=' + exhi['name'].replace(' ', '').replace('、', '')
        
        
        # todo: 檢查 check 是否是 True

        exhi_str = bubb_temp(exhi['logo'], exhi['url'], exhi['name'], exhi['location'], exhi['date'], exhi['id_add'])

        contents.append(exhi_str)

    # 產生 carousel 的 dict
    # car_dict = {"type": "carousel", "contents":contents}
    return {"type": "carousel", "contents":contents}


def list_bubble(exhi_list: list) -> dict:
    contents = list()
    # colors = ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE']
    for exhi in exhi_list:
        temp_dict = {
                      "type": "text",
                      "text": exhi['name'],
                      # "align": "center",
                      "margin": "lg",
                      "size": "lg",
                      "color": "#0066cc",
                      # "color": colors[exhi_list.index(exhi) % len(colors)],
                      "action": {
                        "type": "postback",
                        "label": "action",
                        "data": "show_exhib@@@@@" + exhi['id_add']
                      }
                    }
        contents.append(temp_dict)
    bubble = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "LOVE EXHIB",
            "weight": "bold",
            "color": "#1DB446",
            "size": "md"
          },
          {
            "type": "text",
            "text": "我的最愛展覽清單",
            "weight": "bold",
            "size": "xxl",
            "margin": "xs"
          },
          {
            "type": "text",
            "text": "可點擊展覽名稱查看詳細資訊",
            "size": "sm",
            "color": "#aaaaaa",
            "wrap": True
          },
          {
            "type": "separator",
            "margin": "lg"
          },
          {
            "type": "box",
            "layout": "vertical",
            # "margin": "xxl",
            "spacing": "sm",
            "contents": contents
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          # {
          #   "type": "box",
          #   "layout": "horizontal",
          #   "margin": "md",
          #   "contents": [
          #     {
          #       "type": "text",
          #       "text": "PAYMENT ID",
          #       "size": "xs",
          #       "color": "#aaaaaa",
          #       "flex": 0
          #     },
          #     {
          #       "type": "text",
          #       "text": "#743289384279",
          #       "color": "#aaaaaa",
          #       "size": "xs",
          #       "align": "end"
          #     }
          #   ]
          # }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return bubble


def show_list(love_exhi: list) -> dict:
    '''
    為了 show 出 list_bubble，為了讓使用者查看自己收藏的展覽
    拿到 展覽 id ，並從 kuei_dict 中找出對應的展覽名稱
    再將展覽名稱與 展覽 id 放入 list_bubble 中，
    並回傳 dict 格式的 bubble
    params:
        love_exhi: list, 使用者收藏的展覽 id
    return:
        dict, list_bubble
    '''
    # 讀取展覽資料為 kuei_dict
    try:
        with open('static/checked/kuei_20241229_0045.json', 'r', encoding='utf-8') as f:
            kuei_dict = json.load(f)
    except Exception as e:
        kuei_dict = {"message": "Error reading kuei.json"}
        print(f"Error reading kuei.json: {e}")
        return kuei_dict
    
    # 從 love_exhi 中挑選展覽（exhi為dict格式），成為 exhi_list 為欲輸出展覽的 list
    exhi_list = []
    for exhi in kuei_dict:
        if exhi['id_add'] in love_exhi:
            exhi_list.append(exhi)
            # if len(exhi_list) == 12: # 最多只能有 幾 個展覽？
            #     break
    # 刪減 exhi_list 裡的每個 dict 元素，僅保留 name 和 id_add
    exhi_list = [{'name': exhi['name'], 'id_add': exhi['id_add']} for exhi in exhi_list]
    
    for exhi in exhi_list:
        # 檢查 name 是否是 None
        if exhi.get('name', None) is None:
            exhi['name'] = '展覽名稱待更新'
        
        exhi = {'name': exhi['name'], 'id_add': exhi['id_add']}
    return list_bubble(exhi_list)




if __name__ == '__main__':
    import requests
    import time
    # print(show_love_exhi())
    # print(type(show_love_exhi()))

    # 讀取展覽資料
    try:
        with open('static/checked/kuei_20241229_0045.json', 'r', encoding='utf-8') as f:
            kuei_dict = json.load(f)
    except Exception as e:
        kuei_dict = {"message": "Error reading kuei.json"}
        print(f"Error reading kuei.json: {e}")
    
    for h in kuei_dict:
        # if (url_list := h.get('url', None)):
        #   if url_list[1] != '':
        #       h['url'] = url_list[1]
        #   elif url_list[0] != '':
        #       h['url'] = url_list[0]
        #   else:
        #       h['url'] = 'https://www.google.com.tw/search?q=' + h['name'].replace(' ', '')
        #       print("***************")
        # print(h['url'])
        # r = requests.get(h['url'])
        # print(r.status_code)
        # time.sleep(1)
        encoded_exhi_loca = urllib.parse.quote(h['location'].replace(' ', ''))
        print(f"https://www.google.com.tw/maps/search/?api=1&query={encoded_exhi_loca}")
        # r = requests.get(f"https://www.google.com.tw/maps/search/?api=1&query={h['location'].replace(' ', '')}")
        # print(r.status_code)

        print("=========")
