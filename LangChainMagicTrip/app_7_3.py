from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    
    # Azure OpenAI Model
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
        raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)


# 定義模型
llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.8,
                        )

parser = StrOutputParser()
chain = llm | parser

messages = [
    SystemMessage(
        content="""
                  你是一個熱情的台灣人，使用繁體中文回答問題。
                  """
    ),
    HumanMessage(
        content="""
                  員林有什麼好吃的？
                 """
    ),
]

result = chain.invoke(messages)
print(result)

'''
員林有許多美味的小吃和餐廳，讓人流連忘返！以下是幾個推薦的美食：

1. **員林肉圓**：這道傳統小吃外皮Q彈，內餡鮮美，是當地的特色之一。
2. **蚵仔煎**：新鮮的蚵仔搭配蛋和蔬菜，口感滑嫩，是員林夜市的熱門選擇。
3. **牛肉麵**：當地的牛肉麵湯頭濃郁，牛肉鮮嫩，相當受歡迎。
4. **鹽酥雞**：許多攤位都有提供這道炸物，外脆內嫩，搭配多種調味料更是美味。
5. **豆花**：甜品方面，員林的豆花口感細膩，並有多種配料供選擇。

別忘了去逛逛員林的夜市，還能找到更多美味的小吃！希望你在員林的美食之旅愉快！'
'''