import os
from configparser import ConfigParser
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain_core.prompts.chat import ChatPromptTemplate


try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
        raise Exception("Please provide a valid API key and endpoint")
except:
    try:
        config = ConfigParser()
        config.read('config.ini')
        AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
        AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
        AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
        AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')

        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT_NAME:
            raise Exception("Please provide a valid API key and endpoint")
    except:
        print("Please provide a valid API key and endpoint")
        exit()


model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        )

# 模板定義
example_prompt = (
    HumanMessagePromptTemplate.from_template("{description}")  # 使用者輸入部分
    + AIMessagePromptTemplate.from_template("{classification}")  # AI 回應部分
)

# 情報資料
examples = [
    {
        "description": "食物偏甜",
        "classification": "南部人",
    },
    {
        "description": "食物偏鹹",
        "classification": "北部人",
    },
    {
        "description": "滷肉飯",
        "classification": "北部人",
    },
    {
        "description": "搭乘大眾運輸，不怕走路",
        "classification": "北部人",
    },
    {
        "description": "騎摩托車",
        "classification": "南部人",
    },
    {
        "description": "講話婉轉",
        "classification": "北部人",
    },
    {
        "description": "講話直接",
        "classification": "南部人",
    },
]

# FewShotChatMessagePromptTemplate
# 用於建立少量樣本（few-shot）提示的模板，讓 AI 模型可以通過學習範例來理解任務。
few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,  # 提供的資料列表
    example_prompt=example_prompt,  # 資料的格式模板
)

parser = StrOutputParser() 
# 輸出解析器：用來處理模型的輸出
# 將模型的輸出轉換為純文字字串
# 移除任何額外的格式或標記

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "請根據以下描述，判斷這個人是哪裡人："),
        few_shot_prompt,
        ("human", "{input}")
    ]
)

chain = final_prompt | model | parser

user_input = "喜歡吃醬油，特別是帶有甜味的"
response = chain.invoke({"input": user_input})
print("描述：" + user_input)  # 描述：喜歡吃醬油，特別是帶有甜味的
print("分類：" + response)  # 分類：南部人


user_input = "很熱心，喜歡幫助別人"
response = chain.invoke({"input": user_input})
print("描述：" + user_input)  # 描述：很熱心，喜歡幫助別人
print("分類：" + response)  # 分類：南部人