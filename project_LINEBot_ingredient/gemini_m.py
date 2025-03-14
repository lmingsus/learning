from configparser import ConfigParser
import google.generativeai as genai


# 載入設定檔取得金鑰
config = ConfigParser()
config.read('config.ini')
Gemini_API_KEY = config['Gemini']['Gemini_API_KEY']

# 建立 Gemini 模型
genai.configure(api_key=Gemini_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def gemini_mod(input: str|list):
    '''
    透過 Gemini 模型生成文本
    :param input: 輸入文本
    '''
    # 透過 Gemini 模型生成文本
    response = model.generate_content(input)
    return response


def gemini_chat_test(prompt, history=[]):
    '''
    透過 Gemini 模型進行對話測試
    :param promt: 輸入文本
    '''
    # 透過 Gemini 模型進行對話測試
    chat = model.start_chat(history=history)
    response = model.send_message(prompt)
    return response.text

# chat = model.start_chat(history=[])


# prompt = "你好我家有3隻狗"
# response = chat.send_message(prompt)
# response.text

# prompt2 = "我家有幾隻狗"
# response2 = chat.send_message(prompt2)
# response2.text

# print(response)

if __name__ == '__main__':
    # 將客戶端上傳的圖片轉換為PIL Image
    from PIL import Image
    import io
    
    with open('aaa1.jpg', 'rb') as f:
        image_data1 = f.read()
    image1 = Image.open(io.BytesIO(image_data1))
    with open('bbb.jpg', 'rb') as f:
        image_data2 = f.read()
    image2 = Image.open(io.BytesIO(image_data2))
    # 使用 Gemini 模型生成內容
    model_prompt = "請比較這兩樣商品的成分"
    response = gemini_mod([model_prompt, image1, image2])