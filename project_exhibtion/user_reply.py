import os
import json
from configparser import ConfigParser
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    PostbackAction,
    QuickReply,
    QuickReplyItem,
    TextMessage,
)

from qr_type import exhibitions, make_quick_reply_exhi
from show_exhi import show_exhi, show_list
from show_firm import show_firm, show_list_firm, show_both
from richmenu0103 import rich_menu_set


# 載入環境變數
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    ADMINISTRATOR_SECRET = config.get('LINE', 'ADMINISTRATOR_SECRET')
except:
    print('載入環境變數 ADMINISTRATOR 密碼失敗')



def user_reply(user_history, event, configuration):
    user_id = event.source.user_id
    user_input = event.message.text.strip()

    user_status = user_history["users"][user_id]["status"]

    if user_status == "want_to_be_Admin":
        # 如果使用者輸入的是 Administrator 密碼
        if user_input == ADMINISTRATOR_SECRET:
            user_history["Administrator"].append(user_id)
            user_history["users"][user_id]["status"] = None
            reply_message = [TextMessage(text="您已進入管理模式。")]
        else:
            user_history["users"][user_id]["status"] = None
            reply_message = [TextMessage(text="密碼錯誤！")]
        user_history["users"][user_id]["status"] = None

    elif user_status == "search_exhibition_by_keyword":
        # 搜尋展覽
        reply_message = [TextMessage(text="尚未開放搜尋功能！")]

    elif user_status is not None:
        if user_status.split("@@@@@")[0] == "bring_me_to":
            # 已接收 user_input = 起點，接下來要傳送地圖
            if user_input == "取消":
                user_history["users"][user_id]["status"] = None
                reply_message = [TextMessage(text="帶我趣已取消！")]
            else:
                frim_id = user_status.split("@@@@@")[1]
                user_history["users"][user_id]["status"] = None # 結束導航，重置使用者狀態
                reply_message = [TextMessage(text=f"你的起點是：{user_input}\n你的目的地是：{frim_id}\n\n導航功能尚未開放！")]

    elif user_input == 'Administrator':
        # want to be Administrator
        if user_id in user_history["Administrator"]:
            user_history["Administrator"].remove(user_id)
            reply_message = [TextMessage(text="您已退出管理模式。")]
        elif user_id in user_history["Super_Administrator"] and user_id not in user_history["Administrator"]:
            user_history["Administrator"].append(user_id)
            reply_message = [TextMessage(text="您已進入管理模式。")]
        elif user_id not in user_history["Administrator"]:
            user_history["users"][user_id]["status"] = "want_to_be_Admin"
            reply_message = [TextMessage(text="請輸入密碼：")]

    elif user_input == '查看 event':
        # 查看 line event
        reply_message = list()
        for item in list(event)[0:-1]:
            reply_message.append(item[0] + ":\n" + str(item[1]))
            print(item[0], item[1], sep=":\n")
        reply_message = "\n\n".join(reply_message)
        reply_message += "\n\nmessage:"
        for item in event.message:
            reply_message += f"\n\n{item[0]}: {str(item[1])}"
            print(item[0], item[1], sep=":\n")
        reply_message = [TextMessage(text=reply_message)]

    elif user_input == 'exh':
        # 測試展覽，可刪除

        with open(os.path.join(os.path.dirname(__file__), 'car_exh_1223.json'), 'r', encoding='utf-8') as f:
            exh_json = json.load(f)
            exh_json_str = json.dumps(exh_json, ensure_ascii=False, indent=4)
            # print(exh_json_str)
        
        reply_message = [FlexMessage(alt_text="hello", contents=FlexContainer.from_json(exh_json_str))]


    elif user_input == 'exh2':
        # 測試展覽2

        reply_message = [
            TextMessage(text="來趣看展覽！\n隨機挑選\n請選擇您感興趣的展覽："),
            FlexMessage(alt_text="隨機展覽", contents=FlexContainer.from_dict(show_exhi()))
        ]


    elif user_input == 'show love exh':
        # 顯示我的最愛展覽

        love_exhi = user_history["users"][user_id]["love_exhi"]
        if len(love_exhi) == 0:
            reply_message = [TextMessage(text="您尚未加入任何展覽至我的最愛！")]
        else:
            reply_message = [
            TextMessage(text="這些是您感興趣的展覽："),
            FlexMessage(alt_text="我的最愛展覽", contents=FlexContainer.from_dict(show_exhi(love_exhi)))
        ]
    

    elif user_input == 'show love exh list':
        # 顯示我的最愛展覽 - 列表

        love_exhi = user_history["users"][user_id]["love_exhi"]
        if len(love_exhi) == 0:
            reply_message = [TextMessage(text="您尚未加入任何展覽至我的最愛！")]
        else:
            reply_message = [
                FlexMessage(alt_text="我的最愛展覽清單", contents=FlexContainer.from_dict(show_list(love_exhi)))
            ]


    elif user_input == 'show all exh':
        # 顯示「所有」展覽 - 列表

        try:
            with open('static/checked/kuei_20241229_0045.json', 'r', encoding='utf-8') as f:
                kuei_dict = json.load(f)
        except Exception as e:
            kuei_dict = {"message": "Error reading kuei.json"}
            print(f"Error reading kuei.json: {e}")
        
        exh_id_list = [exh["id_add"] for exh in kuei_dict]

        reply_message = [
            TextMessage(text="這些是所有的展覽："),
            FlexMessage(alt_text="所有展覽",
                        contents=FlexContainer.from_dict(show_list(exh_id_list)))
        ]


    elif user_input == 'shop':
        # 測試商店，可刪除
        with open(os.path.join(os.path.dirname(__file__), 'car_shop_1223.json'), 'r', encoding='utf-8') as f:
            shop_json = json.load(f)
            shop_json_str = json.dumps(shop_json, ensure_ascii=False, indent=4)
            # print(shop_json_str)
        
        reply_message = [FlexMessage(alt_text="hello", contents=FlexContainer.from_json(shop_json_str))]
    

    elif user_input == 'firms':
        # 測試商家 - 隨機挑選 5 家
        
        reply_message = [FlexMessage(alt_text="隨機廠商資料", contents=FlexContainer.from_dict(show_firm()))]


    elif user_input == 'love firms':
        # 顯示我的最愛廠商

        love_firms = user_history["users"][user_id]["love_firm"]
        
        reply_message = [FlexMessage(alt_text="我的最愛廠商資料", contents=FlexContainer.from_dict(show_firm(love_firms)))]


    elif user_input == 'show love firm list':
        # 顯示我的最愛廠商 - 列表

        love_firm = user_history["users"][user_id]["love_firm"]
        if len(love_firm) == 0:
            reply_message = [TextMessage(text="您尚未加入任何廠商至我的最愛！")]
        else:
            reply_message = [
                FlexMessage(alt_text="我的最愛展覽清單", contents=FlexContainer.from_dict(show_list_firm(love_firm)))
            ]


    elif user_input == 'show both':
        # 顯示我的最愛展覽、廠商

        love_exhi = user_history["users"][user_id]["love_exhi"]
        love_firm = user_history["users"][user_id]["love_firm"]

        if len(love_exhi) == 0 and len(love_firm) == 0:
            reply_message = [TextMessage(text="您尚未加入任何展覽或廠商至我的最愛！")]
        elif len(love_exhi) == 0:
            reply_message = [FlexMessage(alt_text="我的最愛廠商清單", contents=FlexContainer.from_dict(show_list_firm(love_firm)))]
        elif len(love_firm) == 0:
            reply_message = [FlexMessage(alt_text="我的最愛展覽清單", contents=FlexContainer.from_dict(show_list(love_exhi)))
            ]
        else:
            reply_message = [
                # FlexMessage(alt_text="我的最愛展覽清單", contents=FlexContainer.from_dict(show_list(love_exhi))),
                # FlexMessage(alt_text="我的最愛廠商清單", contents=FlexContainer.from_dict(show_list_firm(love_firm)))
                FlexMessage(alt_text="我的最愛展覽、廠商清單", contents=FlexContainer.from_dict(show_both(love_exhi, love_firm)))
            ]

    elif user_input == 'quick':
        # 進入 quick reply 選擇「喜歡展覽種類」

        print("進入 quick")
        fav_exhi = user_history["users"][user_id]["favorite"]
        # print("這裡是 fav_exhi：", fav_exhi)

        # if len(fav_exhi) == 0:
        #     # 如果還沒選擇展覽，fav_exhi = []，則顯示所有展覽
        #     quick_reply = make_quick_reply_exhi()
        if len(fav_exhi) == len(exhibitions):
            quick_reply = QuickReply(items=[
                QuickReplyItem(
                    action=PostbackAction(label="重新選擇", data="remove_all_fav"))]
                )
        else:
            quick_reply = make_quick_reply_exhi(fav_exhi)

        reply_message = [TextMessage(text="來趣看展覽！\n請選擇您感興趣的展覽種類：", 
                                    quick_reply=quick_reply)]
    
    elif user_input == '重製quick':
        user_history["users"][user_id]["favorite"] = []
        quick_reply = make_quick_reply_exhi()
        reply_message = [TextMessage(text="已重製您的展覽選擇！\n請選擇您感興趣的展覽種類：", 
                                    quick_reply=quick_reply)]
        

    elif user_input.strip() == 'richmenuset':
        # 設定 Rich Menu
        if user_id in user_history["Administrator"]:
            rich_menu_set(configuration)
            reply_message = [TextMessage(text="Rich menu set!")]
        else:
            reply_message = [TextMessage(text="You are not Administrator!")]

    elif user_input == '熊大在嗎？':
        # 測試用
        reply_message = [TextMessage(text="我在，有什麼事？", 
                                     sender={"name": "熊大", 
                                             "iconUrl": "https://4.bp.blogspot.com/-x-fowV0tZAo/WohU6444rGI/AAAAAAAAFGk/_0_40Tx3-hc1yQLlwIKJ19cJDlRwcL6MgCKgBGAs/s1600/03.jpg"},
                                     quoteToken=event.message.quote_token,
                                     )]
    
    elif user_input == '熊大？':
        # 測試用
        reply_message = [TextMessage(text="我在？", 
                                        sender={"name": "熊大", 
                                                "iconUrl": "https://4.bp.blogspot.com/-x-fowV0tZAo/WohU6444rGI/AAAAAAAAFGk/_0_40Tx3-hc1yQLlwIKJ19cJDlRwcL6MgCKgBGAs/s1600/03.jpg"},
                                        quoteToken=event.message.quote_token
                                        )]

    else:
        personalized_message = f"Hello {user_id}, you said: {user_input}"
        reply_message = [TextMessage(text=personalized_message)]
    
    return reply_message, user_history

