from google import genai

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

client = genai.Client(api_key=GEMINI_API_KEY)



# Upload the single audio file 上傳檔案
audio_file_name = "radio_8_5.mp3"
print(f"Uploading file...")
# audio_file = genai.upload_file(path=audio_file_name)
audio_file = client.files.upload(file="radio_8_5.mp3")
print(f"Completed upload: {audio_file.uri}")
print(audio_file.model_dump_json(exclude_none=True, indent=4))
# 印出：
{
    "name": "files/nxxxxxxxxxxa",
    "mime_type": "audio/mpeg",
    "size_bytes": 43226768,
    "create_time": "2025-03-23T18:08:45.865791Z",
    "expiration_time": "2025-03-25T18:08:45.831713Z",
    "update_time": "2025-03-23T18:08:45.865791Z",
    "sha256_hash": "Zxxxxxxx=",
    "uri": "https://generativelanguage.googleapis.com/v1beta/files/nxxxxxxxxxxa",
    "state": "ACTIVE",
    "source": "UPLOADED"
}




prompt = """
請仔細聆聽以下的音檔，再寫下這個聲音檔的重要內容摘要。
"""

# model = genai.GenerativeModel(
#     model_name='gemini-2.0-flash-001',
#     system_instruction="使用繁體中文回答。"
# )
# response = model.generate_content([prompt, audio_file])


response = client.models.generate_content(
    model='gemini-2.0-flash', 
    contents=[
        prompt, 
        audio_file
    ]
)

print(response.text)
print(response.model_dump_json(exclude_none=True, indent=4))
'''
{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "這是一個關於科技趨勢的廣播節目「科技透視Tech on Toast」，主持人為柯林。節目中，邀請了行動開發學院負責人Ryan Chun，來討論近期很紅的AI聊天機器人，以及聊天機器人為何這麼受歡迎，還有他們是不是真的像傳聞中的厲害。\n\nRyan提到，聊天機器人的發展已有一段時間，概念上來說，人工智慧一直希望能打造出一台可以對話的機器，如果在一段時間內，無法分辨布幕之後是真人還是聊天機器人的話，那這就是一個很成功的聊天機器人，大家也都在努力朝這個方向邁進。\n\n主持人柯林，在稍後也與Ryan討論了AI聊天機器人為何在近期成為熱門話題。"
                    }
                ],
                "role": "model"
            },
            "avg_logprobs": -0.8850702285766602,
            "finish_reason": "STOP"
        }
    ],
    "model_version": "gemini-2.0-flash",
    "usage_metadata": {
        "candidates_token_count": 160,
        "prompt_token_count": 45022,
        "total_token_count": 45182
    },
    "automatic_function_calling_history": []
}
'''


# =====================================================================
# Download file
'''
Files created by `upload` can't be downloaded. You can tell which files are
downloadable by checking the `source` or `download_uri` property.
'''

# =====================================================================
# 列出所有上傳的檔案

for file in client.files.list():
    print(file.name)

file = client.files.get(name=file.name)
print(file.model_dump_json(exclude_none=True, indent=4))
# =====================================================================
# 沒有要再問問題時，再把檔案從雲端刪除
# genai.delete_file(audio_file.name)
# print(f"Deleted file {audio_file.uri}")


response_del = client.files.delete(name=file.name)