from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# # 使用 QdrantVectorStore
# from qdrant_client import QdrantClient
# from langchain_qdrant import QdrantVectorStore

# 改用 FAISS
from langchain_community.vectorstores import FAISS

from tqdm import tqdm
import time
import logging
from pathlib import Path

import logging
# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


from configparser import ConfigParser
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/embeddings?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT]):
        raise Exception("Please provide all required Azure OpenAI configuration values in config.ini.") 
    
    # Azure OpenAI Embedding
    EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
    if not all([EMBEDDING_MODEL, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, AZURE_OPENAI_API_EMBEDDING_VERSION]):
        raise Exception("Please provide all required Azure OpenAI Embedding configuration values in config.ini.")
except Exception as e:
    logger.error(f"config.ini 讀取失敗：{str(e)}")




def create_vectorstore_in_batches(documents, embedding_llm, batch_size=5):
    """批次處理文件向量化"""
    vectorstore = None
    total_batches = len(range(0, len(documents), batch_size))
    
    with tqdm(total=total_batches, desc="處理批次") as pbar:
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            try:
                if vectorstore is None:
                    vectorstore = FAISS.from_documents(batch, embedding_llm)
                    logger.info(f"建立新的向量資料庫，批次 {i//batch_size + 1}/{total_batches}")
                else:
                    vectorstore.add_documents(batch)
                    logger.info(f"新增文件到向量資料庫，批次 {i//batch_size + 1}/{total_batches}")
                
                # 每處理一個批次後儲存
                vectorstore.save_local("faiss_index")
                logger.info(f"儲存向量資料庫，批次 {i//batch_size + 1}/{total_batches}")
                
                # 更新進度條
                pbar.update(1)
                
                # 等待一段時間避免達到 API 限制
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"處理批次 {i//batch_size + 1} 時發生錯誤: {str(e)}")
                time.sleep(60)  # 遇到錯誤時等待較長時間
                continue
    
    return vectorstore




def main():
    # 初始化 embedding 模型
    embedding_llm = AzureOpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
        api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=AZURE_OPENAI_API_EMBEDDING_VERSION,
    )

    # 載入 PDF 文件
    loader = PyPDFLoader("docs/勞動基準法.pdf")
    pages = loader.load_and_split()

    # 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        # separators=["\n\n", "\n", "。", "，"],  # 優先使用段落分隔，其次是句號和逗號
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(pages)

    # 使用批次處理建立向量資料庫
    vectorstore = create_vectorstore_in_batches(
        documents=splits,
        embedding_llm=embedding_llm,
        batch_size=5
    )
    
    logger.info("向量資料庫建立完成")

if __name__ == "__main__":
    main()
