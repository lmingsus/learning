import os
from configparser import ConfigParser

from langchain_core.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate

from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate


try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/embeddings?api-version={AZURE_OPENAI_API_VERSION}
    # Azure OpenAI Model
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
        raise 
    
    # Azure OpenAI Embedding Model
    AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("MODEL")
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_EMBEDDING_VERSION = os.getenv("AZURE_OPENAI_API_EMBEDDING_VERSION")
    if not AZURE_OPENAI_EMBEDDING_MODEL or not AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME or not AZURE_OPENAI_API_EMBEDDING_VERSION:
        raise 
    
except:
    try:
        config = ConfigParser()
        config.read('config.ini')
        # Azure OpenAI Model
        AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
        AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
        AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
        AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT_NAME:
            raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI 參數")
        
        # Azure OpenAI Embedding Model
        AZURE_OPENAI_EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
        AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
        AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
        if not AZURE_OPENAI_EMBEDDING_MODEL or not AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME or not AZURE_OPENAI_API_EMBEDDING_VERSION:
            raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI Embedding Model 參數")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please provide a valid API key and endpoint")
        exit(1)


# 模板定義
example_prompt = (
    HumanMessagePromptTemplate.from_template("{description}")  # 使用者輸入部分
    + AIMessagePromptTemplate.from_template("{classification}")  # AI 回應部分
)

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
        "description": "肉燥飯",
        "classification": "南部人",
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
        "description": "講話婉轉，不直接",
        "classification": "北部人",
    },
    {
        "description": "講話直接",
        "classification": "南部人",
    },
]

# 將 text-embedding-3-small 作為 Embedding Model
#https://learn.microsoft.com/zh-tw/azure/ai-services/openai/tutorials/embeddings?tabs=python-new%2Ccommand-line&pivots=programming-language-python
embedding_function = AzureOpenAIEmbeddings(
    model=AZURE_OPENAI_EMBEDDING_MODEL,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_EMBEDDING_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
)

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples, # 範例列表
    embedding_function,  # 來自 AzureOpenAIEmbeddings：將文字轉換為向量的函數
    Chroma,  # 用於儲存和檢索向量的資料庫
    k=1  # 指定返回最相似的範例數量
)



# 3-3

# 修改 few shot prompt，加入 example_selector 參數
few_shot_prompt_v2 = FewShotChatMessagePromptTemplate(
    # examples=examples, # 這裡不再需要 examples
    example_prompt=example_prompt,
    example_selector=example_selector,
)

# 撈出最相關的一則情報
print(few_shot_prompt_v2.invoke({"description": "喜歡吃甜甜"}))
# 輸出：
# messages=[HumanMessage(content='食物偏甜', additional_kwargs={}, response_metadata={}), 
#           AIMessage(content='南部人', additional_kwargs={}, response_metadata={})]




# 要求 LLM 根據精選的情報判斷，使 LLM 回應限縮在判斷北部人或南部人
model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        )

final_prompt_v2 = ChatPromptTemplate.from_messages(
    [
        ("system", "請根據以下精選參考描述，判斷這個人是北部人還是南部人："),
        few_shot_prompt_v2,
        ("human", "{input}"),
    ]
)

parser = StrOutputParser()

chain_v2 = final_prompt_v2 | model | parser


user_input = "喜歡吃醬油有甜味的"
response = chain_v2.invoke({"input": user_input})  # invoke 輸入必須是字典格式
print("描述：", user_input)
print("分類：", response)
# 描述： 喜歡吃醬油有甜味的
# 分類： 南部人

user_input2 = "熱情大方，講話直接"
response2 = chain_v2.invoke({"input": user_input2})  # invoke 輸入必須是字典格式
print("描述：", user_input2)
print("分類：", response2)
# 分類： 這個人可能是南部人。南部人通常給人熱情大方的印象，且講話比較直接。



# ======================================================
# 修正提示，請 LLM 做選擇：
final_prompt_v2_2 = ChatPromptTemplate.from_messages(
    [
        ("system", "請根據以下精選參考描述，判斷這個人是北部人還是南部人："),
        few_shot_prompt_v2,
        ("human", "{input}"),
    ]
)

chain_v2_2 = final_prompt_v2_2 | model | parser
user_input3 = "熱情大方"
response3 = chain_v2_2.invoke({"input": user_input3})  # invoke 輸入必須是字典格式
print("描述：", user_input3)
print("分類：", response3)
# 分類： 南部人