import os
from configparser import ConfigParser
from openai import AzureOpenAI

try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
        raise Exception("Please provide a valid API key and endpoint")
except:
    try:
        config = ConfigParser()
        config.read('config.ini')
        AZURE_OPENAI_API_KEY = config['Azure']['OPENAI_KEY']
        AZURE_OPENAI_API_VERSION = config['Azure']['OPENAI_API_VERSION']
        AZURE_OPENAI_ENDPOINT = config['Azure']['OPENAI_ENDPOINT']
    except:
        print("Please provide a valid API key and endpoint")
        exit()

client = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY,
                    api_version=AZURE_OPENAI_API_VERSION,
                    azure_endpoint = AZURE_OPENAI_ENDPOINT
                    )

AZURE_OPENAI_DEPLOYMENT_NAME = config['Azure']['OPENAI_DEPLOYMENT_NAME']
deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME # the custom name you chose for your deployment


#  `system` 訊息用來設定 AI 的行為模式，而 `user` 和 `assistant` 的對話可以構建更複雜的互動。


### 1. 設定特定角色的助手

messages=[
    {"role": "system", "content": "你是一位精通科技歷史的專家，特別熟悉科技公司的發展史。"},
    {"role": "user", "content": "請詳細說明微軟的創立過程。"}
]


### 2. 多輪對話範例

messages=[
    {"role": "system", "content": "你是一位耐心的教師。"},
    {"role": "user", "content": "什麼是作業系統？"},
    {"role": "assistant", "content": "作業系統是電腦的基礎軟體，負責管理硬體資源。"},
    {"role": "user", "content": "Windows 是什麼時候發布的？"}
]

### 3. 設定特定輸出格式

messages=[
    {"role": "system", "content": "請以簡潔的重點列表方式回答問題。"},
    {"role": "user", "content": "列出微軟最重要的產品。"}
]


### 4. 多語言切換

messages=[
    {"role": "system", "content": "你是一位翻譯專家，請用中文和英文回答。"},
    {"role": "user", "content": "介紹比爾蓋茲。"}
]



### 5. 角色扮演情境

messages=[
    {"role": "system", "content": "你是比爾蓋茲，請用第一人稱回答問題。"},
    {"role": "user", "content": "請分享您創立微軟的經驗。"}
]



response = client.chat.completions.create(
    model=deployment_name, # model = "deployment_name".
    messages=messages
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)


