import os
import sys
import random
from flask import Flask, request, abort
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile # 建立臨時檔案和目錄，它可以在所有有支援的平臺上使用
# 此 module 所使用的檔名為一個隨機字元組成的字串，這讓檔案可以更安全地在共享的臨時目錄中被建立
import errno
import logging

# LINE
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    # StickerMessage,
    # ImageMessage,
    # LocationMessage,
    # VideoMessage,
    MessagingApiBlob,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    # CameraAction,
    # LocationAction,
    ButtonsTemplate,
    TemplateMessage,
    ClipboardAction,
)
from linebot.v3.webhooks import (
    # https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-kitchensink/app.py
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    # AudioMessageContent,
    # VideoMessageContent,
    PostbackEvent,
)

import configparser
import io, time 
# from IPython.display import Image # 只能取 local file

from gemini_m import gemini_mod
from ingred_list import add_to_json, choose_empty_ingred, add_ingred_contents


# 載入設定檔取得金鑰
config = configparser.ConfigParser()
config.read('config.ini')
try:
    CHANNEL_ACCESS_TOKEN = config['Line']['CHANNEL_ACCESS_TOKEN']
    CHANNEL_SECRET = config['Line']['CHANNEL_SECRET']
except KeyError as e:
    print("找不到金鑰：", e)
    sys.exit(1)


# 建立 flask app 物件
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
# app.wsgi_app：Flask 應用程式的 WSGI 中介軟體。這是一個 WSGI 應用程式，它將所有的請求和回應傳遞給 WSGI 中介軟體。
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app.logger.setLevel(logging.INFO)


# 設定 LINE 聊天機器人的基本資料
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# os.path.dirname(__file__)：取得目前檔案的路徑
# os.path.join 加上層層資料夾 '\\static\\tmp'

# function for create tmp dir for download content
# 建立暫存目錄
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            # 如果文件存在，則忽略
            pass
        else:
            raise


# v3
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


is_asking_ingredients = False
ingredientslist_str = str()
is_comparing_ingredients_1 = False
comparing_response_1 = str()
is_comparing_ingredients_2 = False
comparing_response_2 = str()

# v3
# 處理文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text  # event.message.text 為使用者輸入的文字
    print("收到文字訊息：", user_message)
    app.logger.info("取得文字訊息： %s", user_message)

    global is_asking_ingredients, ingredientslist_str
    global is_comparing_ingredients_1, is_comparing_ingredients_2
    global comparing_response_1, comparing_response_2

    with ApiClient(configuration) as api_client:
        # 建立 MessagingApi 實例
        line_bot_api = MessagingApi(api_client)
        
        if user_message == "@開始分析成分":
            is_asking_ingredients = True
            reply_messages = [TextMessage(text="請上傳圖片")]
            
        elif user_message == "@AI分析成分":
            prompt = "這是一份食品的成分：\n" + ingredientslist_str
            prompt += "。請分析這份物品的成分，在每一項成分的下一行新增以20字以內的正體中文簡短說明是否有益或有害，並在最後以30字以內簡短總結是否推薦。"
            response = gemini_mod([prompt])
            reply_messages = [TextMessage(text=response.text)]

        elif user_message == "@開始比較成分":
            is_comparing_ingredients_1 = True
            reply_messages = [TextMessage(text="請上傳第一張圖片")]

        elif user_message == "@顯示比較結果":
            prompt = "這是第一張圖片的成分：\n" + comparing_response_1 
            prompt += "。這是第二張圖片的成分：\n" + comparing_response_2
            prompt += "。請比較這兩張圖片的成分，考慮到不同國家的標示法規後，判斷並以正體中文回答是否相同以及有無刻意違法缺漏。"
            response = gemini_mod([prompt])
            reply_messages = [TextMessage(text=response.text)]

        elif user_message == "@功能選單":
            buttons_template = ButtonsTemplate(
                title='功能選單', # 標題
                text='請選擇：', # 模板的文字內容
                thumbnail_image_url='https://wish.with.tw/cdn/shop/articles/DALL_E_2024-04-07_13.48.05_-_Create_an_image_that_embodies_the_theme_of_inspiring_and_motivational_quotes_from_various_anime_series._The_image_should_visually_represent_the_essenc.webp', # 圖片網址
                actions=[
                    MessageAction(label='比較成分', text='@開始比較成分'),
                    MessageAction(label='分析成分', text='@開始分析成分'),
                    MessageAction(label='輸入成分（未整合）', text='@輸入成分'),
                ])
            # 建立模板訊息
            template_message = TemplateMessage(
                # alt_text 是 LINE 跳出通知時，上面會顯示的文字
                alt_text='有這些功能可以使用',
                template=buttons_template
            )
            reply_messages = [template_message]

        elif user_message == "@輸入成分":
            if not choose_empty_ingred():
                reply_messages = [TextMessage(text="已無空成分")]
            else:
                temp_ingred_list = [choose_empty_ingred() for _ in range(4)]
                buttons_template = ButtonsTemplate(
                    title='輸入成分內容', # 標題
                    text='請選擇想要輸入內容的成分', # 模板的文字內容
                    thumbnail_image_url='https://wish.with.tw/cdn/shop/articles/DALL_E_2024-04-07_13.48.05_-_Create_an_image_that_embodies_the_theme_of_inspiring_and_motivational_quotes_from_various_anime_series._The_image_should_visually_represent_the_essenc.webp', # 圖片網址
                    actions=[
                        # 會發送一個 postback 資料給伺服器，就是Post給自己
                        # 使用 PostbackAction 會觸發下面的 PostbackEvent
                        PostbackAction(label=ingred[:20], data=ingred, displayText="我選擇：{}".format(ingred),
                                       inputOption='openKeyboard', fillInText="【 "+ingred+" 】\nzh: \nusage: \nsource: \nsafety: ")
                        for ingred in temp_ingred_list
                        # label 是按鈕上的文字，最長20，data 是按鈕被點擊時會發送的資料
                    ])
                # 建立模板訊息
                template_message = TemplateMessage(
                    # alt_text 是 LINE 跳出通知時，上面會顯示的文字
                    alt_text='請選擇想要輸入內容的成分',
                    template=buttons_template
                )
                reply_messages = [template_message]
            
        elif user_message.startswith("【") and user_message.split('\n')[0].endswith("】"):
            if add_ingred_contents(user_message):
                reply_messages = [TextMessage(text="輸入成功")]
            else:
                reply_messages = [TextMessage(text="輸入失敗")]

        elif user_message == "@測試":
            pass

        else:
            # response = model.generate_content([user_message])
            response = gemini_mod(user_message)
            reply_messages = response.text

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=reply_messages,
            )
        )


from PIL import Image

# 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    print("收到圖片訊息")

    global is_asking_ingredients, ingredientslist_str
    global is_comparing_ingredients_1, is_comparing_ingredients_2
    global comparing_response_1, comparing_response_2

    if is_asking_ingredients: # "@開始分析成分"
        with ApiClient(configuration) as api_client:
            # 建立 MessagingApiBlob 實例
            line_bot_blob_api = MessagingApiBlob(api_client)
            # 將客戶端上傳的圖片轉換為PIL Image
            message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            print("這裡message_content:", io.BytesIO(message_content))
            image = Image.open(io.BytesIO(message_content))
            # 使用 Gemini 模型生成內容
            model_prompt = "請列出品名，再請抓取標示成分並列出每個成分，品名或每項成分皆以換行符號(\n)區隔，勿列出其他資訊"
            response = gemini_mod([model_prompt, image])
            ingredientslist_str = response.text
            reply_messages = [TextMessage(text=response.text,
                                          quick_reply=QuickReply(
                                                items=[
                                                    QuickReplyItem(action=MessageAction(label="AI分析成分", text="@AI分析成分"),),
                                                ]
                                          ))]
            is_asking_ingredients = False
            print(response.text.split('\n'))
            try:
                # 存入 json
                add_to_json(response.text.split('\n'))
                
            except Exception as e:
                print("存入 ingred_list 發生錯誤：", e)
        
    elif is_comparing_ingredients_1: # "@開始比較成分"
        with ApiClient(configuration) as api_client:
            line_bot_blob_api = MessagingApiBlob(api_client)
            message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            print("這裡message_content:", io.BytesIO(message_content))
            
            image = Image.open(io.BytesIO(message_content))
            model_prompt = "請只擷取這張圖中標示成分的部分，並將每項成分以逗號區隔列出，勿列出其他資訊。若有多種語言請只取一種。"
            response = gemini_mod([model_prompt, image])
        
            comparing_response_1 = response.text
            reply_messages=[TextMessage(text=response.text+"\n\n"+"="*20+"\n請上傳第二張圖片")]
            is_comparing_ingredients_1 = False
            is_comparing_ingredients_2 = True
        
    elif is_comparing_ingredients_2:
        with ApiClient(configuration) as api_client:
            line_bot_blob_api = MessagingApiBlob(api_client)
            message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            print("這裡message_content:", io.BytesIO(message_content))
            
            image = Image.open(io.BytesIO(message_content))
            model_prompt = "請只擷取這張圖中標示成分的部分，並將每項成分以逗號區隔列出，勿列出其他資訊。若有多種語言請只取一種。"
            response = gemini_mod([model_prompt, image])
            
            comparing_response_2 = response.text
            reply_messages=[TextMessage(text=response.text+ "\n\n"+"="*20+"\n請輸入：「@顯示比較結果」",
                                        quick_reply=QuickReply(
                                            items=[
                                                QuickReplyItem(
                                                    action=MessageAction(label="@顯示比較結果", text="@顯示比較結果"),
                                                ),
                                            ]
                                        ))]
            is_comparing_ingredients_2 = False
        
    else:
        with ApiClient(configuration) as api_client:
            line_bot_blob_api = MessagingApiBlob(api_client)
            # 將客戶端上傳的圖片轉換為PIL Image
            message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            print("這裡message_content:", io.BytesIO(message_content))
            image = Image.open(io.BytesIO(message_content))
            # 使用 Gemini 模型生成內容
            model_prompt = "請分析這張圖片，並且用正體中文回答"
            # response = model.generate_content([model_prompt, image])
            response = gemini_mod([model_prompt, image])
            reply_messages=[TextMessage(text=response.text)]
    
    # TemporaryFile 回傳一個可當作臨時儲存區域的類檔案物件
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix="jpg" + '-', delete=False) as tf:
        tf.write(message_content)
        tempfile_path = tf.name
    
    dist_path = tempfile_path + '.jpg' # 檔案路徑
    dist_name = os.path.basename(dist_path) # 檔案名稱
    # os.rename(要修改的檔案或目錄名, 修改後的檔案或目錄名) # 重新命名檔案
    os.rename(tempfile_path, dist_path)
    
    with ApiClient(configuration) as api_client:
        # 建立 MessagingApi 實例
        line_bot_api = MessagingApi(api_client)
        # 回覆使用者的訊息
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                # 回覆使用者的訊息
                messages=reply_messages,
            )
        )


@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        ingred =  event.postback.data
        text = f"請輸入 {ingred} 的中文名(zh)、用途(usage)、來源(source)及安全性(safety)。"
        reply_messages = [TextMessage(text=text,
                                      quick_reply=QuickReply(
                                                items=[
                                                    QuickReplyItem(action=ClipboardAction(label=f"複製 「{ingred}」", clipboard_text=ingred),),
                                                ]
                                          ))]
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=reply_messages
            )
        )

if __name__ == "__main__":
    app.run(port=5001, debug=True)

# 這裡的 port 要和 ngrok 的 port 一致