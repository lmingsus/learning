'''
MultiPromptChain:
    - RouterChain: 負責決定將輸入的訊息轉發到不同的Chain
    - DestinationChain: 每一個任務的 Chain
'''

from configparser import ConfigParser

# 引入必要的模組
from langchain.chains import LLMChain,ConversationChain
from langchain.chains.router import MultiPromptChain
from langchain_core.runnables import RunnableLambda, RunnableBranch
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
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

# 定義 一般 template，當目標任務不在任務列表中時，使用此 template
general_template = """回答以下問題：{input}"""
# 一般 Prompt template
general_prompt = PromptTemplate(
    input_variables=["input"],
    template=general_template,  # 使用一般 template
    output_variables=["text"]
)
# 一般 chain
general_chain = general_prompt | llm




# 每一個任務 Chain 的資訊
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

# 透過 prompt_infos 陣列取得各個 chain 的 name 以及 description 資訊
destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)
'translate_chain: 進行中文翻譯成英文的任務\nwrite_chain: 進行創意寫作的任務'


# 建立 LLMRouterChain：會根據 RouterOutputParser 的結果，將輸入的訊息轉發到不同的 Chain
# 使用 MULTI_PROMPT_ROUTER_TEMPLATE 格式化提示訊息
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    prompt_infos=prompt_infos,
    general_chain=general_chain,
    output_parser=RouterOutputParser()
)
# LLMRouterChain 
router_chain = router_prompt| llm

print(router_prompt)
"""
input_variables=['input'] 
input_types={} 
output_parser=RouterOutputParser() 
partial_variables={} 
template='Given a raw text input to a language model select the model prompt best suited for the input. \
            You will be given the names of the available prompts and a description of what the prompt is best suited for.\
            You may also revise the original input if you think that revising it will ultimately lead to a better response from the language model.\n\n\
            << FORMATTING >>\nReturn a markdown code snippet with a JSON object formatted to look like:\n```json\n\
            {{\n    "destination": string \\ name of the prompt to use or "DEFAULT"\n    "next_inputs": string \\ a potentially modified version of the original input\n}}\n```\n\n\
            REMEMBER: "destination" MUST be one of the candidate prompt names specified below OR it can be "DEFAULT" if the input is not well suited for any of the candidate prompts.\n\
            REMEMBER: "next_inputs" can just be the original input if you don\'t think any modifications are needed.\n\n\
            << CANDIDATE PROMPTS >>\ntranslate_chain: 進行中文翻譯成英文的任務\nwrite_chain: 進行創意寫作的任務\n\n\
            << INPUT >>\n{input}\n\n\
            << OUTPUT (must include ```json at the start of the response) >>\n\
            << OUTPUT (must end with ```) >>\n'
"""



# 建立執行任務的 chain 物件：destination_chains
destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]

    prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
    chain = prompt | llm

    destination_chains[name] = chain

# # 建立 MultiPromptChain
# # deprecated
# chain = MultiPromptChain(
#     router_chain=router_chain,
#     destination_chains=destination_chains,
#     default_chain=general_chain, # 預設執行chain
#     verbose=True,
# )

# # 建立分支處理鏈
# chain = RunnableBranch(
#     (lambda x: route_prompt(x) == "translate", translate_chain),
#     (lambda x: route_prompt(x) == "write", write_chain),
#     general_chain  # 預設處理鏈
# )



# 執行處理鏈
result = chain.invoke("請寫一篇關於夏天初戀約一百字文章。")
print(result)

# ===============================================
