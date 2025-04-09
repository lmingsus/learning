# from google import genai

# 使用 langchain_google_genai：pip install langchain-google-genai
# https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html
from langchain_google_genai import ChatGoogleGenerativeAI

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    # Gemini API
    GEMINI_API_KEY = config.get('GEMINI', 'API_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("請在 config.ini 中設定所有必要的 Gemini 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", 
                             api_key=GEMINI_API_KEY)

result = llm.invoke("何謂孿生質數？請以約150字解釋。")


print(result.content)
print(result.model_dump_json(exclude_none=False, indent=4))

'''
{
    "content": "孿生質數是指**相差 2 的兩個質數**。換句話說，它們是一對「鄰居」質數，中間只隔著一個數字。\n\n例如：\n\n*   3 和 5 (5 - 3 = 2)\n*   5 和 7 (7 - 5 = 2)\n*   11 和 13 (13 - 11 = 2)\n*   17 和 19 (19 - 17 = 2)\n\n孿生質數猜想是數論中一個著名的未解之謎，它猜測存在**無窮多對**孿生質數。雖然數學家們已經證明存在無窮多對質數之間相差一個固定的數（例如 246），但尚未完全證明相差 2 的情況。",
    "additional_kwargs": {},
    "response_metadata": {
        "prompt_feedback": {
            "block_reason": 0,
            "safety_ratings": []
        },
        "finish_reason": "STOP",
        "safety_ratings": []
    },
    "type": "ai",
    "name": null,
    "id": "run-17xxxxxd-xxxx-xxxx-bxxx-02xxxxxxxxxx-x",
    "example": false,
    "tool_calls": [],
    "invalid_tool_calls": [],
    "usage_metadata": {
        "input_tokens": 16,
        "output_tokens": 185,
        "total_tokens": 201,
        "input_token_details": {
            "cache_read": 0
        }
    }
}
'''