import os
from configparser import ConfigParser

from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import AzureOpenAIEmbeddings

try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/embeddings?api-version={AZURE_OPENAI_API_VERSION}
    MODEL = os.getenv("MODEL")
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
        MODEL = config.get('Azure_Embeddings', 'MODEL')
        AZURE_OPENAI_API_KEY = config.get('Azure_Embeddings', 'OPENAI_KEY')
        AZURE_OPENAI_API_VERSION = config.get('Azure_Embeddings', 'OPENAI_API_VERSION')
        AZURE_OPENAI_ENDPOINT = config.get('Azure_Embeddings', 'OPENAI_ENDPOINT')
        AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure_Embeddings', 'OPENAI_DEPLOYMENT_NAME')

        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT_NAME:
            raise Exception("Please provide a valid API key and endpoint")
    except:
        print("Please provide a valid API key and endpoint")
        exit()


# model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
#                         azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
#                         openai_api_version=AZURE_OPENAI_API_VERSION,
#                         api_key=AZURE_OPENAI_API_KEY,
#                         )


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
    model=MODEL,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
)


example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples, # 範例列表
    embedding_function,  # 來自 AzureOpenAIEmbeddings：將文字轉換為向量的函數
    Chroma,  # 用於儲存和檢索向量的資料庫
    k=1  # 指定返回最相似的範例數量
)

def fun32():

    # find the most similar example to the user input
    question = "喜歡到台北車站"

    selected_example = example_selector.select_examples(
        {"description": question},
    )

    print(selected_example)
    print("最相似的例子是：")
    for example in selected_example:
        for key, value in example.items():
            print(f"{key}: {value}")
        print("\n")


# ===============================================

from pathlib import Path

def fun32_2():

    # 建立儲存目錄
    persist_directory = "./chroma_db"
    Path(persist_directory).mkdir(parents=True, exist_ok=True)

    # 先創建 Chroma 資料庫實例
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,
        collection_name="north_south_examples"
    )

    example_selector1 = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embedding_function,
        vectorstore,
        k=1,
    )

    question1 = "不喜歡到台北車站"

    selected_example1 = example_selector1.select_examples(
        {"description": question1},
    )

    print(selected_example1)
    # [{'classification': '北部人', 'description': '搭乘大眾運輸，不怕走路'}]
    print("最相似的例子是：")
    for example in selected_example1:
        for key, value in example.items():
            print(f"{key}: {value}")
        print("\n")

# ===============================================

# 在後續使用時，可以直接載入已存在的向量資料庫

def fun32_3(persist_directory):
    
    loaded_vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,  
        collection_name="north_south_examples"
    )

    example_selector2 = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embedding_function,
        loaded_vectorstore,
        k=1,
    )

    question2 = "講話拐彎抹角"

    selected_example2 = example_selector2.select_examples(
        {"description": question2},
    )
    print(selected_example2)
    # [{'classification': '南部人', 'description': '講話直接'}]


    question3 = "熱情大方"
    selected_example3 = example_selector2.select_examples(
        {"description": question3},
    )
    print(selected_example3)
    # [{'classification': '南部人', 'description': '講話直接'}]