from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import faiss
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from configparser import ConfigParser
from tenacity import retry, wait_exponential, stop_after_attempt
import logging
from ratelimit import limits, sleep_and_retry

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 讀取設定

from configparser import ConfigParser
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/embeddings?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    # AZURE_OPENAI_API_VERSION = config.get('Azure', 'GPT35_TURBO_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    # AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'GPT35_TURBO_DEPLOYMENT_NAME')

    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
        raise Exception("Please provide all required Azure OpenAI configuration values in config.ini.") 
    
    # Azure OpenAI Embedding
    EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
    if not all([EMBEDDING_MODEL, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, AZURE_OPENAI_API_EMBEDDING_VERSION]):
        raise Exception("Please provide all required Azure OpenAI Embedding configuration values in config.ini.")
except Exception as e:
    logger.error(f"config.ini 讀取失敗：{str(e)}")

# 初始化模型
generator_llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
)

embedding_llm = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version=AZURE_OPENAI_API_EMBEDDING_VERSION,
)


# 設置 FAISS CPU 多線程
faiss.omp_set_num_threads(4)  # 允許使用 4 核心加速檢索


# 載入向量資料庫
faiss_vectorstore = FAISS.load_local(
    "faiss_index",
    embedding_llm,
    allow_dangerous_deserialization=True
)

# 檢查索引是否已訓練
if not faiss_vectorstore.index.is_trained:
    raise ValueError("FAISS 索引未訓練，請先執行訓練！")

# 設置檢索器
retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 1})

# 建立提示樣板
template = ChatPromptTemplate.from_template("""你是一位精通台灣勞基法的專家。請根據以下參考資料回答問題：

參考資料：{context}

問題：{question}

專家回答：""")

# 建立 QA Chain
qa_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | template
    | generator_llm
    | StrOutputParser()
)


# 設定 API 限流，每 60 秒最多 10 次請求
@sleep_and_retry
@limits(calls=10, period=60)
@retry(
    wait=wait_exponential(multiplier=5, min=5, max=60),
    stop=stop_after_attempt(5)
)
def query_with_retry(question: str):
    """帶有重試機制的查詢函數"""
    return qa_chain.invoke(question)

def main():
    try:
        question = "勞工加班費的計算方式是什麼？"
        logger.info(f"開始查詢：{question}")
        response = query_with_retry(question)
        print("\n回答：")
        print(response)
    except Exception as e:
        logger.error(f"查詢時發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()



# test1: gpt-4o-mini, k=1
'''
回答：
根據《勞動基準法》第24條，勞工加班費的計算方式如下：

1. **延長工作時間在二小時以內者**：
   - 按平日每小時工資額加給三分之一以上。

2. **再延長工作時間在二小時以內者**：
   - 按平日每小時工資額加給三分之二以上。

3. **依第三十二條第四項規定，若延長工作時間者**：   
   - 按平日每小時工資額加倍發給。

此外，若勞工在休息日工作：

1. **工作時間在二小時以內者**：
   - 按平日每小時工資額另再加給一又三分之一以上。

2. **工作二小時後再繼續工作者**：
   - 按平日每小時工資額另再加給一又三分之二以上。

這些規定確保了勞工在加班及休息日工作時能獲得合理的報酬。
'''
# test2: gpt-35-turbo, k=2
'''
回答：
根據《勞動基準法》第24條，雇主延長勞工工作時間時，加班費的計算方式為：
- 延長工作時間在二小時以內者，按平日每小時工資額加給三分之一以上。    
- 再延長工作時間在二小時以內者，按平日每小時工資額加給三分之二以上。  
- 依第32條第四項規定，延長工作時間者，按平日每小時工資額加倍發給。    

因此，根據勞基法規定，加班費的計算方式取決於延長工作時間的長度。
'''
# test3: gpt-35-turbo, k=5
'''
回答：
根據「勞動基準法」第24條的規定，雇主延長勞工工作時間時，加班費的計算方式如下：  
1. 延長工作時間在2小時以內時，按照平日每小時工資額加給三分之一以上。
2. 再延長工作時間在2小時以內時，按照平日每小時工資額加給三分之二以上。
3. 根據第32條第4項規定延長工作時間時，按照平日每小時工資額加倍發給。

因此，根據勞基法的規定，雇主在延長勞工工作時間時應按照以上規定支付加班費給勞工。
'''