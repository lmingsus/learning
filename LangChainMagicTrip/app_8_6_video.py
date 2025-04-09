from google import genai
import time

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



# Upload the video file
video_file_name = "video_8_6.mp4"
print(f"Uploading video file...")
video_file = client.files.upload(file=video_file_name)
print(f"Completed upload: {video_file.uri}")
print(123)
print(video_file.model_dump_json(exclude_none=True, indent=4))
# video_file 印出：
{
    "name": "files/a90oca002skc",
    "mime_type": "video/mp4",
    "size_bytes": 20956574,
    "create_time": "2025-03-23T18:58:37.817067Z",
    "expiration_time": "2025-03-25T18:58:37.782526Z",
    "update_time": "2025-03-23T18:58:37.817067Z",
    "sha256_hash": "NDU1OA==",
    "uri": "https://generativelanguage.googleapis.com/XXXXX/files/XXXXX",
    "state": "PROCESSING",
    "source": "UPLOADED"
}


# Wait for the video to be processed
while video_file.state.name == "PROCESSING":
    print("Waiting for video to be processed.")
    # time.sleep(10)
    # video_file = genai.get_file(video_file.name)
    video_file = client.files.get(name=video_file.name)
print(video_file.model_dump_json(exclude_none=True, indent=4))
# video_file 印出：
{
    "name": "files/a90oca002skc",
    "mime_type": "video/mp4",
    "size_bytes": 20956574,
    "create_time": "2025-03-23T18:58:37.817067Z",
    "expiration_time": "2025-03-25T18:58:37.782526Z",
    "update_time": "2025-03-23T18:58:42.475918Z",
    "sha256_hash": "NDU1OA==",
    "uri": "https://generativelanguage.googleapis.com/XXXXX/files/XXXXX",
    "state": "ACTIVE",
    "source": "UPLOADED",
    "video_metadata": {
        "videoDuration": "37s"
    }
}

if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)


# Upload the image file
image_file_name = "image_8_6.jpg"
print(f"Uploading image file...")
image_file = client.files.upload(file=image_file_name)
print(f"Completed upload: {image_file.uri}")
print(image_file.model_dump_json(exclude_none=True, indent=4))
# image_file 印出：
{
    "name": "files/e7kfignbusbl",
    "mime_type": "image/jpeg",
    "size_bytes": 1098779,
    "create_time": "2025-03-23T19:09:36.636070Z",
    "expiration_time": "2025-03-25T19:09:36.605495Z",
    "update_time": "2025-03-23T19:09:36.636070Z",
    "sha256_hash": "MD==",
    "uri": "https://generativelanguage.googleapis.com/XXXXX/files/XXXXX",
    "state": "ACTIVE",
    "source": "UPLOADED"
}


image_file = client.files.get(name=image_file.name)
print(image_file.model_dump_json(exclude_none=True, indent=4))
{
    "name": "files/e7kfignbusbl",
    "mime_type": "image/jpeg",
    "size_bytes": 1098779,
    "create_time": "2025-03-23T19:09:36.636070Z",
    "expiration_time": "2025-03-25T19:09:36.605495Z",
    "update_time": "2025-03-23T19:09:36.636070Z",
    "sha256_hash": "MD==",
    "uri": "https://generativelanguage.googleapis.com/XXXXX/files/XXXXXXXXXXXX",
    "state": "ACTIVE",
    "source": "UPLOADED"
}

# List uploaded files
for file in client.files.list():
    print(file.name)




# Create the prompt.
prompt = "請問你從影片中看到什麼？用正體中文回答。"
prompt = "請詳細地條列出影片中每個人所說的話，用正體中文回答。"
prompt = "請問影片中有沒有出現圖片裡的這種動物，在第幾秒，他做了什麼，用正體中文回答。"



# Make the LLM request.
print("Gemini思考中...")
response = client.models.generate_content(
    model='gemini-2.0-flash', 
    contents=[
        prompt, 
        image_file,
        video_file,
    ],
)
print(response.text)
print(response.model_dump_json(exclude_none=True, indent=4))
{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "好的，在影片中從0:00到0:31都出現了獅子，牠們主要是在綠地上行走。不過，這些獅子並非你圖片中的雄獅，而是兩隻雌獅。"
                    }
                ],
                "role": "model"
            },
            "avg_logprobs": -0.8063242539115574,
            "finish_reason": "STOP"
        }
    ],
    "model_version": "gemini-2.0-flash",
    "usage_metadata": {
        "candidates_token_count": 46,
        "prompt_token_count": 13924,
        "total_token_count": 13970
    },
    "automatic_function_calling_history": []
}




# 沒有要再問問題時，再把圖片、影片從雲端刪除：
# Delete the cloud video file
for file in client.files.list():
    print(f'刪除檔案：{file.name}')
    file = client.files.delete(name=file.name)
    # print(file.model_dump_json(exclude_none=True, indent=4))    # 回傳：{}