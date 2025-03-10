import os
from configparser import ConfigParser
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


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


model = AzureChatOpenAI(api_key=AZURE_OPENAI_API_KEY,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME
                        )



### exp 1：保留完整的回應內容，包括其他元數據metadata
response = model.invoke("你好，請問你是誰？")
print(response.content)
# 需要使用 `response.content` 來獲取實際的文本內容
# 你好！我是一个人工智能助手，用来回答问题和提供信息。请问有什么我可以帮助你的呢？


### exp 1-1：使用解析器和鏈式調用，只包含文本內容
parser = StrOutputParser()  # 創建一個字符串輸出解析器
chain = model | parser  
# 管道運算符 `|` 將模型和解析器串聯成一個鏈，直接返回解析後的字符串結果
response = chain.invoke("你好，請問你是誰？")
print(response)



### exp 2：將提示放在 invoke 方法中
parser = StrOutputParser()  # 創建一個字符串輸出解析器
chain = model | parser
response = chain.invoke("將以下中文翻譯成英文：知之為知之，不知為不知，是知也。")
print(response)


### exp 3：使用 ChatPromptTemplate 來定義提示
prompt_template = ChatPromptTemplate.from_messages(
    [("system", "你是一位哲學家，也是一位語言專家，請用你的專業翻譯以下內容為{language}。"),
     ("user", "{text}")]
)

chain = prompt_template | model | parser

target_language = "日文"
user_input = "知之為知之，不知為不知，是知也。"
chain.invoke({"text": user_input, "language": target_language})
# '知っていることを知っていると言い、知らないことを知らないと言う。それが真の知識である。'