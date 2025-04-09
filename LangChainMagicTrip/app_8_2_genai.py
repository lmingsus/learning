# import google.generativeai as genai
# 改為：pip install -U -q "google-genai"
from google import genai
from google.genai import types

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


# pricing: https://ai.google.dev/gemini-api/docs/pricing?hl=zh-tw
# models: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference


client = genai.Client(api_key=GEMINI_API_KEY)
# print(type(client))


response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='什麼是孿生質數？請以約150字解釋。',

    config=types.GenerateContentConfig(
        system_instruction='你是對專門研究數論的七十歲數學系教授',
        temperature=0.5,    # 控制生成內容的隨機性，值越高生成的內容越多樣化
        # top_p=0.5,    # 使用核取樣（nucleus sampling）來限制生成的內容，值越低生成的內容越集中於高概率的選項
        # max_output_tokens=400,    # 控制生成的內容長度
        # top_k=40,    # 控制生成的內容中每個字元出現的機率，值越高生成的內容越多樣化，值越低生成的內容越集中於高概率的選項
        # repetition_penalty=1.0,    # 控制生成內容中重複的懲罰程度，值越高模型越傾向於避免重複，默認值 1.0 表示不對重複進行額外懲罰
        # presence_penalty=0.0,    # 控制生成內容中引入新主題的傾向，值越高模型越傾向於引入新主題，默認值 0.0 表示不對引入新主題進行額外鼓勵
        # stop_sequences=[],    # 指定一個或多個停止序列，模型將在遇到這些序列時停止生成，例如 ["\n"]
        # response_mime_type= 'application/json',
        # seed=42,    # 設定隨機種子
    )
)

print(response.text)

print(response.model_dump_json(exclude_none=True, indent=4))
{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "哎呀，孿生質數啊，這可是數論中一個迷人的小角落。\n\n所謂孿生質數，指的是一對相差為2的質數。換句話說，它們是「近鄰」的質數，彼此之間只隔著一個偶數。\n\n舉例來說，(3, 5)、(5, 7)、(11, 13) 和 (17, 19) 都是孿生質數。\n\n數學家們對孿生質數的分布非常感興趣。一個著名的猜想是孿生質數有無窮多對，但至今尚未被證明。儘管如此，我們已經知道孿生質數在數軸上會越來越稀疏，也就是說，隨著數字變大，找到孿生質數的機會就越小。\n\n研究孿生質數不僅僅是為了滿足好奇心，它還能幫助我們更深入地理解質數的本質和分布規律。\n"
                    }
                ],
                "role": "model"
            },
            "avg_logprobs": -0.17008807898708508,
            "finish_reason": "STOP"
        }
    ],
    "model_version": "gemini-2.0-flash-001",
    "usage_metadata": {
        "candidates_token_count": 209,
        "prompt_token_count": 31,
        "total_token_count": 240
    },
    "automatic_function_calling_history": []
}

