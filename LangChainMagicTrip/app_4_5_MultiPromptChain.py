'''
https://python.langchain.com/docs/versions/migrating_chains/multi_prompt_chain/
MultiPromptChain:
    - RouterChain: 負責決定將輸入的訊息轉發到不同的Chain
    - DestinationChain: 每一個任務的 Chain
'''

from configparser import ConfigParser

# 引入必要的模組
from langchain.chains.router import MultiPromptChain
from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI


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
                        temperature=0.5,
                        )



# 定義 翻譯 template
translate_template = """將以下中文文本翻譯成英文：{input}"""

# 定義 寫作 template
write_template = """根據以下提示創作一段文字：{input}"""

# 每一個任務Chain的資訊
prompt_infos = [
    {
        "name": "translate_chain", # chain 名稱
        "description": "進行中文翻譯成英文的任務", # chain 的簡單描述
        "prompt_template": translate_template, # chain的提示樣板
    },
    {
        "name": "write_chain", # chain 名稱
        "description": "進行創意寫作的任務", # chain 的簡單描述
        "prompt_template": write_template , # chain的提示樣板
    },
]

chain = MultiPromptChain.from_prompts(llm, prompt_infos)

chain.invoke({"input": "我想要一杯咖啡。"})
# {'input': '我想要一杯咖啡。', 'text': 'I would like a cup of coffee.'}

chain.invoke({"input": "請寫一篇關於夏天初戀約一百字文章。"})
# {'input': '請寫一篇關於夏天初戀的創意文章，大約一百字。',
#  'text': '在那個陽光燦爛的夏天，我們的故事在蝉鸣聲中悄然展開。她的笑聲如清泉般流淌，輕輕撩動我心底的涟漪。每個午後，我們一起在樹蔭下分享冰淇淋，手指輕觸間，彷彿時間靜止。夕陽染紅了天邊，我們的約定在微風中飄蕩，像是永恆的誓言。那段純真的初戀，宛如盛夏的花朵，雖然短暫卻絢爛無比，成為我心中永不褪色的記憶。'}


# ===================================================================
# # 一般 Prompt template
# # 定義 一般 template，當目標任務不在任務列表中時，使用此 template
# general_template = """回答以下問題：{input}"""
# general_prompt = PromptTemplate(
#     input_variables=["input"],
#     template=general_template,  # 使用一般 template
#     output_variables=["text"]
# )
# # 一般 chain
# general_chain = general_prompt | llm

general_prompt = "回答以下問題：{input}"
general_chain = general_prompt | llm

chain2 = MultiPromptChain.from_prompts(llm, prompt_infos, default_chain=general_chain)
# 'RunnableSequence' object has no attribute 'get'