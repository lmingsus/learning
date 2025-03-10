import os
import json
import random
import urllib.parse

from show_exhi import show_list


def bubb_temp(img_url, firm_url, firm_name, firm_loca, firm_id) -> dict:
    # 對中文 firm_loca 進行 URL 編碼
    encoded_firm_loca = urllib.parse.quote(firm_loca.replace(' ', '').replace('、', ''))

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
                "uri": firm_url
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": firm_name,
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
                                    "text": firm_loca,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        # {
                        #     "type": "box",
                        #     "layout": "baseline",
                        #     "spacing": "sm",
                        #     "contents": [
                        #         {
                        #             "type": "icon",
                        #             "url": "https://png.pngtree.com/element_our/20190531/ourmid/pngtree-clock-time-icon-image_1287819.jpg",
                        #             "size": "lg"
                        #         },
                        #         {
                        #             "type": "text",
                        #             "text": firm_date,
                        #             "wrap": True,
                        #             "color": "#666666",
                        #             "size": "sm",
                        #             "flex": 5
                        #         }
                        #     ]
                        # }
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
                        "uri": firm_url
                    }
                },
                {
                    "type": "button",
                    "style": "secondary", # 顯示為次要按鈕
                    # "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "帶我趣",
                        "data": f"bring_me_to@@@@@{firm_id}"
                    }
                },
                # {
                #     "type": "button",
                #     "style": "secondary", # 顯示為次要按鈕
                #     "height": "sm",
                #     "action": {
                #         "type": "postback",
                #         "label": "查看參展廠商",
                #         "data": f"show_shop@@@@@{firm_id}"
                #     }
                # },
                {
                    "type": "button",
                    "style": "primary", # 顯示為主要按鈕
                    "action": {
                        "type": "postback",
                        "label": "加到我的最愛",
                        "data": f"add_love_firm@@@@@{firm_id}",
                        "displayText": f"我喜歡「{firm_name}」！"
                    }
                }
            ],
            "flex": 0
        }
    }
    # label: 按鈕上的文字
    # "displayText": 發送到聊天視窗上的文字
    # return json.dumps(bubble) # 轉換成 json 格式
    return bubble


def show_firm(love_firm: list = list()) -> dict:
    '''
    產生一個 carousel ，格式為 dict，裡面包含最多 12 個廠商的資訊
    params:
        love_firm: list, 使用者收藏的展覽 id
    return:
        dict, carousel
    '''
    file_path_list = list()
    file_index_list = list()
    if love_firm == []:
        # 讀取json，廠商的資訊，並隨機挑選 5 個廠商
        path = r"static\exp241230"
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                file_path = os.path.join(path, filename)
                # print(file_path)

                file_path_list.append(file_path)
        
        file_path_list = random.sample(file_path_list, 5)
    elif isinstance(love_firm, str):
        file_path_list.append("static\\exp241230\\" + love_firm.split('_')[0])
        file_index_list.append(int(love_firm.split('_')[1]))
    else:
        for firm_id in love_firm:
            print("firm_id 是", firm_id)
            file_path_list.append("static\\exp241230\\" + firm_id.split('_')[0])
            file_index_list.append(int(firm_id.split('_')[1]))


    # contents 為 bubble 的 list，每個 bubble 代表一個展覽
    contents = []
    for file_path in file_path_list:

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                firms_data = json.load(f)
        except Exception as e:
            print(f"Error reading .json: {e}")
            return {"message": "Error reading .json"}

        if love_firm != []:
            # 如果有最愛廠商，則firm為該廠商
            firm  = firms_data[file_index_list[file_path_list.index(file_path)]]
        else:
            # 如果沒有，隨機挑選一個廠商
            firm = firms_data[random.randint(1, len(firms_data)-1)]

        # 檢查 name 是否是 None
        if firm.get('name', None) is None:
            firm['name'] = '展覽名稱待更新'

        # 檢查 location (在 firms_data[0] ) 是否是 None
        if firms_data[0] is None:
            firms_data[0] = '展覽地點待更新'

        # 檢查 logo 是否是 None
        if firm.get('logo', None) is None:
            firm['logo'] = 'https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png'
        elif firm['logo'].startswith('www'):
            firm['logo'] = 'https://' + firm['logo']
        elif not firm['logo'].startswith('http'):
            firm['logo'] = 'https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png'
        
        # 檢查 url 是否是 None
        if firm.get('url', None) is None:
            firm_name_urllib = urllib.parse.quote(firm['name'].replace(' ', '').replace('、', ''))
            firm['url'] = 'https://www.google.com.tw/search?q=' + firm_name_urllib
        elif firm['url'].startswith('www'):
            firm['url'] = 'https://' + firm['url']
        elif firm['url'] == "":
            print("firm['url'] 是空的字串")
            firm_name_urllib = urllib.parse.quote(firm['name'].replace(' ', '').replace('、', ''))
            firm['url'] = 'https://www.google.com.tw/search?q=' + firm_name_urllib

        
        # 暫時將 firm_id 設為這個形式，之後須修改。
        flle_id = file_path.split('\\')[-1] + '_' + str(firms_data.index(firm))
        
        # todo: 檢查 check 是否是 True

        # 產生 bubble 的 str
        # firm_str = bubb_temp(firm['logo'], firm['url'], firm['name'], firms_data[0], flle_id)
        # 產生 bubble 的 dict
        contents.append(bubb_temp(firm['logo'], firm['url'], firm['name'], firms_data[0], flle_id))
        print(firm['logo'])
        print(firm['url'])
        print(firm['name'])
        print(firms_data[0]) # 展覽名稱
        print(flle_id)
        print("=========")

        # contents.append(json.loads(firm_str))

    # 產生 carousel 的 dict
    # car_dict = {"type": "carousel", "contents":contents}
    return {"type": "carousel", "contents":contents}


def list_bubble(firm_list: list) -> dict:
    '''
    產生一個 list_bubble，格式為 dict
    params:
        firm_list: list, 元素為dict，使用者收藏的展覽資訊：name、id_add
    return:
        dict, list_bubble
    '''
    contents = list()
    # colors = ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE']
    for firm in firm_list:
        temp_dict = {
                      "type": "text",
                      "text": firm['name'],
                      # "align": "center",
                      "margin": "lg",
                      "size": "lg",
                      "color": "#0066cc",
                      # "color": colors[firm_list.index(firm) % len(colors)],
                      "action": {
                        "type": "postback",
                        "label": "action",
                        "data": "show_firm@@@@@" + firm['id_add']
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
            "text": "LOVE FIRM",
            "weight": "bold",
            "color": "#1DB446",
            "size": "md"
          },
          {
            "type": "text",
            "text": "我的最愛廠商清單",
            "weight": "bold",
            "size": "xxl",
            "margin": "xs"
          },
          {
            "type": "text",
            "text": "可點擊廠商名稱查看詳細資訊",
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


def show_list_firm(love_firm: list) -> dict:
    '''
    為了 show 出 list_bubble，為了讓使用者查看自己收藏的展覽
    拿到 廠商 id ，並從 資料夾 中找出對應的檔案和廠商資訊，
    再將展覽名稱與 展覽 id 放入 list_bubble 中，
    並回傳 dict 格式的 bubble
    params:
        love_firm: list, 使用者收藏的展覽 id
    return:
        dict, list_bubble
    '''

    firm_list = list()
    # 讀取展覽資料
    for firm_id in love_firm:
        firm_path = "static\\exp241230\\" + firm_id.split('_')[0]
        firm_index = int(firm_id.split('_')[1])
        try:
            with open(firm_path, 'r', encoding='utf-8') as f:
                firm_data = json.load(f)
        except Exception as e:
            print(f"Error reading .json: {e}")

        firm = firm_data[firm_index]

        # 檢查 name 是否是 None
        if firm.get('name', None) is None:
            firm['name'] = '展覽名稱待更新'
        
        firm_list.append({'name': firm['name'], 'id_add': firm_id})

    return list_bubble(firm_list)

def show_both(love_exhi, love_firm) -> dict:
    '''
    顯示兩個 bubble
    params:
        bubble1: dict, bubble
        bubble2: dict, bubble
    return:
        dict, carousel
    '''
    bubble1 = show_list(love_exhi)
    bubble2 = show_list_firm(love_firm)
    return {"type": "carousel", "contents": [bubble1, bubble2]}




if __name__ == '__main__':
    import requests
    import time
    # print(show_love_firm())
    # print(type(show_love_firm()))

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
        encoded_firm_loca = urllib.parse.quote(h['location'].replace(' ', ''))
        print(f"https://www.google.com.tw/maps/search/?api=1&query={encoded_firm_loca}")
        # r = requests.get(f"https://www.google.com.tw/maps/search/?api=1&query={h['location'].replace(' ', '')}")
        # print(r.status_code)

        print("=========")
