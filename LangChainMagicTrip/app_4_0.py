'''
1. Prompt Templates
2. LLM
3. Output Parser
都是 Runnable 物件，可以串接在一起，形成一個 Chain。

LCEL: LangChain Expression Language

'''
from configparser import ConfigParser
# 引入 Azure OpenAI LLM 模組
from langchain_openai import AzureChatOpenAI
# 引入 Prompt Template 模組
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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



# Input Prompt Template
prompt = ChatPromptTemplate.from_template('{city} 位於哪個國家？')

# Azure OpenAI LLM 物件
model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        )

# Output Parser
output_parser = StrOutputParser()

# chain
chain = prompt | model | output_parser

# result
result = chain.invoke({'city': '高雄'})
print(result)
# 高雄位於台灣。它是台灣的主要城市之一，位於台灣的南部沿海地區。高雄是台灣第二大城市，也是重要的港口城市。

# =========================================================
# 不使用 LCEL 表達式
prompt0 = ChatPromptTemplate.from_template('{city} 位於哪個國家？')

result0 = output_parser.invoke(
            model.invoke(
                prompt0.invoke({'city': '高雄'})
                )
            )
print(result0)
# 高雄位於台灣，是台灣的第二大城市，位於其南部沿海地區。


# =========================================================
# RunnableSequence 類別
from langchain_core.runnables import RunnableSequence

prompt1 = ChatPromptTemplate.from_template('在 {city} 的人都如何用餐？')

chain1 = RunnableSequence(
    prompt1,
    model,
    output_parser
)

result1 = chain1.invoke({'city': '員林'})
print(result1)


# =========================================================
# RunnableParrallel 類別
# 將同一個輸入傳送到多個 Runnable 物件，並行執行
# 並將所有的結果合併成一個結果（字典）


from langchain_core.runnables import RunnableParallel

# 建立第一個 PromptTemplate
prompt2 = ChatPromptTemplate.from_template('在 {city} 的人都如何用餐？')
chain2 = prompt2 | model | output_parser

# 建立第二個 PromptTemplate
prompt3 = ChatPromptTemplate.from_template('在 {city} 的人都喜歡吃什麼？')
chain3 = prompt3 | model | output_parser

# 建立 RunnableParallel 物件
eating_style_chain = RunnableParallel(
    style=chain2,
    food=chain3
)

result2 = eating_style_chain.invoke({'city': '員林'})
print(result2)
# 輸出字典：
{'style': '員林是台灣彰化縣的一個城鎮...', 
 'food': '員林是台灣的一個城市，以美食聞名...美食選擇非常多樣。'}
print(result2.get('style'))
print(result2.get('food'))

# =================
# 也可改為
eating_style_chain4 = RunnableParallel(
    {'style': chain2, 'food': chain3}
)

result4 = eating_style_chain4.invoke({'city': '彰化'})
print(result4)
# 輸出字典：
{'style': '彰化是台灣的一個城市，以其豐富的美食文化聞名...', 
 'food': '彰化是台灣的一個縣，因為地理和文化的特色...必嚐的美食。'}
print(result4.get('style'))
print(result4.get('food'))


# =========================================================
# RunnablePassthrough 類別
# 傳遞資料，不做任何處理

from langchain_core.runnables import RunnablePassthrough

# 建立一個 RunnablePassthrough 
passthrough0 = RunnablePassthrough()

# 傳遞單一資料，不做任何處理
output0 = passthrough0.invoke('Hello, World!')

print(output0) 
# 輸出： Hello, World!

data01 = {'message': "This is a test message.",
         'value': 21}

output01 = passthrough0.invoke(data01)
print(output01)
#  輸出：{'message': 'This is a test message.', 'value': 21}


# =========================================================
# RunnableBinding 類別
# 將輸入資料綁定到指定的變數上，並將其傳遞給下一個 Runnable 物件
# 需要在多個上下文裡面共享參數，使用 RunnableBinding。

from langchain_core.runnables import Runnable

# 定義可執行的 Runnable
class MyRunnable0(Runnable):
    def invoke(self, input, *args, **kwargs):
        constant_param = kwargs.get('constant_param_123', 'No constant_param provided')
        return {"Processed": input, "Constant Param": constant_param}

# 建立 RunnableBinding 物件
my_runnable0 = MyRunnable0()
bound_runnable0 = my_runnable0.bind(constant_param_123=55555)

# 執行 RunnableBinding 物件
result5 = bound_runnable0.invoke("666666")
print(result5)
# {'Processed': '666666', 'Constant Param': 55555}

# =====================
# 批次處理或串流

# 使用 `bind` 方法建立 RunnableBinding 物件，並傳遞額外參數
runnable_binding1 = model.bind(stop=['餘暉'])

# 調用 runnable_binding1 物件
result6 = runnable_binding1.invoke("請你說：「說真的，只能陪你走到這。當夕陽，餘暉灑落的此刻。」")
print(result6)
print(type(result6))  # <class 'langchain_core.messages.ai.AIMessage'>
print(result6.content) # 說真的，只能陪你走到這。當夕陽，
# 輸出：
content='說真的，只能陪你走到這。當夕陽，' 
additional_kwargs={'refusal': None} 
response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 36, 'total_tokens': 50, 
                                   'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 
                                   'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 
                    'model_name': 'gpt-4o-mini-2024-07-18', 
                    'system_fingerprint': 'fp_ded0d14823', 
                    'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'jailbreak': {'filtered': False, 'detected': False}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 
                    'finish_reason': 'stop', 
                    'logprobs': None, 
                    'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'protected_material_code': {'filtered': False, 'detected': False}, 'protected_material_text': {'filtered': False, 'detected': False}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}} 
id='run-763b3edd-fbb0-4a7b-bd5b-2983134413f3-0' 
usage_metadata={'input_tokens': 36, 'output_tokens': 14, 'total_tokens': 50, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}