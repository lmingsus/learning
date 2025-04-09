from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from IPython.display import Image, display



from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    # Gemini API
    GEMINI_API_KEY = config.get('GEMINI', 'API_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("請在 config.ini 中設定所有必要的 Gemini 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)



llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001", 
    google_api_key=GEMINI_API_KEY
)

user_messages = []

# append user input question
user_input = "圖片中的生物是什麼？"

user_messages.append({"type": "text", "text": user_input + "請使用繁體中文回答。"})

# append images
image_url = "https://cdn.myfeel-tw.com/media/hzhvEfU2r5fx0o3b4PKDM31XhnJXs3LuToUw1EZr.jpg"

user_messages.append({"type": "image_url", "image_url": image_url})

human_messages = HumanMessage(content=user_messages)

result = llm.invoke([human_messages])

print("Q: " + user_input)
print("A: " + result.content)

# Display the image
display(Image(url=image_url))



# =================================================================
# Loading from local files is no longer supported for security reasons. 
# Please specify images as Google Cloud Storage URI, b64 encoded image string (data:image/...), or valid image url.
import base64
import httpx

user_input2 = "請以正體中文描述這張圖片"
image_url = "https://upload.wikimedia.org/wikipedia/commons/9/9f/Yuanlin_Station_20150425.jpg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
message = HumanMessage(
    content=[
        {"type": "text", "text": user_input2},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ]
)
result2 = llm.invoke([message])
print("Q: " + user_input2)
print("A: " + result2.content)

# Display the image
display(Image(url=image_url, width=400))

# ===============================================================

import base64

# 指定本地圖片檔案路徑
image_file_path = "image.jpg"

# 讀取圖片檔案並進行 Base64 編碼
with open(image_file_path, "rb") as image_file:
    image_data3 = base64.b64encode(image_file.read()).decode("utf-8")

# 使用 Base64 編碼的圖片資料
message3 = HumanMessage(
    content=[
        {"type": "text", "text": user_input2},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data3}"},
        },
    ]
)

# 呼叫模型
result3 = llm.invoke([message3])
print("Q: " + user_input2)
print("A: " + result3.content)

# 顯示圖片
display(Image(filename=image_file_path, width=400))

# ==============================================================

user_messages = []
user_input4 = "這隻動物可能出現在這裡嗎？"

user_messages.append({"type": "text", "text": user_input4 + "請使用正體中文回答。"})

# 指定圖片網址
image_url = "https://upload.wikimedia.org/wikipedia/commons/9/9f/Yuanlin_Station_20150425.jpg"
user_messages.append({"type": "image_url", "image_url": image_url})

# 指定本地圖片檔案路徑
image_file_path = "image.jpg"
# 讀取圖片檔案並進行 Base64 編碼
with open(image_file_path, "rb") as image_file:
    image_data4 = base64.b64encode(image_file.read()).decode("utf-8")
    user_messages.append({"type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data4}"}})


human_messages = HumanMessage(content=user_messages)

result4 = llm.invoke([human_messages])

print("Q: " + user_input4)
print("A: " + result4.content)

'''
Q: 這隻動物可能出現在這裡嗎？
A: 圖片中的動物是水豚。

在第一張圖片的環境（看起來像台灣的捷運站）中，**水豚自然出現的可能性非常低。** 水豚原產於南美洲，它們需要特定的環境和氣候才能生存。

因此，水豚不太可能自然出現在那個捷運站附近。 除非是從動物園逃脫，或者有人非法飼養並棄養，否則不會在那裡看到水豚。
'''


# ==============================================================
from google import genai
from PIL import Image

client = genai.Client(api_key=GEMINI_API_KEY)

# 指定本地圖片檔案路徑
image_path = "https://upload.wikimedia.org/wikipedia/commons/9/9f/Yuanlin_Station_20150425.jpg"
image0 = Image.open("image.jpg")
image0.load()  # 強制載入全部圖片數據

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        '告訴我這張圖片的內容。',
        image0
    ]
)
# print(response.text)
# * GenerateContentRequest.contents[1].parts: contents.parts must not be empty.


# =================================
with open(image_file_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# 構建內容：注意必須以特定格式傳遞 base64 編碼的圖片
contents = [
    '告訴我這張圖片的內容。',
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
]

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=contents
)
# print(response.text)
# Input should be a valid string [type=string_type, input_value=[...], input_type=list]

# =================================
import base64

# 讀取本地圖片並轉換成 Base64 格式
with open("image.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# 將圖片內嵌到純文字裡，使用特殊標記（這裡僅作示範，請參考官方文件指引正確使用）
contents = f"告訴我這張圖片的內容。圖片資料：data:image/jpeg;base64,{image_data}"

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=contents
)
print(response.text)

# ================================================================================
# https://ai.google.dev/gemini-api/docs/openai#image-understanding
import base64
from openai import OpenAI

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image("image.jpg")

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "請以正體中文告訴我這張圖片的內容。",
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0].message.content)
# 這張圖片中，可以看到三隻水豚擠在一起。牠們有著粗糙、棕色的毛髮，看起來有點濕潤。水豚的背景是綠色的草地，前方則有一些木頭和蔬菜水果，像是牠們的食物。其中兩隻水豚的臉部比較清晰，可以看見牠們的眼睛和鼻子。整體畫面給人一種溫馨、可愛的感覺。
print(response.model_dump_json(exclude_none=True, indent=4))
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "這張圖片中，可以看到三隻水豚擠在一起。牠們有著粗糙、棕色的毛髮，看起來有點濕潤。水豚的背景是綠色的草地，前方則有一些木頭和蔬菜水果，像是牠們的食物。其中兩隻水豚的臉部比較清晰，可以看見牠們的眼睛和鼻子。整體畫面給人一種溫馨、可愛的感覺。\n",
                "role": "assistant"
            }
        }
    ],
    "created": 1742744746,
    "model": "gemini-2.0-flash",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 84,
        "prompt_tokens": 3367,
        "total_tokens": 3451
    }
}