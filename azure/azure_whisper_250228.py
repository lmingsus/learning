import configparser
from openai import AzureOpenAI

# Azure OpenAI 設定
# 讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')

# 初始化 Azure OpenAI 客戶端
client = AzureOpenAI(
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/audio/completions?api-version={AZURE_OPENAI_API_VERSION}
    api_key=config.get('AZURE', 'AZURE_OPENAI_API_KEY'),  # Azure OpenAI 金鑰
    api_version=config.get('AZURE', 'AZURE_OPENAI_API_VERSION'),  # API 版本
    azure_endpoint=config.get('AZURE', 'AZURE_OPENAI_ENDPOINT')  # Azure 端點
)

def transcribe_audio(audio_file_path):
    """
    使用 Azure OpenAI 的 Whisper 模型來轉錄音訊檔案
    """
    try:
        # 開啟並讀取音訊檔案
        with open(audio_file_path, "rb") as audio_file:
            # 呼叫 API 進行音訊轉錄
            response = client.audio.transcriptions.create(
                model=config.get('AZURE', 'deployment_id'),  # AZURE_OPENAI_DEPLOYMENT_NAME
                file=audio_file,            # 音訊檔案
            )
            return response
    except Exception as e:
        # 如果發生錯誤，印出錯誤訊息
        print(f"轉錄過程發生錯誤: {str(e)}")
        return None

def main():
    # 使用範例
    audio_file_path = "AI競賽.m4a"  # 請更改為您的音訊檔案路徑
    
    # 取得轉錄結果
    transcription = transcribe_audio(audio_file_path)
    
    # 輸出結果
    if transcription:
        print("轉錄結果:")
        print(transcription)
    else:
        print("轉錄失敗")

# 程式進入點
if __name__ == "__main__":
    main()