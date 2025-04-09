from google import genai
import asyncio
from typing import Optional
import time
from configparser import ConfigParser
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 設定和初始化
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    GEMINI_API_KEY = config.get('GEMINI', 'API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("請在 config.ini 中設定所有必要的 Gemini 參數")
except Exception as e:
    logger.error(f"設定讀取錯誤: {str(e)}")
    raise



client = genai.Client(api_key=GEMINI_API_KEY)



@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def check_file_status(client, file) -> Optional[dict]:
    """檢查檔案處理狀態的非同步函數"""
    try:
        updated_file = client.files.get(name=file.name)
        logger.info(f"檔案 {file.name} 目前狀態: {updated_file.state.name}")
        if updated_file.state.name != "PROCESSING":
            return updated_file
        return None
    except Exception as e:
        logger.error(f"檢查狀態時發生錯誤: {str(e)}")
        raise

async def wait_for_processing(client, file, timeout: int = 300):
    """等待檔案處理完成的主要非同步函數"""
    logger.info(f"開始等待處理 {file.name}...")
    start_time = time.time()
    
    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError(f"處理 {file.name} 超時")
            
        result = await check_file_status(client, file)
        if result:
            logger.info(f"{file.name} 處理完成！")
            return result
            
        await asyncio.sleep(5)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def upload_file(client, file_name: str):
    """上傳檔案的非同步函數"""
    logger.info(f"開始上傳 {file_name}")
    try:
        file = client.files.upload(file=file_name)
        logger.info(f"{file_name} 上傳完成: {file.uri}")
        return file
    except Exception as e:
        logger.error(f"上傳 {file_name} 時發生錯誤: {str(e)}")
        raise


async def process_files(video_file_name: str, image_file_name: str, prompt: str):
    """處理檔案上傳和查詢的主要流程"""
    try:
        # 同時上傳影片和圖片，設定更長的超時時間
        upload_tasks = [
            upload_file(client, video_file_name),
            upload_file(client, image_file_name)
        ]
        
        # 使用 gather 處理多個上傳任務
        try:
            video_file, image_file = await asyncio.gather(*upload_tasks)
        except Exception as e:
            logger.error(f"上傳檔案時發生錯誤: {str(e)}")
            raise
        

        if video_file.state.name == "PROCESSING":
            video_file = await wait_for_processing(client, video_file)
        
        # 取得圖片的最新狀態
        image_file = client.files.get(name=image_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError(f"影片處理失敗: {video_file.state.name}")
        
        # 進行 LLM 請求
        logger.info("開始生成內容...")
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=[prompt, image_file, video_file]
        )
        
        logger.info("\n回答內容:")
        print(response.text)
        logger.info("\n詳細資訊:")
        print(response.model_dump_json(exclude_none=True, indent=4))
        
        return response
        
    except Exception as e:
        logger.error(f"處理過程中發生錯誤: {str(e)}")
        raise
    
async def cleanup_files():
    """清理已上傳的檔案"""
    try:
        logger.info("開始清理檔案...")
        for file in client.files.list():
            logger.info(f"刪除檔案: {file.name}")
            client.files.delete(name=file.name)
        logger.info("檔案清理完成")
    except Exception as e:
        logger.error(f"清理檔案時發生錯誤: {str(e)}")
        raise

async def main():
    video_file_name = "video_8_6.mp4"
    image_file_name = "image_8_6.jpg"
    prompt = "請問影片中有沒有出現圖片裡的這種動物，在第幾秒，他做了什麼，用正體中文回答。"
    
    try:
        response = await process_files(video_file_name, image_file_name, prompt)
        # print(response.text)
        # print(response.model_dump_json(exclude_none=True, indent=4))
        if input("\n是否要清理檔案？(Y/n)：").lower() == 'y':
            await cleanup_files()
    except Exception as e:
        logger.error(f"主程序發生錯誤: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())