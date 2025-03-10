from configparser import ConfigParser
# 引入 Azure OpenAI LLM 模組
from langchain_openai import AzureChatOpenAI
# 引入 Chain 模組，已棄用
# from langchain.chains import LLMChain # Deprecated
# 引入 Prompt Template 模組
from langchain_core.prompts import PromptTemplate

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



prompt = PromptTemplate.from_template(
    "Translate the following English text to zh-tw: {text}"
    )

model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        )

chain = prompt | model # | parser

# 輸入英文文本
text = "I am a student."
response = chain.invoke({"text": text})
print(response)

# 輸出結果：
content='我是學生。' 
additional_kwargs={'refusal': None} 
response_metadata={
    'token_usage': {'completion_tokens': 3, 
                    'prompt_tokens': 22, 
                    'total_tokens': 25, 
                    'completion_tokens_details': {
                        'accepted_prediction_tokens': 0, 
                        'audio_tokens': 0, 
                        'reasoning_tokens': 0, 
                        'rejected_prediction_tokens': 0
                        }, 
                    'prompt_tokens_details': {
                        'audio_tokens': 0, 
                        'cached_tokens': 0}
                    }, 
    'model_name': 'gpt-4o-mini-2024-07-18', 
    'system_fingerprint': 'fp_ded0d14823', 
    'prompt_filter_results': [
        {'prompt_index': 0, 
         'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 
                                    'jailbreak': {'filtered': False, 'detected': False}, 
                                    'self_harm': {'filtered': False, 'severity': 'safe'}, 
                                    'sexual': {'filtered': False, 'severity': 'safe'}, 
                                    'violence': {'filtered': False, 'severity': 'safe'}}}],
    'finish_reason': 'stop', 
    'logprobs': None, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 
                                                 'protected_material_code': {'filtered': False, 'detected': False}, 
                                                 'protected_material_text': {'filtered': False, 'detected': False}, 
                                                 'self_harm': {'filtered': False, 'severity': 'safe'}, 
                                                 'sexual': {'filtered': False, 'severity': 'safe'}, 
                                                 'violence': {'filtered': False, 'severity': 'safe'}}}
id='run-4b903d4d-4dca-46d4-b62e-e9ba1c48fe06-0' 
usage_metadata={'input_tokens': 22, 
                'output_tokens': 3, 
                'total_tokens': 25, 
                'input_token_details': {'audio': 0, 'cache_read': 0}, 
                'output_token_details': {'audio': 0, 'reasoning': 0}}



# 只在特定呼叫時啟用 verbose
text2 = "Ukraine’s presence in Russia’s Kursk region has deteriorated sharply, with the advance threatening Kyiv’s sole territorial bargaining counter at a crucial time in the war."

from langchain_core.callbacks import StdOutCallbackHandler

response2 = chain.invoke(
    {"text": text2},
    config={
        "callbacks": [StdOutCallbackHandler()],
        "verbose": True
    }
)
# 輸出：
# > Entering new RunnableSequence chain...


# > Entering new PromptTemplate chain...

# > Finished chain.

# > Finished chain.
print(response2)