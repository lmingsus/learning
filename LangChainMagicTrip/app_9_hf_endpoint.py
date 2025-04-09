from langchain_huggingface import HuggingFaceEndpoint

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    ACCESS_TOKEN = config.get('HUGGING_FACE', 'ACCESS_TOKEN')

    if not ACCESS_TOKEN:
        raise ValueError("請在 config.ini 中設定所有必要的 HUGGING_FACE 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)

api_token = ACCESS_TOKEN

llm = HuggingFaceEndpoint(
    # repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    repo_id="google/gemma-3-27b-it",
    task="text-generation",
    max_new_tokens=50,
    do_sample=False,
    huggingfacehub_api_token = api_token
)

response = llm.invoke("富士山在哪裡？請用正體中文回答")

print(response)


# ===============================================
from huggingface_hub import InferenceClient

# 建立 InferenceClient 實例
client = InferenceClient(
    model="google/gemma-3-27b-it", 
    token=api_token
)

# 使用 chat_completion 方法執行對話式生成
# 注意：chat_completion 需要傳入 message 列表
response = client.chat_completion(
    messages=[{"role": "user", "content": "富士山在哪裡？"}],
    # max_tokens=50,
)

print(response)
print(response.choices[0].message.content)

# print(response.model_dump_json(exclude_none=True, indent=4))
# AttributeError: 'ChatCompletionOutput' object has no attribute 'model_dump_json'

import json
print(json.dumps(response, indent=4, ensure_ascii=False))

'''
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "富士山位於日本本州島中部的山梨縣和静岡縣交界處。 \n\n更精確的地理位置：\n\n*   **山梨縣側:** 富士吉田市、忍野村\n*   **静岡縣側:** 富士宮市、小山町\n\n它可以從東京、橫濱等附近的大城市看到，是日本最具代表性的地標之一。\n",
                "tool_calls": null
            },
            "logprobs": null
        }
    ],
    "created": 1742920278,
    "id": "",
    "model": "google/gemma-3-27b-it",
    "system_fingerprint": "3.2.1-native",
    "usage": {
        "completion_tokens": 85,
        "prompt_tokens": 14,
        "total_tokens": 99
    },
    "object": "chat.completion"
}
'''