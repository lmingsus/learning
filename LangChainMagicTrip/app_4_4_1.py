from configparser import ConfigParser

# 引入 Azure OpenAI LLM 模組
from langchain_openai import AzureChatOpenAI
# 引入 Prompt Template 模組
from langchain_core.prompts import PromptTemplate
# 引入 Output Parser 模組
from langchain_core.output_parsers import StrOutputParser
# 引入 RunnableParallel 模組
from langchain_core.runnables import RunnableParallel

from datetime import datetime


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
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)

llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.9,
                        )

# 定義描述城市的提示模板
describe_prompt = PromptTemplate(
    input_variables=["city"],
    template="請用以五十字以內描述 ### {city} ### 這個城市。"
)

# 定義描述氣候的提示模板
climate_prompt = PromptTemplate(
    input_variables=["city", "month"],
    template="現在是 {month}，請以十字以內描述 ### {city} ### 這個城市的氣候。"
)

# 定義生成旅遊建議的提示模板
travel_prompt = PromptTemplate(
    input_variables=["description", "climate"],
    template="請根據以下對這個城市的描述，為旅客提供三十字以內旅遊指南: ### {description} ### ，氣候： ### {climate} ###"
)

# 定義翻譯的提示模板
translate_prompt = PromptTemplate(
    input_variables=["travel"],
    template="請將以下描述翻譯成日文: ### {travel} ###"
)

# 定義輸出解析器
parser = StrOutputParser()


# 建立三個 Chain，分別對應描述、生成旅遊建議與翻譯
describe_chain = describe_prompt | llm | {"description": lambda x: x.content}
climate_chain = climate_prompt | llm | {"climate": lambda x: x.content}

# 1. 描述
describe_and_climate_chain = RunnableParallel(
    description=describe_chain,
    climate=climate_chain
)

# 2. 旅遊建議
travel_chain = travel_prompt | llm | parser
# 3. 翻譯
translate_chain = translate_prompt | llm | parser


# 最終執行處理鏈
chain = describe_and_climate_chain | travel_chain | translate_chain

# 本月份數字
current_month = datetime.now().month

result = chain.invoke({"city": "員林", "month": current_month})


# 印出結果
print(result)
'### 員林の文化歴史を探索し、地元のスナックを味わい、マーケットをぶらぶらし、親切な住民の温かさを感じ、四季のはっきりした気候を楽しみましょう。 ###'