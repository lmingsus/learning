
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
)

from qr_type import exhibitions, make_quick_reply_exhi, recommend_like_or_not
from show_exhi import show_exhi, show_list
from show_firm import show_firm, show_list_firm, show_both


def postback_reply(event, user_history):
    """
    Postback 回覆
    """

    user_id = event.source.user_id

    # 如果 data 有 @@@@@，則分開 data_stat 和 data，data為 id
    data_orgin = event.postback.data
    data = data_orgin.split("@@@@@")[1] if "@@@@@" in data_orgin else data_orgin
    data_stat = data_orgin.split("@@@@@")[0] if "@@@@@" in data_orgin else None

    if data_orgin.startswith("show_both"):
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

    elif data_orgin.startswith("add_love_firm"):
        # 將廠商加入我的最愛
        love_firm = user_history["users"][user_id]["love_firm"]
        # add_time = event.timestamp # 加入時間，之後 list 變成 dict 再加入時間
        if data not in love_firm:
            love_firm.append(data)
            reply_message = [TextMessage(text="已加入我的最愛！")]
        else:
            # 將已經在我的最愛裡的廠商移到 list 最後面
            love_firm.remove(data)
            love_firm.append(data)
            reply_message = [TextMessage(text="這個廠商已經在我的最愛裡了！")]
    

    elif data_orgin.startswith("show_firm"):
        # 顯示廠商詳細資訊
        print("這裡是 data：", data)
        reply_message = [FlexMessage(alt_text="廠商資訊", contents=FlexContainer.from_dict(show_firm(data)))]
    
    elif data_orgin.startswith("add_love_exhib"):
        # 將展覽加入我的最愛
        love_exhi = user_history["users"][user_id]["love_exhi"]
        # add_time = event.timestamp # 加入時間，之後 list 變成 dict 再加入時間
        if data not in love_exhi:
            love_exhi.append(data)
            reply_message = [TextMessage(text="已加入我的最愛！")]
        else:
            # 將已經在我的最愛裡的展覽移到 list 最後面
            love_exhi.remove(data)
            love_exhi.append(data)
            reply_message = [TextMessage(text="這個展覽已經在我的最愛裡了！")]
    
    elif data_orgin.startswith("bring_me_to"):
        # 帶我去攤位
        user_history["users"][user_id]["status"] = "bring_me_to_01" + "@@@@@" + data
        reply_message = [TextMessage(text="帶我趣～～\n請輸入你現在附近的攤位名稱：\n離開請輸入「取消」。")]
    

    elif data_orgin.startswith("show_exhib"):
        # 顯示展覽詳細資訊
        print("這裡是 show_exhib 的 data：", data)
        reply_message = [FlexMessage(alt_text="展覽資訊", contents=FlexContainer.from_dict(show_exhi(data)))]
    

    elif data_orgin == 'recommend':
        # 搜尋展覽
        reply_text = "這裡是推薦展覽的功能！"
        reply_message = [TextMessage(text=reply_text),
                         FlexMessage(alt_text="隨機展覽", contents=FlexContainer.from_dict(show_exhi())),
                         FlexMessage(alt_text="隨機廠商", contents=FlexContainer.from_dict(show_firm())),
                         TextMessage(text="先隨機抓幾個展覽和廠商給你看！",
                                     quick_reply=recommend_like_or_not()),
                        ]


    elif data_orgin == 'search':
        # 搜尋展覽
        reply_text = "請輸入您想搜尋的展覽關鍵字：\n這裡是搜尋展覽的功能！\n但現在還沒有:)"
        user_history["users"][user_id]["status"] = "search_exhibition_by_keyword"
        reply_message = [TextMessage(text=reply_text)]


    elif data_orgin == 'quick':
        # 進入 quick reply 選擇「喜歡展覽種類」

        print("進入 quick")
        fav_exhi = user_history["users"][user_id]["favorite"]

        if len(fav_exhi) == len(exhibitions):
            quick_reply = QuickReply(items=[
                QuickReplyItem(
                    action=PostbackAction(label="重新選擇", data="remove_all_fav"))]
                )
        else:
            quick_reply = make_quick_reply_exhi(fav_exhi)

        reply_message = [TextMessage(text="來趣看展覽！\n請選擇您感興趣的展覽種類：", 
                                    quick_reply=quick_reply)]
    
    elif data == "remove_all_fav":
        # 展覽種類重置
        user_history["users"][user_id]["favorite"] = []
        reply_text = "已重製您的展覽選擇！\n請選擇您感興趣的展覽種類："
        reply_message = [TextMessage(text=reply_text, 
                                    quick_reply=make_quick_reply_exhi())]
    


    elif data in exhibitions:
        # 選擇展覽種類

        reply_text = f"你喜歡{exhibitions[data]}！\n收到type為：{data}"
        print("這裡是 reply_text：", reply_text)
        if data not in user_history["users"][user_id]["favorite"]:
            user_history["users"][user_id]["favorite"].append(data)
        
        if len(user_history["users"][user_id]["favorite"]) == len(exhibitions):
            reply_text += "\n你已經選擇了所有展覽！"
            reply_message = [TextMessage(text=reply_text)]
        else:
            reply_message = [
                FlexMessage(alt_text="展覽資訊", contents=FlexContainer.from_dict(show_exhi())),
                TextMessage(text=reply_text, 
                            # quick_reply=make_quick_reply_exhi(user_history["users"][user_id]["favorite"])
                            )
                            ]
    
    
    else:
        reply_text = "這個 postback 目前不存在！"
        reply_text += f"\n以下是 data 部分：\n{data}"
        print("這裡是 reply_text：", reply_text)
        reply_message = [TextMessage(text=reply_text)]
    
    return reply_message, user_history