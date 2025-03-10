from configparser import ConfigParser

# 引入 Chain 模組
from langchain.chains.sequential import SimpleSequentialChain
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

llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.9,
                        )


# 定義
describe_prompt = PromptTemplate(
    input_variables=["city"],
    template="請用一段優雅的文字描述 {city} 這個城市。"
)

# 翻譯
translate_prompt = PromptTemplate(
    input_variables=["description"],
    template="請將以下描述翻譯成英文: ### {description} ###"
)

# 建立兩個 Chain，分別對應描述與翻譯
describe_chain = describe_prompt | llm
translate_chain = translate_prompt | llm


# chain = SimpleSequentialChain(chains=[describe_chain, translate_chain])
chain = (
    {"city": lambda x: x}  # 輸入映射
    | describe_prompt 
    | llm  
    | {"description": lambda x: x.content}  # 中間結果映射
    | translate_prompt 
    | llm
)
result = chain.invoke({"city": "高雄"})
print(result)
# 輸出：
content="### Kaohsiung, a harbor city located in the southwest of Taiwan, shines like a brilliant pearl, quietly radiating its charm. It boasts vast oceans and a blue sky, with the endless Kaohsiung Port witnessing the fusion of thriving trade and culture. The Love River meanders through the city, where the shadows of trees and lights intertwine, creating a romantic scene.\n\nThe streets of Kaohsiung are full of life, with the sounds of vendors and the aromas of street food intertwining, making it hard for visitors to leave. The clear waters of Lotus Pond reflect the colorful Dragon and Tiger Pagodas, while the incense from the temples wafts through the air, conveying the faith and hopes of the residents. The annual Kaohsiung Air Show amazes with the city's creativity and vitality, and the bustling Liuhe Night Market exemplifies the city's passion, with people expressing their love for life amid the throng.\n\nEvery corner of Kaohsiung exudes a unique atmosphere, from cultural and artistic exhibitions to explorations of natural beauty, all reflecting the city's inclusiveness and diversity. Kaohsiung, like an elegant woman, tells endless stories to each visitor with her unique charm. ###" 
additional_kwargs={'refusal': None} 
response_metadata={'token_usage': {'completion_tokens': 246, 
                                   'prompt_tokens': 374, 
                                   'total_tokens': 620, 
                                   'completion_tokens_details': {'accepted_prediction_tokens': 0, 
                                                                 'audio_tokens': 0, 
                                                                 'reasoning_tokens': 0, 
                                                                 'rejected_prediction_tokens': 0}, 
                                   'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 
                    'model_name': 'gpt-4o-mini-2024-07-18', 
                    'system_fingerprint': 'fp_b705f0c291', 
                    'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'jailbreak': {'filtered': False, 'detected': False}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 
                    'finish_reason': 'stop', 
                    'logprobs': None, 
                    'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'protected_material_code': {'filtered': False, 'detected': False}, 'protected_material_text': {'filtered': False, 'detected': False}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}} 
id='run-3ce3f306-0a48-43a7-9a6f-2fee1ecc9181-0' 
usage_metadata={'input_tokens': 374, 'output_tokens': 246, 'total_tokens': 620, 
                'input_token_details': {'audio': 0, 'cache_read': 0}, 
                'output_token_details': {'audio': 0, 'reasoning': 0}}